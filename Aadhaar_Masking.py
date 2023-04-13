import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import pickle
import cv2
import os
from tensorflow.keras import backend as k
import sys
import re
from PIL import Image ,TiffTags,ExifTags
from io import BytesIO
from datetime import datetime,timedelta

class Aadhaar_Masking():


	def maskedAadharnumber(self, img_bytes):

			try:

				nparr = np.fromstring(img_bytes, np.uint8)
				img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

				# loading YoloV3 weights and configuration file with the help of dnn module of OpenCV
				net = cv2.dnn.readNet(
					os.getcwd() + '/Ml_Models/Masked_aadharnumber_model/yolov3-maskaadharnumber_final.weights',
					os.getcwd() + '/Ml_Models/Masked_aadharnumber_model/yolov3-maskaadharnumber.cfg')

				with open(os.getcwd() + "/Ml_Models/Masked_aadharnumber_model/obj.names", "r") as f:
					classes = f.read().splitlines()
				
				layers_names = net.getLayerNames()  # returns the indices of the output layers of the network.
				output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
				
				height, width, channel = img_np.shape

				# accepting image  model and output layers as parameters.
				blob = cv2.dnn.blobFromImage(img_np, 0.0039, (416, 416), (0, 0, 0), True, crop=False)
				net.setInput(blob)
				outs = net.forward(output_layers)
				for out in outs:
					for detection in out:
						# identify the index of class with highest confidence/score
						scores = detection[5:]
						class_id = np.argmax(scores)
						confidence = scores[class_id]
						if confidence > 0.5:
							centre_x = int(detection[0] * width)  # coordinates of the centre of the object detected
							centre_y = int(detection[1] * height)
							w = int(detection[2] * width)  # height and width of the bounding box,
							h = int(detection[3] * height)
							x = int(centre_x - w / 2)
							y = int(centre_y - h / 2)
							#(x, x), (x + w, y + h)
							color = (0, 0, 0)
							thickness = -1
							
							image = cv2.rectangle(img_np, (x,y),(x+w,y+h), color, thickness)
							co_ordinate = (x,y,(x+w),(y+h))
							aadhaar_front_cv2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
							
							im_pil = Image.fromarray(aadhaar_front_cv2)
							
							im_pil.save("masked.jpg", format='JPEG')
							
							
			
			except Exception as E:

				return False

