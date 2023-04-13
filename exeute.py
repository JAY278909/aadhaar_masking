import sys
import os 
from Aadhaar_Masking import *
from PIL import Image
import io


getClass = Aadhaar_Masking()
im = Image.open("Sample_PVC_Aadhar_Card_back.jpg")
img_byte_arr = io.BytesIO()
im.save(img_byte_arr, format='PNG')
img_byte_arr = img_byte_arr.getvalue()

getClass.maskedAadharnumber(img_byte_arr)
