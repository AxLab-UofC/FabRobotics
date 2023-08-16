from typing import Union
from coreCube import CoreCube
from Constants import toioADDR
from time import sleep
from events import ToioEvent
import bluepy
import time

#Class for managing all toio connected to Fabrobotics
class ToioManager:
    def __init__(self) -> None:
        self.toios = []
        self.names = []

    #connect a toio by number, or mac_address
    def connect(self, addr: Union[str, int]) -> None:
        toio = CoreCube()
        if (type(addr) == int):
            toio.connect(toioADDR[addr], bluepy.btle.ADDR_TYPE_RANDOM)
        if (type(addr) == str):
            toio.connect(addr, bluepy.btle.ADDR_TYPE_RANDOM)
        toio.id()
        toio.battery()
        self.toios.append(toio)
        self.names.append(addr)

    #returns status of a single indexed toio
    def getStatus(self, index:int, update:bool=False) -> dict:
        toio = self.toios[index]
        if update:
            toio.battery()
            toio.id()
        return {"x": toio.x, "y": toio.y, "dir": toio.dir, "battery": toio.batt}

    #Returns list of status for all toio connected
    def getStatusAll(self):
        status = []
        for toio in self.toios:
            try:
                toio.battery()
                toio.id()
                status.append({"x": toio.x, "y": toio.y, "dir": toio.dir, "battery": toio.batt})
            except:
                continue  
        return status
    
    #Used to update status on fabrobotics front end
    def checkStatusAll(self):
        status = []
        for (i, toio) in enumerate(self.toios):
            status.append({"name": self.names[i], "x": toio.x, "y": toio.y, "dir": toio.dir, "battery": toio.batt})
        return status
    
    #Updates list of toio status
    def update(self, id: Union[int, None] = None) -> None:
        if (type(id) == int):
            self.toios[id].battery()
            self.toios[id].id()
        else:
            for toio in self.toios:
                try:
                    toio.battery()
                    toio.id()
                except:
                    continue

    #command for targeting toio
    def target(self, index: int, x:int, y:int, theta:int = 0):
        toio = self.toios[index]
        # while True:
        print("attempting " + str(x) + ", " + str(y))
        loc = self.getStatus(index, True)
           
        tol = 10
        print(loc)
        toio.motorToTarget(0, 0, 0, 80, 3, x, y, theta)
        time.sleep(2)
            # if (loc["x"] < x + tol) and (loc["x"] > x - tol) and (loc["y"] < y + tol) and (loc["y"] > y - tol):
            #     break
            #Note: comments above were used to continously check toio location and make sure it was within tolerance.
            #Commented out because it caused some issues with taking too long and timeing out our background scheduler
        print("Done!")

    #Does a single target
    def singleTarget(self, index: int, x:int, y:int, theta:int = 0):
        toio = self.toios[index]
        loc = self.getStatus(index)
        toio.motorToTarget(0, 0, 0, 80, 3, x, y, theta)
        toio.id()
        print("Done!")

    #Sets motor speed
    def motor(self, index: int, leftspeed: int, rightspeed: int, duration: int) -> None:
        toio = self.toios[index]
        toio.id()
        toio.motor([leftspeed, rightspeed], duration)
        toio.id()

    #Runs through list of cmds in a toio event and runs them all chronologically.
    def execute(self, event:ToioEvent) -> None:
        for cmd in event.cmds:
            if (cmd[0] == "c"): self.connect(cmd[1])
            elif (cmd[0] == "t"): self.target(cmd[1], cmd[2], cmd[3], cmd[4])
            elif (cmd[0] == "m"): self.motor(cmd[1], cmd[2], cmd[3], cmd[4])
