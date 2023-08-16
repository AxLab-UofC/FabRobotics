import time
from flask import Flask, jsonify, render_template, request
from events import ToioEvent
import math
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
import math
# from Gcode_event import GCode_Event
from timelineManager import TimelineManager, Bed
timeline = TimelineManager()
files = []

#Tells if the printer has started
global printerStart
printerStart = False

#Tells what the current event printing is
global current
current = ""
global print_form
print_form = ""

#Tells what the print progress is
global progress
global gcode_to_add 
global docks_to_add 
global toios_to_add 
global stuff
stuff = []
gcode_to_add = []
docks_to_add = []
toios_to_add = []
progress = 0.0
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    global progress
    
    
    return render_template("index.html", files = files, events = timeline.get_events(), printerStart = printerStart, toios = timeline.toioMan.names, start = printerStart,  current = current, progress = progress)

@app.route('/toio',methods=['POST', 'GET'])
def toio():
    global progress
    if request.method == 'POST':
        num = request.form.get("num")
        # toios.append(str(num))
        timeline.toioMan.connect(int(num))      
        # toios.append(timeline.toioMan.getStatus(0))    
        return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart,  current = current)

@app.route('/_update', methods = ['GET'])
def update():
    return jsonify(result=time.time(), progress = timeline.printMan.progress(), 
                   num_chunks = timeline.num_chunks(), event_type = timeline.current_type(), 
                   temp1 = timeline.extruder_temp(), temp2 = timeline.bed_temp(), 
                   status = timeline.printMan.Api.get_printer_status(), events=timeline.get_events(), toios=timeline.toioMan.checkStatusAll())

@app.route('/target',methods=['POST', 'GET'])
def target():
    global progress
    timeline.toioMan.target(0,100,100)        
    return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart,  current = current)
    
@app.route('/motor',methods=['POST', 'GET'])
def motor():
    timeline.toioMan.motor(0,50,50,255)        
    return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart,  current = current )
    
#File Uploading, Saves the event into an array of files
@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/finish_toio',methods=['POST', 'GET'])
def finish_toio():
    global print_form
    global gcode_to_add 
    global docks_to_add 
    global toios_to_add 
    global stuff
    # for dock in docks_to_add:
    x = docks_to_add[0][0]
    y = docks_to_add[0][1]
    name = docks_to_add[0][2]
    timeline.modify_dock(x,y, "Print Toio Dock on Bed for " + name) #THIS LINE FOR ADDING DOCK
    for toio in toios_to_add:
        timeline.addEvent(toio)
        # timeline.add_Gcode_event(files[-1], "Print <" + str(files[-1][:len(files[-1])-6]) + "> on Toio", print_form)
        
    if(print_form == "print_on"):
        timeline.add_Gcode_event(files[-1], "Print <" + str(files[-1][:len(files[-1])-6]) + "> on Toio", print_form)
    if(print_form == "support"):
        split_files(stuff[0], stuff[1], stuff[2], stuff[3], stuff[4], stuff[5],stuff[6], stuff[7])
    # elif(print_form == "support"):
        # x = gcode_to_add[0][0]
        # y = gcode_to_add[0][1]
        # split_files(files[-1], x, y)
    print_form = ""
    gcode_to_add = []
    docks_to_add = []
    toios_to_add = []
    return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart)
    
