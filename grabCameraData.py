import urllib2
import time
import sys
start = 550
end = 650
stream1 = "http://207.251.86.238/cctv303.jpg?math=0.29673863811952195"
stream2 = "http://207.251.86.238/cctv914.jpg?math=0.6789836945555643" #10 ave at 42nd
stream3 = "http://207.251.86.238/cctv413.jpg?math=0.8986791025384302" #Queens Bridge upper level CM @ Roosevelt
stream4 = "http://207.251.86.238/cctv492.jpg?math=0.07714356129290212" #Park Avenue @ 57th
stream5 = "http://207.251.86.238/cctv797.jpg?math=0.38479171676407686" #Park Avenue @ 72nd
for i in range(start, end):
	sys.stdout.write("\033[F")
	sys.stdout.write("\033[K")
	print("Grabbing img " + str(i-start) + " of " + str(end-start))

	f = open('cameraStills/stream5_' + str(i) + '.jpg', 'wb')
	f.write(urllib2.urlopen(stream5).read())
	f.close()
	time.sleep(10)