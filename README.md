**Abstract**

We present FabRobotics, a digital fabrication pipeline that combines traditional 3D printing with mobile robots. By integrating these
two technologies, we aim to create new opportunities for 3D printers to fabricate objects quickly and efficiently, and for mobile robots
to enhance their adaptability and interactivity. To explore this novel research opportunity, we have developed a proof-of-concept
implementation pipeline, allowing users to execute hybrid turn-taking control of a 3D printer and mobile robots to autonomously
3D print objects on/with mobile robots. The system was implemented with commercially available 3D printers (Prusa MINI) and
mobile robots (toio), and we share various techniques and knowledge specific to fusing 3D printers and mobile robots (e.g., printing
mobile robot docks for stable prints on robots). Based on the proof-of-concept system, we demonstrate various application usages and
functionalities, showcasing how 3D printing and mobile robots can mutually advance each other for novel fabrication and interaction.
Lastly, we share our further exploration of extended prototypes (e.g., fusing two printers) and discuss future technical challenges and
research opportunities.

**How to set up**

To set up FabRobotics you need a few things:
- any 3D printer
- 2 Raspberry Pis(We used 2 Raspberry Pi 4 Model B)
- Toio Robots

Set up the first Pi with OctoPi Software and adjust to the print settings of your specific printer. The info for all of this can be found online. We found this link helpful: https://www.raspberrypi.com/tutorials/set-up-raspberry-pi-octoprint/#:~:text=Set%20up%20OctoPrint,details%20of%20your%203D%20printer.

Clone this Repo onto the second Raspberry Pi. And install all libraries used.
Note: Make sure that you change the API Key and local address to those from your Octoprint instance. You will also need to get the mac address of your toio robots to be able to connect to them. 

Good luck! Feel free to reach out to jmlindstrom14@gmail or "RAMARKOS EMAIL" with any questions.

**Software Architecture Explained**

**Server and GUI:**
Our front-end is hosted on a Flask Server, which presents a UI that regularly receives updates from the 3D printer manager and toio manager about the status of the 3D printer, toios, and the print progress. During the Planning Phase, user input is sent to the timeline manager, where it is processed, and new events are generated and added to the timeline on the GUI. During the Execution Phase, the timeline on the GUI presents the live completion and progress of events.

**Timeline Manager:**
The timeline manager is one of the core technical contributions in FabRobotics, enabling turn-taking control between the toio robots and 3D printer. The timeline manager is comprised of two major components: the timeline generator and and timeline executor. Based on user input, the timeline generator then processes uploaded G-code and the placement of toios into print event(s) and toio event(s). The timeline generator will also automatically add events as necessary, such as placing docks for toios, as well as starting up and cooling down the printer. The timeline executor will then take the list of events and execute them one-by-one through turn-taking, allowing for seamless integration of toio and printer control. Print and toio events are handed off to their respective manager, and the timeline executor will wait for the completion of the previous command before the execution of the next command.

**Toio Manager:**
The toio manager is responsible for constructing and executing toio events, allowing for the control of toio robots during the entirety of the printing process. It manages toio movements on and off the print-bed and enables precise navigation of toios to the selected locations from the Planning Phase. Our toio manager is implemented through the usage of the bluepy library, which allows for communication with BTLE (Bluetooth Low Energy) Devices. By sending and receiving Bluetooth commands, we can directly control each connected toio's position, motor speed, as well as monitor their current battery.

**Print Manager and OctoPrint:**
The 3D printer manager handles the execution, modification, and monitoring of G-code on the printer. Through the OctoPrint API, The print manager can wirelessly upload, start, and cancel prints. However, our implementation of communication through the OctoPrint API has a limitation of only allowing G-code files of a length shorter than 2000 lines to be uploaded. To account for this, a G-code event is segmented into smaller files when uploaded files are processed. The 3D printer manager also processes prints for required edits when printing while using toios as a bed or as supports. When using toios as beds, the 3D printer manager will add a toio dock event, as well as edit the uploaded G-code file(s) to raise the entire print to the height of the toio. When using toios as supports, the 3D printer manager will remove all G-codes that would intersect with a toio, and splits the print in two to allow the toio to move into position when it can begin acting as a support.


**Potential Issues and notes for future users:**
- Docks code could be improved upon, our dock worked well for driving the toio in but could have provided
better support. To change the dock design simply replace "dock.gcode" with a new file. It must be named the same
    - This caused issues with the first layer getting down
    - toio didnt always consistantly drive into the dock

- Continous multiprint: This code had alot of points of error with the toio colliding. The code we used is at the bottom of the timeline manager commented out. If you plan on implementing this there are a few things to remember to change:
    - The toio are supposed to be constantly targeting the corner, a function set in the background scheduler in server.py. This would need to be changed to avoid the toio you are printing on targeting back to the corner.
    - Under finish toio in server.py you need to ensure that it will only attempt to print 1 dock and queue multiple prints. It is configured right now to add multiple docks for multiple toio for a single print such as our grippers.

-Bed: If the bed changes alot of coordinates need to be changed to make things work. Most of our coordinate mapping is based around the center. Our background checker targets the top left corner and same for driving down the ramp. Make sure you look thouroughly through server , printer Manager, toio Manager, events, and timeline manager to ensure all the hardcoded coordinates are changed.

-File storage: Given our time crunch we did not implement a file storage system. When we were attempting to have a folder for it octoprint then had trouble finding it.

-Adding a new printer: Make sure under timeline manager you change the key and location for octoprint if you are using a different raspberry pi. You should be able to add a second printer api through timeline manager but this has not been tested. Just create another instance of octocontrol with the new printers address and API key.


