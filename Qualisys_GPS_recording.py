from __future__ import print_function

import time
import qtm
from qtm.packet import QRTComponentType

class QScript:

	def __init__(self):
		self.qrt = qtm.QRT("192.168.10.2", 22223) ## set to the IP address of the computer running Qualisys (can be this one)
		self.qrt.connect(on_connect=self.on_connect, on_disconnect=self.on_disconnect, on_event=self.on_event)

	def on_connect(self, connection, version):
		print('Connected to QTM with {}'.format(version))
		# Connection is the object containing all methods/commands you can send to qtm
		self.connection = connection
		# Try to start rt from file

		self.connection.start(rtfromfile=True, on_ok=lambda result: self.start_stream(), on_error=self.on_error)
		##								^ set to false if running in real time
		## if running from a pre-recorded file, open the file in qualisys, but do not run it - this programme will automatically start it
		## if running in real time, make sure you have previously run once without this programme so that you can set it to automatically save and name the .qtm file
		## this programme will start running the qualisys capture but you have to stop it manually. (even if you close this programme, qualisys will keep recording)
	def on_disconnect(self, reason):
		print('disconnected : ', reason)
		# Stops main loop and exits script
		qtm.stop()

	def on_event(self, event):
		# Print event type
		print('event : ',event)

	def on_error(self, error):
		error_message = error.getErrorMessage()
		if error_message == "'RT from file already running'":
			# If rt already is running we can start the stream anyway
			self.start_stream()
		else:
			# On other errors we fail
			print('error : ',error_message)
			self.connection.disconnect()

	def on_packet(self, packet):
		# All packets has a Framenumber and a timestamp
		
		print('Framenumber: %d\t Timestamp: %d' % (packet.framenumber, packet.timestamp))
		print('time = ', time.time())
		# all components have some sort of header
		# both header and components are named tuples
		header, bodies = packet.get_6d_euler()
		names = ['Object', 'ASV_1', 'ASV_2', 'ASV_3']
		## ^ a list of the names of the bodies known by Qualisys, in the order they appear under "project options" -> "6DoF tracking" in Qualisys
		Coords = ['Coords']
		GPS = ['GPS']
		Coords.append([names[1], [bodies[1][0][0], bodies[1][0][1], bodies[1][0][2]]])
			## 50deg 56.20500mins N , 1deg 24.34367mins W = (0,0) in tank coordinates
			## 1 deg lat = 111.2483km , 1 min lat = 1.8541km = 1854100mm
			## 1 mm lat = 0.0000005393 min lat
			## 1 deg long = 70.1977km , 1 min long = 1.1700km = 1170000mm
			## 1 mm long = 0.0000008547 min long
		GPS.append([names[1], '$GPGGA,'+str(packet.timestamp)+','+'050'+str(56.205 + (bodies[1][0][1]*0.0000005393))+',N,001'+str(24.34367 + (0.0000008547*bodies[1][0][0]))+',W,5,4,1.0,'+str(bodies[1][0][2]/1000)+',m,0,m,'])
		print(Coords)
		print(GPS)
		print()
				
	def start_stream(self):
		# Start streaming 2d data and register packet callback
		self.connection.stream_frames(frames='frequencydivisor:100', on_packet=self.on_packet, components=['6dEuler'])
		##										^ the data will be recorded every n frames

		# Schedule a call for later to shutdown connection
		qtm.call_later(50000000, self.connection.disconnect)
		##				^ the number of seconds the programme will run for (Qualisys will keep recording after this time has elapsed, but this programme will no longer record data)

def main():
	# Instantiate our script class
	# We don't need to create a class, you could also store the connection object in a global variable
	QScript()

	# Start the processing loop
	qtm.start()


if __name__ == '__main__':
	main()
