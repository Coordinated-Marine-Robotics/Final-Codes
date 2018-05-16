## Minimises maximum angle traveled by all ASVs when getting into position
## Allocates each position its closest ASV, considering the positions in order from the furthest from an ASV to the closest
## This list is updated every time a position is allocated its ASV
## Includes a clause that makes sure no ASVs cross paths
import numpy as np

## ASV_Data = [[Name, [Coordinates], camera distance]]
def Position_Allocation(ASV_Data, Object_Centre):
	ASV_Angles_from_Positions = [[number, []] for number in range(0, len(ASV_Data))]
	for ASV in ASV_Data:
		ASV.append(np.degrees(np.arctan2((ASV[1][0]-Object_Centre[0]),((ASV[1][1]-Object_Centre[1]))))) # angle from centre
		ASV.append([])
		for i in range(len(ASV_Data)):
			angle = ASV[3]-(i*360//len(ASV_Data))
			if abs(angle) > 180:
				angle = angle + 360
			ASV[4].append(angle)
			ASV_Angles_from_Positions[i][1].append(abs(angle))
		ASV.append(ASV[4].index(min(a for a in ASV[4] if a>=0)))
		ASV.append(ASV[4].index(max(a for a in ASV[4] if a<=0)))
	## ASV_Data is now a list of lists [ASV's name, coordinates, distance from camera, angle from centre, [angles from positions], closest anti-clockwise position, closest clockwise position]
	## ASV_Angles_from_Positions is a list of list [position number, [angle of each ASV from that position]]
	ASV_Pos_Inc_Angle = sorted(ASV_Angles_from_Positions, key=lambda Position:min(Position[1]), reverse=True)
	## ASV_Pos_Inc_Angle is ASV_Angles_from_Positions sorted in descending order of the minimum distances
	ASV_Allocation = ['x' for number in range(0, len(ASV_Data))]
	while 'x' in ASV_Allocation:
		i = ASV_Pos_Inc_Angle.pop(0) ## Position to be filled
		minIndex = i[1].index(min(i[1])) ## it's closest ASV
		
		#if there is an occupied position between the closest ASV's angle and the angle of the position it's going to:
			#swap the ASVs
		Crossing_Positions = [] ## a list of the position numbers that the ASV will be passing through to get to its intended position. the final intended position should be the final item in this list
		if ASV_Data[minIndex][4][i[0]] > 0: ## ASV will travel anti-clockwise
			cross_pos = ASV_Data[minIndex][5]
			while ASV_Angles_from_Positions[cross_pos] != i:
				Crossing_Positions.append(cross_pos)
				cross_pos -= 1
				if cross_pos < 0:
					cross_pos = len(ASV_Data)-1
		elif ASV_Data[minIndex][4][i[0]] < 0: ## ASV will travel clockwise
			cross_pos = ASV_Data[minIndex][6]
			while ASV_Angles_from_Positions[cross_pos] != i:
				Crossing_Positions.append(cross_pos)
				cross_pos += 1
				if cross_pos > len(ASV_Data)-1:
					cross_pos = 0
		Crossing_Positions.append(i[0])
			
		for cp in Crossing_Positions:
			if ASV_Allocation[cp] != 'x' and cp != i[0]:
				Crossed_ASV = ASV_Allocation[cp]
				ASV_Allocation[cp] = ASV_Data[minIndex][0]
				if ASV_Allocation[Crossing_Positions[Crossing_Positions.index(cp)+1]] == 'x':
					ASV_Allocation[Crossing_Positions[Crossing_Positions.index(cp)+1]] = Crossed_ASV
				else:
					print('help me, I have broken! I want to shuffle again but the code will not let me!')
					## I'm 99% certain it will only ever try to shuffle 1 ASV, but just in case it tries more I've added an error message
					
		if ASV_Allocation[i[0]] == 'x':
			ASV_Allocation[i[0]] = ASV_Data[minIndex][0] ## If it hasn't already done a swap (ie. not crossed any occupied positions) allocate the position its closest ASV
		for  p in ASV_Pos_Inc_Angle:
			p[1][minIndex] = max(p[1]) + 1 ## Make all the distances for the ASV that's just been allocated larger than their maximums
		ASV_Pos_Inc_Angle = sorted(ASV_Pos_Inc_Angle, key=lambda Position:min(Position[1]), reverse=True)
	return(ASV_Allocation) ## ASV_Allocation = List of ASV names where index = allocated position 