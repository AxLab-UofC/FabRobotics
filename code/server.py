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
global files
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
global supports_to_add
global support_vals 
supports_to_add = {"fh": None, "x": [], "y": [], "x_bed": [], "y_bed": [], "index": []}

stuff = []
gcode_to_add = []
docks_to_add = []
toios_to_add = []
progress = 0.0
app = Flask(__name__)

@app.route('/')
@app.route('/home')

#Home route
def home():
    global files
    global progress
    return render_template("index.html", files = files, events = timeline.get_events(), printerStart = printerStart, toios = timeline.toioMan.names, start = printerStart,  current = current, progress = progress)

#Route for adding toio
@app.route('/toio',methods=['POST', 'GET'])
def toio():
    global files
    global progress
    if request.method == 'POST':
        num = request.form.get("num")
        timeline.toioMan.connect(int(num))      
        return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart,  current = current)

#Route for updating jsonify values for dyanmic updates
@app.route('/_update', methods = ['GET'])
def update():
    return jsonify(result=time.time(), progress = timeline.printMan.progress(), 
                   num_chunks = timeline.num_chunks(), event_type = timeline.current_type(), 
                   temp1 = timeline.extruder_temp(), temp2 = timeline.bed_temp(), 
                   status = timeline.printMan.Api.get_printer_status(), events=timeline.get_events(), toios=timeline.toioMan.checkStatusAll())

#route for target testing, not used in final
@app.route('/target',methods=['POST', 'GET'])
def target():
    global files
    global progress
    timeline.toioMan.target(0,100,100)        
    return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart,  current = current)

#route for motor testing, not used in final
@app.route('/motor',methods=['POST', 'GET'])
def motor():
    global files
    timeline.toioMan.motor(0,50,50,255)        
    return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart,  current = current )
    
#File Uploading, Saves the event into an array of files
@app.route('/upload')
def upload_file():
   
   return render_template('upload.html')

#Finish placing toio buttons, adds the events based on configurations
@app.route('/finish_toio',methods=['POST', 'GET'])
def finish_toio():
    global files
    global print_form
    global gcode_to_add 
    global docks_to_add 
    global toios_to_add 
    global supports_to_add
    global stuff
    if (print_form == "support"):
        split_files(supports_to_add)
    else:
        for dock in docks_to_add:
            x = dock[0]
            y = dock[1]
            name = dock[2]
            timeline.modify_dock(x,y, "Print Toio Dock on Bed for " + name) #THIS LINE FOR ADDING DOCK
        for toio in toios_to_add:
            timeline.addEvent(toio)
            
        if(print_form == "print_on"):
            timeline.add_Gcode_event(files[-1], "Print <" + str(files[-1][:len(files[-1])-6]) + "> on Toio", print_form)
            timeline.addMotorDownRamp()
    #reset variables
    print_form = ""
    gcode_to_add = []
    docks_to_add = []
    toios_to_add = []
    return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart)

#Button for confirming a toio placement, adds appropriate docks and toio events to
#docks to add and toios to add
@app.route('/toio_event',methods=['POST', 'GET'])
def toio_event():
    global files
    global print_form
    global gcode_to_add 
    global docks_to_add 
    global toios_to_add 
    global support_vals
    #calculations for converting the inputted coordinates in mm on the front
    #end to toio coordinates for targeting
    x_bed = (float(request.form.get("x")))
    y_bed = (float(request.form.get("y")))
    x_diff = ((x_bed-90) *7.2619048)/10
    y_diff = ((y_bed-90) *7.2619048) /10
    x = int(882 + x_diff)
    y = int(358 - y_diff)
    
    name = str(request.form.get("toio"))
    event_name = "Move Toio " + name

    if(print_form == "support"):
        event_name = "Move Toio " + name + " as support"
        print("GOT HERE")
        index = timeline.toioMan.names.index(int(name))
        supports_to_add["fh"] = files[-1]
        supports_to_add["x"].append(x)
        supports_to_add["y"].append(y)
        supports_to_add["x_bed"].append(x_bed)
        supports_to_add["y_bed"].append(y_bed)
        supports_to_add["index"].append(index)

        support_vals = [files[-1], x_bed, y_bed, x, y, event_name, "", index]


    if(print_form == "print_on"):
        docks_to_add.append([x,y, name])
        event_name = "Move Toio " + name + " into dock"
        index = int(timeline.toioMan.names.index(int(name)))
        event = ToioEvent(event_name)
        event.addTarget(index, x, y+40, 270)
        event.addTarget(index, x, y+20, 270)
        event.addTarget(index,x,y, 270)
        event.addMotor(index, 10, 10, 0)
        toios_to_add.append(event) #motor into dock based on x,y placement
        gcode_to_add.append(files[-1]) #adds most recent file
        
    else:
        index = int(timeline.toioMan.names.index(int(name)))
        event = ToioEvent(event_name)
        event.addTarget(index, x, y+40, 270)
        event.addTarget(index, x, y+20, 270)
        event.addTarget(index,x,y, 270)
        toios_to_add.append(event)
        
    return render_template('index.html', files = files, events = timeline.get_events(), printerStart = printerStart,  toios = timeline.toioMan.names, start = printerStart)


