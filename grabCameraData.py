import urllib2
import time
import sys
start = 0
end = 100
stream1 = "http://207.251.86.238/cctv303.jpg?math=0.29673863811952195"
stream2 = "http://207.251.86.238/cctv914.jpg?math=0.6789836945555643" #10 ave at 42nd
stream3 = "http://207.251.86.238/cctv413.jpg?math=0.8986791025384302" #Queens Bridge upper level CM @ Roosevelt
stream4 = "http://207.251.86.238/cctv492.jpg?math=0.842557268994081" #Park Avenue @ 57th

for i in range(start, end):
	sys.stdout.write("\033[F")
	sys.stdout.write("\033[K")
	print("Grabbing img " + str(i) + " of " + str(end-start))

	f = open('cameraStills/stream4_' + str(i) + '.jpg', 'wb')
	f.write(urllib2.urlopen(stream4).read())
	f.close()
	time.sleep(5)