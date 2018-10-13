import tensorflow as tf
import cv2
import numpy as np
class CarDetector:
	def __init__(self, graphFile):
		PATH_TO_MODEL = graphFile
		self.detection_graph = tf.Graph()
		with self.detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(PATH_TO_MODEL, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')
			self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
			self.d_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
			self.d_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
			self.d_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
			self.num_d = self.detection_graph.get_tensor_by_name('num_detections:0')
		self.sess = tf.Session(graph=self.detection_graph)

	def getClassification(self, img):
	# Bounding Box Detection.
		with self.detection_graph.as_default():
			# Expand dimension since the model expects image to have shape [1, None, None, 3].
			img_expanded = np.expand_dims(img, axis=0)  
			(boxes, scores, classes, num) = self.sess.run(
				[self.d_boxes, self.d_scores, self.d_classes, self.num_d],
				feed_dict={self.image_tensor: img_expanded})
		
		return boxes, scores, classes, num

# im = cv2.imread("pic123.jpg")
# b,g,r = cv2.split(im)       # get b,g,r
# rgb_img = cv2.merge([r,g,b])     # switch it to rgb
# C = CarDetector()
# C.getClassification(rgb_img)