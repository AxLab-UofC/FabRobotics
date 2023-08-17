from printer_manager import Print_Manager
from events import Event, ToioEvent, GCode_Event
from toioManager import ToioManager
import math
import random
import time

#created to be able to program different bed coordinates but never used
class Bed:
    def __init__(self, xmin, xmax, ymin, ymax) -> None:
        self.xScale = (xmin, xmax - xmin)
        self.yScale = (ymin, ymax - ymin)
    
    def scale(self, h, k) -> list:
        newx = self.xScale[0] + (h/180) * self.xScale[1]
        newy = self.yScale[0] + (k/180) * self.yScale[1]

        return (int(newx), int(newy))

#Timeline execution and generation
class TimelineManager:
    def __init__(self):
        #Initializes queue, toio manager, print manager, and connects to the printer
        self.queue = []
        self.toioMan = ToioManager()
        self.printMan = Print_Manager()
        self.printMan.connect_printer()
        time.sleep(2)
        self.place = 0
        self.finish = False
        self.svgs = []
        self.queue.append(GCode_Event(1, "start_up.gcode", "Start Up Printer")) #Adds start up printer event
        # self.modify_dock(882,358, "Print Toio Dock on Bed") #THIS LINE FOR ADDING DOCK
        self.queue.append(GCode_Event(1, "cool_down.gcode", "Cool Down Printer", "finishing")) #adds cool down printer event
        self.printMan.Api.fileUpload("start_up.gcode") #uploads both to octoprint
        self.printMan.Api.fileUpload("cool_down.gcode")

        # event = ToioEvent("Motor Down Ramp") #Event for motoring down ramp
        # event.addTarget(0,882,400,180) #Note: Coordinates are specific to our bed.
        # event.addTarget(0,780,430,180)
       
        # event.addMotor(0, 80, 80, 250)
        # event.addMotor(0, 80, 80, 250)
        # self.queue.append(event) 
       
       
        
    #All files come through here, will split up a file into chunks of 2000 lines and create gcode events for them as well as 
    #ids so they can be grouped together
    def add_Gcode_event(self, file, name = "default", style = "normal", x = -1, y = -1):
        lines = self.file_to_array(file)
        if(len(lines)>2000):
            file_name = file
            val = 1
            while(len(lines) >2000):
               
                file_name = file[:len(file)-6] + str(val)+ ".gcode"
                chunk = lines[0:2000]
                lines = lines[2000:]
                self.write_file(chunk,file_name)
                event = GCode_Event(val, file_name, name, style, x, y)
                self.queue.insert(len(self.queue)-1, event)
              
                self.printMan.Api.fileUpload(event.file)
                val +=1
            file_name = file[:len(file)-6] + str(val) + ".gcode"
            self.write_file(lines,file_name)
            event = GCode_Event(val, file_name, name, style, x, y)
            self.queue.insert(len(self.queue)-1, event)
            self.printMan.Api.fileUpload(event.file)
        #For files smaller than 2000 lines
        else:
            event = GCode_Event(1, file, name, style, x, y)
            self.queue.insert(len(self.queue)-1, event)
            self.printMan.Api.fileUpload(event.file)

    #Creates a toio event and adds it in between start up and cool down
    def add_Toio_event(self, name, code = []):
        event = ToioEvent(name, code)
        self.queue.insert(-1, event)

     #Creates a general event(either toio or gcode) and adds it in between start up and cool down
    def addEvent(self, event:Event) -> None:
        self.queue.insert(-1, event) 
    
    def addMotorDownRamp(self):
        event = ToioEvent("Motor Down Ramp") #Event for motoring down ramp
        event.addTarget(0,882,400,180) #Note: Coordinates are specific to our bed.
        event.addTarget(0,780,430,180)
       
        event.addMotor(0, 80, 80, 250)
        event.addMotor(0, 80, 80, 250)
        self.addEvent(event)
       

    
    #will rewrite a new file with inputted Gcode
    def write_file(self, Gcode, file_name):
        with open(file_name, 'w') as f:
            new_Gcode = ""
            for line in Gcode:   
                new_Gcode += line
            f.seek(0)    
            f.write(new_Gcode)
    
    #Starts the timeline
    def start(self):
        if(len(self.queue)>self.place):
            self.queue[self.place].start()
            if(type(self.queue[self.place]) == GCode_Event):
                self.printMan.print_event(self.queue[self.place])
                print(self.queue[self.place].name)
                #If one of these print types then constantly drive forward
                if(self.current_print_type() == "print_on" or self.current_print_type() == "driver"):
                    if(len(self.toioMan.toios) > 0):
                        print("Here")
                        place = 0
                        for toio in self.toioMan.toios:
                            self.toioMan.motor(place,10,10,0)
                            place = place +1
            if(type(self.queue[self.place]) == ToioEvent):
                self.printMan.move_extruder(150)
                #Ensures toio doesnt go back to targeting corner when the extruder is about to print on it
                while(self.current_print_type() != "toio"):
                    print("Waiting for current_print_type to change")
                time.sleep(3)
                self.toioMan.execute(self.queue[self.place])
                print(self.queue[self.place].name)
                
        else:
            self.finish = True
    #executes next event ensuring that printing the event before is finished
    def execute_next(self):
        if(self.printMan.finished()):
        
            self.queue[self.place].complete()
            self.place +=1
            self.start() #calls start again for the next index in queue
            self.toioMan.getStatusAll()
            print("Next Executed")
        else:
            print(self.printMan.progress()) #simply used for troubleshooting in terminal
    
    #returns current event
    def current(self):
        if(len(self.queue) >0):
            return self.queue[self.place]
       
    #returns name of current event
    def current_name(self):
        if(len(self.queue) >0):
            if(self.place < len(self.queue)):
                return self.queue[self.place].name
    
    #returns the number of chunks in the current event if it is a gcode event
    def num_chunks(self):
        num = 0
        for event in self.queue:
            if event.name == self.current_name():
                num = num + 1
        if(type(self.current()) == GCode_Event):
            val = self.current()._id
            return str(val) + "/" + str(num)
        else:
            return "0/" + str(num)

    #returns variable finish so server/front end knows when the queue is done
    def finish_queue(self):
        return self.finish
   

    #Returns list of event names, gets rid of duplicates
    def get_events_names(self):
        self.names = []
        for event in self.queue:
            if(event.name not in self.names):
                self.names.append(event.name)
        return self.names
    
    #returns list of events
    def get_events(self):
        events = []
        names = []
        for (i, event) in enumerate(self.queue):
            if(event.name not in names):
                events.append({"name": event.name, "status":event.status, "type":event.type, "i":i})
                names.append(event.name)
            else:
                if event.status == "current":
                    events[-1]["status"] = "current"
        return events

    #takes in a file and returns an array
    def file_to_array(self, file, constraints = "")  -> list:
        with open(file, 'r+') as f:

            Gcode = []           # where the new modified code will be put
            content = f.readlines()  # gcode as a list where each element is a line 

            for line in content: 
                Gcode.append(line)
            return Gcode
    
    #clears and resets the queue
    def clear_Queue(self):
        self.queue = []
        self.place = 0
        self.finish = False 
    
    #used for layer visualization on front end
    def addLayer(self, svgstr:str) -> None:
        self.svgs.append(svgstr)

    #returns type of the current event  
    def current_type(self):
        if(len(self.queue) >0):
            if(self.place < len(self.queue)):
                return self.queue[self.place].type

    #returns print type of the current event, e.g. driver, support, print_on
    def current_print_type(self):
        if(len(self.queue) >0):
            if(type(self.queue[self.place]) == GCode_Event):
                print()
                print(self.current())
                # print(self.current.get_style())
                return self.queue[self.place].style
            else:
                return "toio"

    #gets extruder_temp
    def extruder_temp(self):
        target = str(math.ceil(self.printMan.Api.get_extruder_target_temp()))
        current = str(math.ceil(self.printMan.Api.get_extruder_current_temp()))
        return current + " / " + target + " °C"
    
    #gets bed_temp
    def bed_temp(self):
        target = str(math.ceil(self.printMan.Api.target_bed_temp()))
        current = str(math.ceil(self.printMan.Api.get_bed_temp()))
        return current + " / " + target + " °C"

    #modifys a dock to the x and y coordinates of toio, based around the center.
    # Note: coordinates will change with different bed. 
    def modify_dock(self, x , y, name, theta = "0"):
        x_diff = ((x - 882)/7.2619048)*10
        y_diff = ((y - 358)/7.2619048)*10
        i = random.randint(0,200)
        n = "dock" + str(i) + ".gcode"
        Gcode = self.file_to_array("dock.gcode")
        new_Gcode = []
        for line in Gcode:
            section = line.split(" ")
            newline = ""
            for sec in section:
                if 'X' in sec:  
                    if (len(sec)<10 and ';' not in sec):
                        val = float(sec[1:])
                        val += x_diff
                        if(val >= 179):
                            val = 179
                        sec = "X" + str(val)
                if 'Y' in sec:  
                    if (len(sec)<10 and ';' not in sec):
                        val = float(sec[1:])
                        val -= y_diff
                        if(val >= 179):
                            val = 179
                        sec = "Y" + str(val)
                newline += sec + " "
            new_Gcode.append(newline)
            if("M900 K0.2" in line):
                new_Gcode.append("G0 X90 Y90 Z15")
            
            
            
        self.write_file(new_Gcode, n)
        self.add_Gcode_event(n, name, "normal")


     #Note: The below code was used to attempt continous multiprints. 
        # event1 is both robots target the corner
        # event2 is the first toio moving into a dock
        # event3 is the robots switching(Most issues)
        # event4 is the second robot driving down the dock

        ###########################################
        # self.modify_dock(850, 357, "dock3.gcode")
        # self.modify_dock(882, 400, "dock1.gcode")
        # attempt at controling 2 toio
        # event1 = ToioEvent("Target Corners")
        # event1.addTarget(0, (795 + 0*30),430,270)
        # event1.addTarget(1, (795 + 1*30),430,270)
        # self.queue.append(event1) 

        # event2 = ToioEvent("First Toio Move in")
        # event2.addTarget(1, 882, 357+40, 270)
        # event2.addTarget(1, 882, 357+20, 270)
        # event2.addTarget(1,882,357, 270)
        # event2.addMotor(1, 10, 10, 0)
        # self.queue.append(event2) 

        # event3 = ToioEvent("Second Toio Move in")
        # event3.addTarget(1, 882, 357+40, 270)
        # event3.addTarget(1, 920, 357+50, 90)
        # event3.addTarget(0, 882, 357+40, 270)
        # event3.addTarget(0, 882, 357+20, 270)
        # event3.addTarget(0,882,357, 270)
        # event3.addMotor(0, 10, 10, 0)
        # event3.addTarget(1,882,400,180)
        # event3.addTarget(1,780,430,180)
        # event3.addMotor(1, 80, 80, 250)
        # event3.addMotor(1, 80, 80, 250)
        # self.queue.append(event3) 

        # event4 = ToioEvent("Motor Down Ramp")
        # event4.addTarget(0,882,400,180)
        # event4.addTarget(0,780,430,180)
       
        # event4.addMotor(0, 80, 80, 250)
        # event4.addMotor(0, 80, 80, 250)
        # self.queue.append(event4) 


