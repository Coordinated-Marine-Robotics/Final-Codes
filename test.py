import client as C
client = C.Client()
while True:
	ASV_Data = client.receive()
	ASV_Data.sort()
	print(ASV_Data)

	# Name: ASV_Data[0][0], x-coords: ASV_Data[0][1][0], y-coords: ASV_Data[0][1][1]
