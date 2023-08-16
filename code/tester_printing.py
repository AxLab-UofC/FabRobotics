from printer_manager import Print_Manager
from toioManager import ToioManager
from Gcode_event import GCode_Event
# from octoAPI import api
from octoprint_cli import *
from octocontrol import OctoprintAPI
import time
from timelineManager import TimelineManager

t = ToioManager()
t.connect(163)

while True:
    print(t.getStatusAll())

# Ax = Print_Manager()
# Ax.move_extruder()
# while(True):
#     print(Ax.getStatus(0))
# while(True):
    # time.sleep(1)
# Ax.target(0,136,535,180)
# Ax.target(0,111,536,180)
# Ax.motor(0,100,100,10)
# if __name__ == "__main__":
#     with open("best_test.gcode", 'r+') as f:
#             layers = {}
#             layer = []           # where the new modified code will be put
#             content = f.readlines()  # gcode as a list where each element is a line 
#             start_chunk = False
#             end_chunk = False
#             place = 0
#             for line in content: 
#                 if(";AFTER_LAYER_CHANGE" in line):
#                     start_chunk = True
#                     end_chunk = False
#                 if(";BEFORE_LAYER_CHANGE" in line):
#                     start_chunk = False
#                     end_chunk = True
#                 if(start_chunk):
#                     layer.append(line)
#                 if(end_chunk):
#                     layers[place] = layer
#                     place = place + 1
#                     layer = []
#                     start_chunk = False
#                     end_chunk = False
        
#             print(layers[1])
#     # Ax = Timeline_Manager()
    # Ax2 = Print_Manager()
    # # Ax2.cool_down()
    # # # Ax2.cancel()
    # # #Ax.add_Gcode_event("start_up.gcode", "start_up")
    # # Ax.add_Gcode_event("best_test.gcode", "moves")
    # #Ax.add_Gcode_event("cool_down.gcode", "cool_down")
    # # print(Ax.get_events_names())
    # # # #print(Ax.get_events())
    # Ax.start()
    # # # # print(len(Ax.get_events()))
    # # # # print(Ax.place)
    # while(not Ax.finish_queue()):
    #     print(Ax2.progress())
        
    #     if(Ax2.finished()):
    #         print("Sleeping")
    #         time.sleep(2)
    #         print("Got here")
    #         Ax.execute_next()
    #         print(Ax.current_name())
            
    
    # Ax = octoprint_cli("http://axlab.local", "F5EFDBD8F3AB4C03B8C690B0F6917702")
    # Ax = OctoprintAPI("axlab.local/", "", "F5EFDBD8F3AB4C03B8C690B0F6917702")
    # Ax.connect_to_printer()
    # print(Ax.is_printer_connected())
    # # even = GCode_Event("test.gcode")
    # # Ax2 = Print_Manager()
    # # Ax2.start_up()
    # # Ax2.print_event(even)
    # # Ax2.cool_down()
    # Ax.cancel_job()
    # # Ax2.cool_down()
    # Ax.fileUpload("Gcode/start_up.gcode")
    # Ax.select_file("start_up.gcode")
    # print("Success")
    # print(Ax.get_file_printing())
    # print(Ax.get_print_time_left())
    # print(Ax.get_total_print_time())
    # print(Ax.get_print_progress())
    # while(Ax.get_print_progress() < 100):
    #     print(Ax.get_print_time_left())
    #     print(Ax.get_total_print_time())
    #     print(Ax.get_print_progress())
    #     time.sleep(5)
    # print("Done!")
    # print(Ax.getVersionInfo())
    # Ax.fileUpload("Gcode/start_up.gcode")
    # 
    # # print(even.Gcode)
    # # dock = GCode_Event("Gcode/tester_print.gcode")
    # Ax.connect_printer()
    # # Ax.move_extruder(30)
    # # # # Ax.delay(10000)

    
    # # Ax.start_up()
    # # # # # Ax.print_dock()
    
    # # # # # Ax.delay(30000)
    # #print(even.Gcode)
    # # even.get_Gcode()
    # Ax.print_event(even)
    # #Ax.print_dock(280, 400)
    # # # Ax.purge()
    # Ax.cool_down()

   
    
