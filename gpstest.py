import gpsclient as C

client = C.Client()
while True:
	ASV_Data = client.receive()
	#ASV_Data.sort()
	print(ASV_Data)