@app.route('/toio_event',methods=['POST', 'GET'])
def toio_event():
    global print_form
    global gcode_to_add 
    global docks_to_add 
    global toios_to_add 
    global stuff
    x_bed = (float(request.form.get("x")))
    y_bed = (float(request.form.get("y")))
    x_diff = ((x_bed-90) *7.2619048)/10
    y_diff = ((y_bed-90) *7.2619048) /10
    x = int(882 + x_diff)
    y = int(358 - y_diff)
    
    name = str(request.form.get("toio"))
    print(name)
    event_name = "Move Toio " + name + "off"
    print(print_form)

    if(print_form == "support"):
        event_name = "Move Toio " + name + " as support"
        print("GOT HERE")
        index = timeline.toioMan.names.index(int(name))
        stuff = [files[-1], x_bed, y_bed, x, y, event_name, "", index]

        # gcode_to_add[0] = 
        

       
       
    #     return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart,path = first_layer_path, toio_vals = toios)
       
    #   event3 = ToioEvent("Second Toio Move in")
    #     event3.addTarget(1, 882, 357+40, 270)
    #     event3.addTarget(1, 920, 357+50, 90)
    #     event3.addTarget(0, 882, 357+40, 270)
    #     event3.addTarget(0, 882, 357+20, 270)
    #     event3.addTarget(0,882,357, 270)
    #     event3.addTarget(1,882,400,180)
    #     event3.addTarget(1,780,430,180)
    #     event3.addMotor(1, 80, 80, 250)
    #     event3.addMotor(1, 80, 80, 250)
    #     self.queue.append(event3) 

    if(print_form == "print_on"):
        docks_to_add.append([x,y, name])
        event_name = "Move Toio " + name + " into dock"
        index = int(timeline.toioMan.names.index(int(name)))
        event = ToioEvent(event_name)
       
        # if(index == 0): #Delete this before haptics
        #     event.addTarget(1, 882, 357+60, 270)
        #     event.addTarget(1, 920, 357+50, 90)
        event.addTarget(index, x, y+40, 270)
        event.addTarget(index, x, y+20, 270)
        event.addTarget(index,x,y, 270)
        event.addMotor(index, 10, 10, 0)
        # if(index == 0):
        #     event.addTarget(1,882,400,180)
        #     event.addTarget(1,780,430,180)
        #     event.addMotor(1, 80, 80, 250)
        #     event.addMotor(1, 80, 80, 250)
        toios_to_add.append(event)
        gcode_to_add.append(files[-1])
        
    else:
        # print(toios)

        index = int(timeline.toioMan.names.index(int(name)))
        event = ToioEvent(event_name)
        event.addTarget(index, x, y+40, 270)
        event.addTarget(index, x, y+20, 270)
        event.addTarget(index,x,y, 270)
        # docks_to_add.append([x,y, name])
        print(event.cmds)
        toios_to_add.append(event)
    print(x)
    print(y)
        
    return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart)

def split_files(file, x_bed, y_bed, x,y, toio_name, event_name, index):
    cut(file)
    lines = timeline.file_to_array(file)
    height = 0
    place = 0
    file1 = []
    file2 = []
    file_name = file[:len(file)-6] + "0"+ ".gcode"
    event_name = "Start Print <" + file_name[:len(file_name)-7] + "> [1/2]"
    # file_name = "Test_this.gcode"
    for line in lines:
        if(height >= 26.4):
            print("Broke at ")
            print(height)
            break
        sections = line.split(" ")
        for sec in sections:
            if 'Z' in sec:  
                if (len(sec)<10 and ';' not in sec):
                    height = float(sec[1:])
                    print(height)
        file1.append(line)
        place = place + 1
    file2 = lines[place:]
    timeline.write_file(file1,file_name)
    timeline.add_Gcode_event(file_name, event_name, "support", x_bed, y_bed)
    event = ToioEvent(toio_name)
    event.addTarget(index, x, y+40, 270)
    event.addTarget(index, x, y+20, 270)
    event.addTarget(index,x,y, 270)
    timeline.addEvent(event)
    file_name = file[:len(file)-6] + "1"+ ".gcode"
    event_name = "Continue Print <" + file_name[:len(file_name)-7] + "> [2/2]"
    timeline.write_file(file2,file_name)
    timeline.add_Gcode_event(file_name, event_name, "driver")
    print("Finished This")

def cut(file):
        
        lines = timeline.file_to_array(file)
        # ;BEFORE_LAYER_CHANGE
        # ; Filament-specific end gcode
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
            # print(new_Gcode)
            f.seek(0)           # set the cursor to the beginning of the file
            f.write(new_Gcode)
    
