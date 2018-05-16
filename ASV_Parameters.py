import numpy as np

My_Name = 1

coord = [10,45]

## ESC values:
ESC_Fwd_Max = 2500*4 ## = value assigned to ESC for max forward speed
ESC_Fwd_Min = 1510*4 ## = value assigned to ESC for min forward speed
ESC_Rev_Max = 500*4 ## = value assigned to ESC for max reverse speed
ESC_Rev_Min = 1490*4 ## = value assigned to ESC for min reverse speed
ESC_Stop = 1500*4
T_Cut_Off = 0.1 ## value range around 0 that don't bother turning on at all as close to 0

## 3 thrusters:
## T1 at n (0) facing e (90)
## T2 at se (120) facing nne (210)
## T3 at sw (240) facing ssw (330)
D1 = 69.49      ## distance of T1 from centre of foam
D2 = 103.21     ## distance of T3 from centre of foam
D3 = 103.21     ## distance of T3 from centre of foam
Theta = np.radians(30)	## angle of T2 & T3 from n

Req_Dist_Range = [0.9, 1.1] ## acceptable range of distance from the object as measured by the laser and camera