G1 X170 F1000
M73 P1 R7
G1 Z0.2 F720
G1 X110 E8 F900
G1 X40 E10 F700
G92 E0

M221 S95 ; set flow
G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
M900 K0.2 ; Filament gcode
M107