@app.route('/uploader',methods=['POST', 'GET'])
def uploader():
    global print_form
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        print_form = request.form.get("toio_print")
        files.append(f.filename)
        if(print_form == "normal"):
            timeline.add_Gcode_event(f.filename, "Print <" + str(f.filename[:len(f.filename)-6]) + "> on Bed", print_form)
            print("File Success")
        layers = get_layers(f.filename)
        for i in range(1, len(layers)):
            timeline.addLayer(gcodeToSVG(layers[i]))
        
        # print(first_layer_path)
    return render_template("index.html", files = files, events = timeline.get_events(),printerStart = printerStart, toios = timeline.toioMan.names, start = printerStart,  current = current)

def get_layers(file):
    with open(file, 'r+') as f:
            layers = {}
            layer = []           # where the new modified code will be put
            content = f.readlines()  # gcode as a list where each element is a line 
            start_chunk = False
            end_chunk = False
            place = 0
            for line in content: 
                if(";AFTER_LAYER_CHANGE" in line):
                    start_chunk = True
                    end_chunk = False
                if(";BEFORE_LAYER_CHANGE" in line):
                    start_chunk = False
                    end_chunk = True
                if(start_chunk):
                    layer.append(line)
                if(end_chunk):
                    layers[place] = layer
                    place = place + 1
                    layer = []
                    start_chunk = False
                    end_chunk = False

            return layers
        
@app.route('/printer',methods=['POST', 'GET'])
def printer():
    global progress
    global printerStart
    timeline.start()
    printerStart = True
    return render_template("index.html", files = files, events = timeline.get_events(),printerStart = printerStart, toios = timeline.toioMan.names, start = printerStart,  current = current, progress = progress)

@app.route('/cancel',methods=['POST', 'GET'])
def cancel():
    global printerStart
    printerStart = False
    timeline.clear_Queue()
    timeline.printMan.cancel()
    timeline.add_Gcode_event("cool_down.gcode", "Cool Down", "normal")
    timeline.add_Gcode_event("start_up.gcode", "Start Up", "normal")
    
    return render_template("index.html", files = files, events = timeline.get_events(),printerStart = printerStart, toios = timeline.toioMan.names, start = printerStart, current = current)
    
@app.route('/getsvg')
def getsvg():
    if (len(timeline.svgs) == 0): return jsonify(["M 0 0"])
    else: return jsonify(timeline.svgs)
    
@app.route('/dnd')
def dnd():
    return render_template("dnd.html")

def gcodeToSVG(gcode, sidelength = 250):
    start = True
    svgstr = ""
    for line in gcode:
        if line.startswith("G1"):
            x, y, e = (None, None, False)
            coords = line[len("G1"):-1].split()
            for coord in coords:
                if coord.startswith("E"):
                    e = True
                elif coord.startswith("X"):
                    x = float(coord[1:]) * sidelength / 180
                elif coord.startswith("Y"):
                    y = float(coord[1:]) * sidelength / 180
            if (x != None and y != None):
                if start or not e:
                    svgstr += f"M {x} {y} "
                    start = False
                else:
                    svgstr += f"L {x} {y} "
    return(svgstr)

def background():
    global printerStart
    global current
    global progress
    print("Here")
    print(timeline.current_name())
  


    if(printerStart):

        count = 0
        if(count == 4):
            count = 0
        
                
        elif(timeline.current_print_type() == "normal" or timeline.current_print_type() == "support"):
            if(len(timeline.toioMan.names) > 0 and count == 0):
                place = 0
                for toio in timeline.toioMan.toios:
                    timeline.toioMan.singleTarget(place,(795 + place*30),430,90)
                    place = place +1
            count = count +1
        elif(timeline.current_print_type() == "toio"):
            print("Toios Event")
        
           
            
            
        current = timeline.current_name()
        timeline.execute_next()
        if(timeline.finish_queue()):
            printerStart = False
   


# def foreground():
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(background, 'interval', seconds=2)
    scheduler.start()
    app.run(host='0.0.0.0', port=8000)