G1 X89.891 Y89.441 E.00734
G1 X89.709 Y89.509 E.0079
G1 X89.628 Y89.568 E.00405
G1 X90.428 Y90.368 E.04594
G1 X90.267 Y90.506 E.00863
G1 X90.069 Y90.568 E.00841
G1 X89.962 Y90.57 E.00435
G1 X89.935 Y90.566 E.00111
G1 X89.258 Y89.888 E.03892
; stop printing object Body1.stl id:0 copy 0
;LAYER_CHANGE
;Z:22
;HEIGHT:0.200001
;BEFORE_LAYER_CHANGE
G92 E0.0
;22


G1 E-2.24 F4200
;WIPE_START
G1 F7200
G1 X89.935 Y90.566 E-.53101
G1 X89.962 Y90.57 E-.01515
G1 X90.069 Y90.568 E-.05935
G1 X90.267 Y90.506 E-.11475
G1 X90.428 Y90.368 E-.11769
G1 X90.333 Y90.273 E-.07405
;WIPE_END
G1 E-.048 F4200
G1 Z22 F720
;AFTER_LAYER_CHANGE
;22
; printing object Body1.stl id:0 copy 0
G1 X90.196 Y90.135 F9000
G1 E3.2 F2400
M204 P800
;TYPE:Perimeter
;WIDTH:0.45
G1 F900
G1 X90.14 Y90.19 E.00265
G1 X90.021 Y90.234 E.00428
G1 X89.89 Y90.205 E.00457
G1 X89.815 Y90.144 E.00325
G1 X89.776 Y90.065 E.00298
G1 X89.767 Y89.978 E.00298
G1 X89.792 Y89.893 E.00298
G1 X89.846 Y89.824 E.00298
G1 X89.921 Y89.779 E.00298
G1 X90.021 Y89.767 E.0034
G1 X90.114 Y89.792 E.00325
G1 X90.182 Y89.847 E.00298
G1 X90.225 Y89.924 E.00298
G1 X90.238 Y90.011 E.00298
G1 X90.222 Y90.082 E.00244
M204 P1000
G1 X90.495 Y90.411 F9000
M204 P800
;TYPE:External perimeter
G1 F900
G1 X90.361 Y90.535 E.00618
G1 X90.221 Y90.605 E.00531
G1 X90.075 Y90.64 E.00509
G1 X89.841 Y90.624 E.00792
G1 X89.695 Y90.565 E.00532
G1 X89.572 Y90.48 E.00509
G1 X89.427 Y90.291 E.00804
G1 X89.36 Y90.06 E.00814
G1 X89.383 Y89.821 E.00814
G1 X89.492 Y89.607 E.00814
G1 X89.671 Y89.447 E.00814
G1 X89.894 Y89.365 E.00802
G1 X90.051 Y89.359 E.00532
G1 X90.198 Y89.386 E.00509
G1 X90.408 Y89.499 E.00804
G1 X90.563 Y89.682 E.00814
G1 X90.641 Y89.91 E.00814
G1 X90.629 Y90.15 E.00814
G1 X90.533 Y90.364 E.00796
M204 P1000
G1 X90.314 Y90.389 F9000
; stop printing object Body1.stl id:0 copy 0
G1 E-2.24 F4200
;WIPE_START
G1 F7200;_WIPE
G1 X90.361 Y90.535 E-.13417
G1 F7200;_WIPE
G1 X90.221 Y90.605 E-.08701
G1 F7200;_WIPE
G1 X90.075 Y90.64 E-.0834
G1 F7200;_WIPE
G1 X89.841 Y90.624 E-.12971
G1 F7200;_WIPE
G1 X89.695 Y90.565 E-.08702
G1 F7200;_WIPE
G1 X89.572 Y90.48 E-.0834
G1 F7200;_WIPE
G1 X89.427 Y90.291 E-.13159
G1 F7200;_WIPE
G1 X89.36 Y90.06 E-.13323
G1 F7200;_WIPE
G1 X89.368 Y89.984 E-.04247
;WIPE_END
G1 E-.048 F4200
G1 Z22.2 F720
M107
;TYPE:Custom