#works the same as the one in events, will cut the files start up and cool down out
def cut(file):
    global files
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


#used for supports, will split the file into 2 files
#name0 and name1 with name0 being the bottom half up until the height of the toio
#and name1 being everything above the height of the toio
#file, x_bed, y_bed, x,y, toio_name, event_name, index
#fh, x_bed, y_bed, x, y, index
#{"fh": None, "x": [], "y": [], "x_bed": [], "y_bed": [], "index": []}
def split_files(dc):
    global files
    fh = dc["fh"]
    cut(fh)
    lines = timeline.file_to_array(fh)
    height = 0
    place = 0
    file1 = []
    file2 = []
    file_name = fh[:len(fh)-6] + "0"+ ".gcode"
    event_name = "Start Print <" + file_name[:len(file_name)-7] + "> [1/2]"
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
    timeline.add_Gcode_event(file_name, event_name, "support", dc["x_bed"], dc["y_bed"])
    for (i, _) in enumerate(dc["x"]):
        (index, x, y) = (dc["index"][i], dc["x"][i], dc["y"][i])
        event = ToioEvent("Move toio" +  str(index) + " as support")
        event.addTarget(index, x, y + 40, 270)
        event.addTarget(index, x, y + 20, 270)
        event.addTarget(index, x, y, 270)
        timeline.addEvent(event)
    file_name = fh[:len(fh)-6] + "1"+ ".gcode"
    event_name = "Continue Print <" + file_name[:len(file_name)-7] + "> [2/2]"
    timeline.write_file(file2,file_name)
    timeline.add_Gcode_event(file_name, event_name, "driver")
    print("Finished This")

#Upload files route, will add the name to files and generate layer visualzation 
@app.route('/uploader',methods=['POST', 'GET'])
def uploader():
    global files
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

#Used to get individual layers of gcode for layer visualization
def get_layers(file):
    global files
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

#route for starting the print   
@app.route('/printer',methods=['POST', 'GET'])
def printer():
    global progress
    global files
    global printerStart
    timeline.start()
    printerStart = True
    return render_template("index.html", files = files, events = timeline.get_events(),printerStart = printerStart, toios = timeline.toioMan.names, start = printerStart,  current = current, progress = progress)

#route for canceling the print, Note to ramarko, I am not sure how to clear the svg file generation or reset the timeline javascript
@app.route('/cancel',methods=['POST', 'GET'])
def cancel():
    global files
    global printerStart
    printerStart = False
    timeline.reset()
    timeline.printMan.cancel()
    files = []
   
    return render_template("index.html", files = files, events = timeline.get_events(),printerStart = printerStart, toios = timeline.toioMan.names, start = printerStart, current = current)

#gets svgs from timeline
@app.route('/getsvg')
def getsvg():
    if (len(timeline.svgs) == 0): return jsonify(["M 0 0"])
    else: return jsonify(timeline.svgs)

#was used for our DND demo in final video
@app.route('/dnd')
def dnd():
    return render_template("dnd.html")

#Converts gcode layers to svgs
def gcodeToSVG(gcode, sidelength = 250):
    global files
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

#Background scheduler, all of this runs in the background without interfereing with interaction with the front end
#Note: Anything put here needs to take less than the time it takes for this scheduler to run through or it will crash
def background():
    global printerStart
    global current
    global progress
    global files
   

    if(printerStart):
        count = 0
        if(count == 4):
            count = 0
        #Constantly targets corner of bed to stay out of the way of extruder.
        elif(timeline.current_print_type() == "normal" or timeline.current_print_type() == "support"):
            if(len(timeline.toioMan.names) > 0 and count == 0):
                place = 0
                for toio in timeline.toioMan.toios:
                    timeline.toioMan.singleTarget(place,(795 + place*30),430,90)
                    place = place +1
            count = count +1
      
        #Constantly trying to execute the next event when the one before it is finished  
        current = timeline.current_name()
        timeline.execute_next()
        if(timeline.finish_queue()):
            printerStart = False
   



if __name__ == "__main__":
    #initializes scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(background, 'interval', seconds=2)
    scheduler.start()
    #run app
    app.run(host='0.0.0.0', port=8000)