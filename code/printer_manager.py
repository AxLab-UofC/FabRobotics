from octocontrol import OctoprintAPI
import time
import math
class Print_Manager:

    #Initializes Print Manager and Connects to API
    def __init__(self):
        self.Api = OctoprintAPI("axlab.local/", "", "F5EFDBD8F3AB4C03B8C690B0F6917702") #API Key and address, will change for new instance of octoprint
        self.Api.connect_to_printer() 
        time.sleep(3)
        # http://axlab.local/api/connection
       

  
   #Modifys dock code to x and y coordinates based on toio coordinates
    def modify_dock(self, x , y, theta):
        y_diff = ((x - 250)/7.2)*10
        x_diff = ((y - 397)/7.2)*10
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
                        val += y_diff
                        if(val >= 179):
                            val = 179
                        sec = "Y" + str(val)
                newline += sec + " "
            new_Gcode.append(newline)
        return new_Gcode

    #Doesnt work, should be able to purge extruder but needs tweaking
    def purge(self) -> None:
        self.run_Gcode(self.file_to_array("Gcode/purge.gcode"))

    #will select a file to be printed
    def print_event(self, event) -> None:
        success = False
        while(not success):
            val = int(self.Api.select_file(event.file))
            if(val == 204):
                print("Success")
                success = True
            else:
                print("Failed Select")
            

      
    
   
    #Takes in GCode as an Array and exectues it
    def run_Gcode(self, Gcode) -> None:
        while(len(Gcode)>2000):
            chunk = Gcode[0:2000]
            Gcode = Gcode[2000:]
            self.Api.send_gcode(chunk)
        self.Api.send_gcode(Gcode)
       

    
    #Takes in a file and converts the code into an array of lines
    def file_to_array(self, file)  -> list:
        with open(file, 'r+') as f:

            Gcode = []           # where the new modified code will be put
            content = f.readlines()  # gcode as a list where each element is a line 

            for line in content: 
                Gcode.append(line)
            return Gcode
    
    #Moves the extruder out of the way and up high, default is center 90cm but can be changed
    def move_extruder(self,height = 90, x = 90, y = 90)  -> None:
        self.Api.send_gcode([("G0 X" + str(x) + " Y" + str(y) + " Z" + str(height))])

    #Connects a printer and checks to confirm connection
    def connect_printer(self)  -> None:
        self.Api.connect_to_printer()
        print(self.Api.is_printer_connected())
        print(self.Api.get_printer_status())
    
    #Gcode command for delays
    def delay(self, time = 5000)  -> None:
       self.Api.send_gcode([("G4 P" + str(time))])

    #Sends API request for canceling
    def cancel(self) -> None:
        self.Api.cancel_job()
    
    #Will return the file printing
    def current(self) -> str:
        return self.Api.get_file_printing()

    #Returns if print progress is finished
    def finished(self) -> bool:
        if(self.Api.get_print_progress() == None):
            return "No Print Going"
        return self.Api.get_print_progress() >= 100

    #returns val for print progress rounded up
    def progress(self) -> bool:
        if(self.Api.get_print_progress() == None):
            return "No Print Going"
        return math.ceil(self.Api.get_print_progress())
       
    