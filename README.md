Fabrobotics is an app created by Jonathan Lindstrom and Ramarko Bhattacharya

It is a digital Fabrication pipeline that is used to control 3D printer and toio robots in sync.

Currently our app is capable of printing one print on one or two toio(theroretically three but hasnt been tested), using the toio as a support, and printing regularly. 

lindstromhci@gmail.com
ramarkob@uchicago.edu


Potential Issues and notes for future users:
- Docks code could be improved upon, our dock worked well for driving the toio in but could have provided
better support. To change the dock design simply replace "dock.gcode" with a new file. It must be named the same
    - This caused issues with the first layer getting down
    - toio didnt always consistantly drive into the dock

- Continous multiprint: This code had alot of points of error with the toio colliding. The code we used is at the bottom of the timeline manager commented out. If you plan on implementing this there are a few things to remember to change:
    - The toio are supposed to be constantly targeting the corner, a function set in the background scheduler in server.py. This would need to be changed to avoid the toio you are printing on targeting back to the corner.
    - Under finish toio in server.py you need to ensure that it will only attempt to print 1 dock and queue multiple prints. It is configured right now to add multiple docks for multiple toio for a single print such as our grippers.

- Bed: If the bed changes alot of coordinates need to be changed to make things work. Most of our coordinate mapping is based around the center. Our background checker targets the top left corner and same for driving down the ramp. Make sure you look thouroughly through server , printer Manager, toio Manager, events, and timeline manager to ensure all the hardcoded coordinates are changed.

- File storage: Given our time crunch we did not implement a file storage system. When we were attempting to have a folder for it octoprint then had trouble finding it.

- Adding a new printer: Make sure under timeline manager you change the key and location for octoprint if you are using a different raspberry pi. You should be able to add a second printer api through timeline manager but this has not been tested. Just create another instance of octocontrol with the new printers address and API key.






