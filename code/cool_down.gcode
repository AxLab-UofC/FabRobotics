 G1 E-1 F2100 ; retract
 G1 Z150.0 F720 ; Move print head up
 G1 X178 Y178 F4200 ; park print head
 G1 Z170.0 F720 ; Move print head further up
 G4 ; wait
 M104 S0 ; turn off temperature
 M140 S0 ; turn off heatbed
 M107 ; turn off fan
 M221 S100 ; reset flow
 M900 K0 ; reset LA
 M84 ; disable motors
 ; max_layer_z = 5
 M73 P100 R0
