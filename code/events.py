#Parent for Timeline Events
class Event:
    def __init__(self, type:str, name:str="default") -> None:
        self.type = type
        self.name = name
        self.status = 'inQueue'
    #Gives status of event if it is inQueue, current, or completed to display on UI
    def start(self):
        self.status = 'current'

    def complete(self):
        self.status = 'complete'
        
#Sub class for Toio Specific events
class ToioEvent(Event):
    def __init__(self, name:str = "default", cmds:list = []):
        Event.__init__(self, "toio", name)
        self.cmds = []

    #Add Command for Connecting toio
    def addConnect(self, toioNum:int) -> None:
        self.cmds.append(["c", toioNum])

    #Add command for Targeting toio coordinates
    def addTarget(self, index:int, x:int, y:int, theta = 90) -> None:
        self.cmds.append(["t", index, x, y, theta])

    #Add command for Motor
    def addMotor(self, index:int, leftspeed: int, rightspeed: int, duration: int) -> None:
        self.cmds.append(["m", index, leftspeed, rightspeed, duration])

#Sub class for Gcode Specific events
class GCode_Event(Event):
    def __init__(self, _id, file, name = "default", style = "normal", x = "-1", y = "-1"):
        Event.__init__(self, "print", name)
        self.file = file
        self.style = style
        self._id = _id
        self.x = int(x)
        self.y = int(y)
        if(file != "start_up.gcode" and file != "cool_down.gcode"):
            self.cut(self.file)
        if(self.style == "print_on"):
            self.move_up(26.2, self.file)
        if(self.x != -1 and self.y != -1):
            self.support_slicer()
            print("cut")
            print(self.x)
            print(self.y)
        
    
    #modifys Gcode file to move print on top of toio
    def move_up(self, offset, file):
        with open(file, 'r+') as f:
            new_Gcode = ""
            content = f.readlines()
            for line in content:
                sections = line.split(" ")
                newline = ""
                for sec in sections:
                    
                    if 'Z' in sec:  
                        if (len(sec)<10 and ';' not in sec):
                            val = float(sec[1:])
                            val += offset
                            if(val >= 179):
                                val = 179
                            sec = "Z" + str(val)
                            # print(sec)
                            
                    
                    newline += sec + " "
            
                new_Gcode+=newline
            f.seek(0)    
            f.write(new_Gcode)
            
    #Cuts out the heating and cooling sections from the file
    def cut(self, file):
        lines = self.file_to_array(file)
        with open(file, 'w') as f:
            new_Gcode = ""
            start = False
            finish = False
            beginning = False
            for line in lines:
                if("M900 K0.2" in line):
                    beginning = True
            for line in lines:
                if(beginning):
                    if("M900 K0.2" in line):
                        start = True
                else:
                    start = True
                if("; Filament-specific end gcode" in line):
                    finish = True
                    
                if(start == True and finish == False):
                    new_Gcode += line 
           
            f.seek(0)          
            f.write(new_Gcode)
    #Removes the section of gcode where the toio is used as a support when "use toio as a support" is selected
    def support_slicer(self):
        xmin = self.x - 16
        xmax = self.x + 16
        ymin = self.y - 16
        ymax = self.y + 16
        height = 0

        lines = self.file_to_array(self.file)
        with open(self.file, 'w') as f:
            new_Gcode = ""
            for line in lines:
                valx = 0
                valy = 0
               
                
                section = line.split(" ")
                for sec in section:
                    if 'X' in sec:
                        if (len(sec)<10 and ';' not in sec):  
                            valx = float(sec[1:])
                            skip_check = True
                           
                    if 'Y' in sec:  
                        if (len(sec)<10 and ';' not in sec):
                            valy = float(sec[1:])
                            skip_check = True

                    if 'Z' in sec:  
                        if (len(sec)<10 and ';' not in sec):
                            height = float(sec[1:])
                if(height < 26.4):
                    if(valx > xmin and valx < xmax and valy > ymin and valy < ymax):
                        continue
                    else:
                        new_Gcode += line
                else:
                    new_Gcode += line
                    
                            
        
                
                # if(skip_check):
                #     if(valx > xmin and valx <xmax and valy > ymin and valy < ymax):
                #         skip_check = False
                #         print("Skip")
                #         print(line)
                #         print(xmax)
                #         print(xmin)
                #         print(ymax)
                #         print(ymin)
                #         continue
                # else:
                    # skip_check = False
                   
                    

                
            f.seek(0)          
            f.write(new_Gcode)



    #returns file name
    def get_file(self):
        return self.file
    
    #returns array of lines from a gcode file
    def file_to_array(self, file)  -> list:
        with open(file, 'r+') as f:

            Gcode = []           # where the new modified code will be put
            content = f.readlines()  # gcode as a list where each element is a line 

            for line in content: 
                Gcode.append(line)
            return Gcode
    
    