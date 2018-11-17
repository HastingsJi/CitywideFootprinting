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

C = CarDetector('CarCounting/InferenceGraph/frozen_inference_graph.pb')
#C = CarDetector('CarCounting/InferenceGraph/ssd_lite_graph.pb')

class tempData:
	def __init__(self):
		self.boundingBoxes = []
		self.total = 0

T = tempData()

class stream:
	def __init__(self):
		self.G = getStream('http://207.251.86.238/cctv797.jpg?math=0.15975369761797253')

	def GET(self):
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

	def getImage(self):
		total = T.total
		boundingBoxes = T.boundingBoxes
		file = self.stream.read()
		encoded_string = base64.b64encode(file)
		arr = np.asarray(bytearray(file), dtype=np.uint8)
		img = cv2.imdecode(arr, -1)

		#filter out background
		img2 = img.copy()
		self.filter(img2)

		sensitivity = 0.7

		boxes, scores, classes, num = C.getClassification(img2)
		limit = 0
		for i in range(scores[0].shape[0]):
			limit = i
			if scores[0][i] < sensitivity:
				break
		nBoxes = boxes[0][0:limit]
		nScores = scores[0][0:limit]
		nClasses = classes[0][0:limit]

		#Box colors

		currentBoxes = []
		for box1 in nBoxes:
			x1 = min(351,int(round(box1[1]*352)))
			y1 = min(239,int(round(box1[0]*240)))
			x2 = min(351,int(round(box1[3]*352)))
			y2 = min(239,int(round(box1[2]*240)))
			print((x1, x2, y1, y2))
			currentBoxes.append((x1, x2, y1, y2))

		#do classification here
		
		self.corr = correlationClass(boundingBoxes, currentBoxes)
		# for img1coords in boundingBoxes:
		# 	(x1, x2, y1, y2) = img1coords
		# 	img1 = img[y1:y2, x1:x2]
		# 	for img2coords in currentBoxes:
		# 		(x1, x2, y1, y2) = img2coords
		# 		img2 = img[y1:y2, x1:x2]
		tracked, new = self.corr.correlateBoxes(img)

		for i in range(len(currentBoxes)):
			(x1, x2, y1, y2) = currentBoxes[i]
			if i in new:
				img = self.drawBox(img, x1, x2, y1, y2, [0, 255, 0])
			else:
				img = self.drawBox(img, x1, x2, y1, y2, [0, 0, 255])

		print("Image 1 bounding boxes: " + str(len(boundingBoxes)))
		print("Image 2 bounding boxes: " + str(len(currentBoxes)))
		print("Number of correlations: " + str(self.corr.numCorrelations))
		T.boundingBoxes = currentBoxes
		T.total += len(new)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(img,'Car Count: ' + str(T.total),(10,230), font, 0.5,(255,255,255),2,cv2.LINE_AA)
		
		retval, b = cv2.imencode('.jpg', img)
		encoded_string = base64.b64encode(b)
		#encoded_string = base64.b64encode(arr)
		return encoded_string

	def filter(self, img, regions=None):
		if regions is None:
			img[0:146, 135, 0] = 0
			img[0:146, 135, 1] = 0
			img[0:146, 135, 2] = 0
			for i in range(141):
				for j in range(84,352):
					if (i*148.0/78 + 84 < j):
						img[i, j, 0] = 0
						img[i, j, 1] = 0
						img[i, j, 2] = 0

	def drawBox(self, img, x1, x2, y1, y2, colors):
		R = colors[0]
		G = colors[1]
		B = colors[2]
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