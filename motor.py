import ASV_Functions as F
import ASV_Parameters as P
import numpy as np
#import laser2
import maestro 
import time,sys,tty,termios
#import tracking as T
#hello

#get_Camera_Distance = F.get_Camera_Distance()

max_value = 2000*4 #maximum speed desired for clockwise rotation
min_value = 1000*4  #minimum speed desired for anti-clockwise rotation

servo = maestro.Controller()
servo.setRange(0, min_value, max_value)
servo.setRange(1, min_value, max_value)
servo.setRange(2, min_value, max_value)
#Initializing motor
servo.setTarget(0,6000)
servo.setTarget(1,6000)
servo.setTarget(2,6000)

print("start, controls, speed or stop")

#def start():
#	T.webcam()
#	T.track()
	#foam.webcam()
	#while(foam.detection == True):		#need to add when object is detected
	#	if camera_centre != object_centre: #need to include frame centre from foam.py
	#		while(object_centre < camera_centre):
	#			turnLeft(0.5)
	#		else:
	#			turnRight(0.5)

		#Keep a constant distance between target object
#		while(get_Camera_Distance == True):
#			if distance > 100:
#				F.Thruster_Values(LDM = 0, Speed_PC=1) # move forwards
#			else:
#				F.Thruster_Values(LDM = 180, Speed_PC=1) # move backwards
#		while(get_Camera_Distance == False):
#			F.turnRight(1)


def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
	return ch


def controls():
	while True:
		char = getch()
		# Move Forward
		if(char=="w"):
			pause()
			time.sleep(3)
			servo.setTarget(0,1498*4)
			servo.setTarget(1,1648*4)
			servo.setTarget(2,1338*4)
			# F.Thruster_Values(LDM = 0, Speed_PC=0.05) #forward
		elif(char=="s"):
			pause()
			time.sleep(3)
			servo.setTarget(0,1498*4)
			servo.setTarget(1,1358*4)
			servo.setTarget(2,1688*4)
			# F.Thruster_Values(LDM = 180, Speed_PC=0.05) #backward
			#time.sleep(2)
		elif(char=="d"):
			pause()
			time.sleep(3)
			F.Thruster_Values(LDM = 90, Speed_PC=0.05) #move right
			#time.sleep(2)
		elif(char=="a"):
			pause()
			time.sleep(3)
			F.Thruster_Values(LDM = -90, Speed_PC=0.05) #move left
			#time.sleep(2)
		elif(char=="e"):
			pause()
			time.sleep(3)
			F.turnRight(1)
			#time.sleep(2)
		elif(char=="q"):
			pause()
			time.sleep(3)
			F.turnLeft(1)
			#time.sleep(2)
		elif(char=="p"):
			pause()
			time.sleep(4)
		elif(char=="h"):
			stop()
			break

def turnLeft():
	pause()
	time.sleep(3)
	servo.setTarget(0,1338*4)
	servo.setTarget(1,1500*4)
	servo.setTarget(2,1500*4)

def turnRight():
	pause()
	time.sleep(3)
	servo.setTarget(0,1648*4)
	servo.setTarget(1,1500*4)
	servo.setTarget(2,1500*4)

def control_speed():
	print ("I'm Starting the motor, I hope its calibrated and armed.")
	time.sleep(1)
	speed1 = 1500*4    # change your speed if you want to.... it should be between 700 - 2000
	speed2 = 1500*4
	speed3 = 1500*4
	print ("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
	while True:
		char = getch()
		servo.setTarget(0,speed1)
		servo.setTarget(1,speed2)
		servo.setTarget(2,speed3)
        #inp = input()

		if char == "a":
			speed1 -= 50    # decrementing the speed like hell
			print ("speed1 = %d" % speed1)
		elif char == "q":
			speed1 += 50    # incrementing the speed like hell
			print ("speed1 = %d" % speed1)
		elif char == "w":
			speed2 += 50     # incrementing the speed 
			print ("speed2 = %d" % speed2)
		elif char == "s":
			speed2 -= 50     # decrementing the speed
			print ("speed2 = %d" % speed2)
		elif char == "e":
			speed3 += 50     # incrementing the speed 
			print ("speed3 = %d" % speed3)
		elif char == "d":
			speed3 -= 50     # decrementing the speed
			print ("speed3 = %d" % speed3)
		elif char == "h":
			stop()          #going for the stop function
			break
		elif char == "manual":
			manual_drive()
			break
		elif char == "arm":
			arm()
			break
		else:
			print ("WHAT DID I SAID!! Press a,q,d,e or stop")


def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    servo.setTarget(0,6000)
    servo.setTarget(1,6000)
    servo.setTarget(2,6000)
    servo.close()
    print("Okay")

def pause(): #This will stop every action your Pi is performing for ESC ofcourse.
    servo.setTarget(0,6000)
    servo.setTarget(1,6000)
    servo.setTarget(2,6000)
    print("Pause")


#Starting the program
# char = input()
# if char == "start":
    # start()
# elif char == "controls":
	# controls()
# elif char == "speed":
	# control_speed()
# elif char == "stop":
    # stop()
# else :
    # print ("Error. Restart from beginning.")
