# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 13:12:18 2018

@author: Syafiqah
"""
#import laser3
import numpy as np
import cv2 as cv
import time
import maestro
#import argparse

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

def nothing(x):
    pass
cv.namedWindow('colour range', cv.WINDOW_NORMAL)
#blue: h [60-120] s[40 203], v[26 217]
h,s,v = 100,100,100
cv.createTrackbar('h', 'colour range',28,179,nothing)
cv.createTrackbar('s', 'colour range',0,255,nothing)
cv.createTrackbar('v', 'colour range',66,255,nothing)
cv.createTrackbar('hu', 'colour range',114,190,nothing)
cv.createTrackbar('su', 'colour range',203,255,nothing)
cv.createTrackbar('vu', 'colour range',255,255,nothing)
#red = np.uint8([[[0,0,255 ]]])
#hsv_red = cv2.cvtColor(red,cv2.COLOR_BGR2HSV)
#print (hsv_red) = [[[  0 255 255]]] ,183

#defaultSpeed = 50
windowCenter = 320
centerBuffer = 50
#pwmBound = float(50)
cameraBound = float(320)
#kp = pwmBound / cameraBound
leftBound = int(windowCenter - centerBuffer)
rightBound = int(windowCenter + centerBuffer)
error = 0
ballPixel = 0

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_SETTINGS,0.0)
#distance = laser3.distance
while(True):
	ret, frame = vid.read()
	median = cv.medianBlur(frame,9)
	gray = cv.GaussianBlur(frame, (11,11),0)
	hsvt = cv.cvtColor(gray,cv.COLOR_BGR2HSV)
	hsvt2 = cv.cvtColor(median,cv.COLOR_BGR2HSV)
	
	h = cv.getTrackbarPos('h','colour range')
	s = cv.getTrackbarPos('s','colour range')
	v = cv.getTrackbarPos('v','colour range')
	hu = cv.getTrackbarPos('hu','colour range')
	su = cv.getTrackbarPos('su','colour range')
	vu = cv.getTrackbarPos('vu','colour range')
	lower_obj = np.array([h,s,v])
	upper_obj = np.array([hu,su,vu])
	
	mask = cv.inRange(hsvt, lower_obj, upper_obj)
	mask = cv.erode(mask, None, iterations=2)
	mask = cv.dilate(mask, None, iterations=2)
	
	mask2 = cv.inRange(hsvt2, lower_obj, upper_obj)
	mask2 = cv.erode(mask2, None, iterations=2)
	mask2 = cv.dilate(mask2, None, iterations=2)

	cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts)>0:
		c = max(cnts, key=cv.contourArea)
		((x, y), radius) = cv.minEnclosingCircle(c)
		M = cv.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		print(center)
		if radius > 10:
			detection = cv.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv.circle(frame, center, 5, (0, 0, 255), -1)
			ballPixel = x
		else:
			ballPixel = 0
	#area = M['m00']
	#xx = M['m10'] / area
	#yy = M['m01'] / area
	(minVal2, maxVal2, minLoc2, maxLoc2) = cv.minMaxLoc(mask)
	res = cv.bitwise_and(frame,frame, mask= mask)
	res2 = cv.bitwise_and(frame,frame, mask= mask2)
	(minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(mask2)
	#cv.circle(frame, maxLoc2, 10, (255,0,0), 2)
	#cv.circle(frame, maxLoc, 10, (255,255,0), 2)
	cv.imshow("ori", frame)
	#cv.imshow('median', median)
#	cv.imshow('resmed', res2)
	#cv.imshow("gray", gray)
	cv.imshow("res", res)
	tl = "Turn Left"
	tr = "Turn Right"
	rev = "Reverse"
	fw = "Move Forward"
	ob = "Object is Centered"
	tm = time.time()
	f = open("tracking-log.txt",'a+')

	if ballPixel == 0:
		print("No object detected")
	elif (ballPixel < leftBound) or (ballPixel > rightBound):
		print(ballPixel)
#		laser = laser2.laser_measurement()
		if ballPixel < leftBound:
			turnLeft()
			time.sleep(0.5)
			f.write('{}: {}\n'.format(tm,tl))
			print(tl)
			# if radius > 50 and ballPixel < 110:
				# print(ballPixel)
		elif ballPixel > rightBound:
			turnRight()
			time.sleep(0.5)
			f.write('{}: {}\n'.format(tm,tr))
			print(tr)
			# if radius > 50 and ballPixel > 540:
				# print(ballPixel)
#		elif laser.distance < 1000:
#			f.write('{}: {}\n'.format(tm,rev))
			# print("Reverse")
#		elif laser.distance > 1000:
#			f.write('{}: {}\n'.format(tm,fw))
			# print("Move Forward")
	else:
		pause()
		f.write('{}: {}\n'.format(tm,ob))
		print(ob)
		# if (radius < 40):

	f.close()
			

	#print ("h = %s, s=%s, v=%s" %h %s %v)
	if cv.waitKey(20) == 27: # 27 is ESC key
		stop()
		break

vid.release()
cv.destroyAllWindows()






