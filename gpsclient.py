import socket
import pickle
import threading
import sys
import ASV_Functions as AF



class Client:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host = '192.168.0.18'
	#host = '10.14.193.149' #eduroam
	addr = 5545

	def __init__(self):
		self.sock.connect((self.host,self.addr))

		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True	#So that it will close when we close the program
		iThread.start()

	def receive(self):
		while True:
			data = self.sock.recv(4096)
			data_arr = pickle.loads(data)
			if not data:
				break
		#	if data[0:] == b'\x11':
		#		self.updatePeers(data[1:])
		#		print("Got peers ",self.peers)
			#else:	
				#print('Received', data_arr)
			return data_arr
			
				

	def sendMsg(self):
		#GPS = [[1,2,3],[[20,15],[14,45],[36,45]]]
		ASV_Data = [AF.GPS]
		data_string = pickle.dumps(ASV_Data)
		#gps_string = pickle.dumps(GPS)
		self.sock.send(data_string)
		#self.sock.send(gps_string)
