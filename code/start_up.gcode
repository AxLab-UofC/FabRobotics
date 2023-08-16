M73 P0 R12
M201 X2500 Y2500 Z400 E5000 ; sets maximum accelerations, mm/sec^2
M203 X180 Y180 Z12 E80 ; sets maximum feedrates, mm / sec
M204 P1250 R1250 T2500 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X8.00 Y8.00 Z2.00 E10.00 ; sets the jerk limits, mm/sec
M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec
M107
;TYPE:Custom
M862.3 P "MINI" ; printer model check
G90 ; use absolute coordinates
M83 ; extruder relative mode
M104 S170 ; set extruder temp for bed leveling
M140 S60 ; set bed temp
M109 R170 ; wait for bed leveling temp
M190 S60 ; wait for bed temp
M204 T1250 ; set travel acceleration
G28 ; home all without mesh bed level
G29 ; mesh bed leveling 
M204 T2500 ; restore travel acceleration
M104 S215 ; set extruder temp
G92 E0
G1 Y-2 X179 F2400
G1 Z3 F720
M109 S215 ; wait for extruder temp

; intro line
G1 X170 F1000
G1 Z0.2 F720
G1 X110 E8 F900
G1 X40 E10 F700
G92 E0

M221 S95 ; set flow
G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
M900 K0.2 ; Filament gcode LA 1.5
; ; Filament gcode LA 1.0
M107
;LAYER_CHANGE
;Z:0.2
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0.0
;0.2