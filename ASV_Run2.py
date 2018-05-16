import ASV_Functions as F
import ASV_Parameters as P
#import comm3 as C
# Is motion a defined function, or the overall programme?!
# I think this should be the basic programme, with interuptions for detecting a different number of ASVs:
# will this method of lots of if statements mean that the thrusters are constantly switching on and off be bad for them?
# maybe don't turn them completely of, keep them running at a very low value that doesn't generate much thrust?


## Start programme:
def main():
    while True:
    # as soon as you've run the distance allocation once, main bulk of programme starts and runs indefinitely
    # to position the ASV and re-assign positions depending on the number of currently active ASVs
    # when the active ASVs changes, run the position allocation again:
        ASV_Data = F.get_Communication_Data()
        if len(ASV_Data) > 1:
         F.Initial_Setup() # runs programme for 1 or 2 ASVs to initially find object and its centre
    
        ASV_Data = F.get_Communication_Data()
        ASV_Positions = P.Position_Allocation(ASV_Data, Object_Centre)
        Req_Angle = ASV_Positions.index(F.My_Data[0])
        while(change < 5): ## time lapse on so that it doesn't just stop immediately in case communication is just a bit patchy - but make sure the rest of the code still runs as normal
            My_Coords = F.get_Coords()
            Object_Centre = F.get_Object_Centre()
            Current_Angle = F.get_Current_Angle(My_Coords, Object_Centre)
        ## only want to move the the right if facing the object
            if Current_Angle > (Req_Angle + 2): # -2 for filter / not too much moving?
                TiS = P.Thruster_Values(LDM = 90, Speed_PC=1) # move to the right
                # Assign to thrusters
            elif Current_Angle < (Req_Angle - 2):
                TiS = P.Thruster_Values(LDM = -90, Speed_PC=1) # move to the left
            # Assign to thrusters

            Camera_Dist = get_Camera_Distance()  ## if this can't be found because the ASV isn't facing the object
            if Camera_Dist > max(P.Req_Dist_Range):
                TiS = P.Thruster_Values(LDM = 0, Speed_PC=1) # move forwards
            # Assign to thrusters
            elif Camera_Dist < min(P.Req_Dist_Range):
                TiS = P.Thruster_Values(LDM = 180, Speed_PC=1) # move backwards
            # Assign to thrusters

        #if object to left of screen:
            #P_C.turnLeft(0.5)
        #elif not seen but last seen to the left:
            #P_C.turnLeft(1)
        #elif object to right of screen:
            #P_C.turnRight(0.5)
        #elif not seen but last seen to the right:
            #P_C.turnLeft(1)
        
            Communicate_Data()
            New_online = get_online()
            if New_online == online:
                change = 0
            if New_online != online:
                change +=1

#main()