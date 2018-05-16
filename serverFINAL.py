import socket
import pickle
import threading
import sys

class Server:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connections = []
	data_list = []
	host = ''
	addr = 5545

	def __init__(self):
		self.sock.bind((self.host,self.addr))
		self.sock.listen(5)
		print("Server running..")

	def dataTransfer(self, c, a):
		global connections
		while True:
			#c, a =self.sock.accept()
			data = c.recv(4096)	#Receive data
			if not data:
				print(str(a[0]) + ':' + str(a[1]), "disconnected")
				self.connections.remove(c)
				for i in range(len(self.data_list)):
					if self.data_list[i][2] == a[1]:	#checks if data list is associated with port
						self.data_list.pop(i)	#removes data associated with connections
						break
				print(len(self.connections))
				if len(data_arr) == 1:
					for connection in self.connections:
						connection.send(pickle.dumps(self.data_list))
				else:
					pass
				c.close()
				break
			# print(data)
			data_arr = pickle.loads(data)
			flag_exist = 0	#data does not exist yet
			
			for i in self.data_list:
				if len(data_arr) == 1:
					if i[0] == data_arr[0]:	#checks if ASV name in list matches ASV name in data 
						i = data_arr	#overwrites new data of same name into the list
						flag_exist = 1	#data already exist, so no need to append
					else:
						if i[0] == data_arr[0][0]:
							i[1] = data_arr[0][1]
							flag_exist = 1

			if flag_exist == 0 and len(data_arr) == 2:
				#if len(data_arr) == 1:
				#print(len(data_arr))
				data_arr.append(a[1])	#add port to list if data is not in the list
				self.data_list.append(data_arr)	#append data if not yet in list


					# if flag_exist == 0:
						# data_arr.append(a[1])
						# self.data_list.append(data_arr)
			# for i in self.data_list:
				# if len(data_arr) == 2:
					# if i[0] == data_arr[0][0]:
						# i[1] = data_arr[0][1]
						# flag_exist = 1

					# if flag_exist == 0:
						# self.data_list.append(data_arr)
			#if flag_exist == 0:
			#	if len(data_arr) == 1:
			#		data_arr.append(a[1])	#add port to list if data is not in the list
			#		self.data_list.append(data_arr)	#append data if not yet in list
			print(len(self.connections))


			for connection in self.connections:
				connection.send(pickle.dumps(self.data_list))
			#if not data:
			#	print(str(a[0]) + ':' + str(a[1]), "disconnected")
			#	self.connections.remove(c)
			#	c.close()
			#	break

	def run(self):
		while True:
			c, a = self.sock.accept()
			print (c)
			print (a)
			cThread = threading.Thread(target=self.dataTransfer, args=(c,a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			#print (len(self.connections))
			print(str(a[0]) + ':' + str(a[1]), "connected")		# a[0], a[1] are the address and port
			


server = Server()
server.run()