import urllib2
#import urllib.request
import cv2
import numpy as np
import web
import base64
from TF_SSD import CarDetector
from utility.correlation import correlationClass

urls = ("/", "stream",
		"/test", "testCamera")

C = CarDetector('CarCounting/InferenceGraph/new_stream5_graph.pb')
#C = CarDetector('CarCounting/InferenceGraph/ssd_lite_graph.pb')
class stream:
	def GET(self):
		self.G = getStream('http://207.251.86.238/cctv797.jpg?math=0.15975369761797253')
		#self.G = getStream('http://207.251.86.238/cctv797.jpg?math=0.8641532073791593')
		print("Getting stream...")
		return self.G.getImage()

class testCamera:
	def GET(self):
		im = cv2.imread("CarCounting/pic0.jpg")
		#im = im[:, :, ::-1]
		
		sensitivity = 0.7
		C = CarDetector('CarCounting/InferenceGraph/frozen_inference_graph.pb')
		boxes, scores, classes, num = C.getClassification(im)
		for i in range(scores[0].shape[0]):
			if scores[0][i] < sensitivity:
				limit = i
				break
		nBoxes = boxes[0][0:limit]
		nScores = scores[0][0:limit]
		nClasses = classes[0][0:limit]

		#Box colors
		R = 0
		G = 255
		B = 0
		for box1 in nBoxes:
			x1 = min(351,int(round(box1[1]*352)))
			y1 = min(239,int(round(box1[0]*240)))
			x2 = min(351,int(round(box1[3]*352)))
			y2 = min(239,int(round(box1[2]*240)))
			im[y1:y2, x1, 0] = R
			im[y1:y2, x1, 1] = G
			im[y1:y2, x1, 2] = B
			im[y1:y2, x2, 0] = R
			im[y1:y2, x2, 1] = G
			im[y1:y2, x2, 2] = B
			im[y1, x1:x2, 0] = R
			im[y1, x1:x2, 1] = G
			im[y1, x1:x2, 2] = B
			im[y2, x1:x2, 0] = R
			im[y2, x1:x2, 1] = G
			im[y2, x1:x2, 2] = B

		retval, b = cv2.imencode('.jpg', im)
		encoded_string = base64.b64encode(b)
		return encoded_string


class getStream:
	def __init__(self, url):
		self.stream = urllib2.urlopen(url)
		self.boundingBoxes = []
		self.corr = correlationClass()

	def getImage(self):
		file = self.stream.read()
		encoded_string = base64.b64encode(file)
		arr = np.asarray(bytearray(file), dtype=np.uint8)
		img = cv2.imdecode(arr, -1)

		sensitivity = 0.7

		boxes, scores, classes, num = C.getClassification(img)
		limit = 0
		for i in range(scores[0].shape[0]):
			limit = i
			if scores[0][i] < sensitivity:
				break
		print(limit)
		print(boxes[0][0:limit])
		nBoxes = boxes[0][0:limit]
		nScores = scores[0][0:limit]
		nClasses = classes[0][0:limit]
		#print(nBoxes)

		#Box colors
		R = 0
		G = 255
		B = 0
		currentBoxes = []
		for box1 in nBoxes:
			x1 = min(351,int(round(box1[1]*352)))
			y1 = min(239,int(round(box1[0]*240)))
			x2 = min(351,int(round(box1[3]*352)))
			y2 = min(239,int(round(box1[2]*240)))
			print((x1, x2, y1, y2))
			currentBoxes.append((x1, x2, y1, y2))

		#do classification here

		for (x1, x2, y1, y2) in currentBoxes:
			img = self.drawBox(img, x1, x2, y1, y2, R, G, B)
		
		for img1 in self.boundingBoxes:
			for img2 in currentBoxes:
				self.corr.correlate(img1, img2)
		print("Number of correlations: " + str(self.corr.numCorrelations))
		self.boundingBoxes = currentBoxes

		retval, b = cv2.imencode('.jpg', img)
		encoded_string = base64.b64encode(b)
		#encoded_string = base64.b64encode(arr)
		return encoded_string

	def drawBox(self, img, x1, x2, y1, y2, R, G, B):
		img[y1:y2, x1, 0] = R
		img[y1:y2, x1, 1] = G
		img[y1:y2, x1, 2] = B
		img[y1:y2, x2, 0] = R
		img[y1:y2, x2, 1] = G
		img[y1:y2, x2, 2] = B
		img[y1, x1:x2, 0] = R
		img[y1, x1:x2, 1] = G
		img[y1, x1:x2, 2] = B
		img[y2, x1:x2, 0] = R
		img[y2, x1:x2, 1] = G
		img[y2, x1:x2, 2] = B
		return img


DOTstream = web.application(urls, locals());