import cv2
import numpy as np
import sys


image_left = cv2.imread('images/100001747275.jpg')
image_center = cv2.imread('images/100001747271.jpg')
image_right = cv2.imread('images/100001747272.jpg')

concat_image = cv2.hconcat([image_left, image_center, image_right])

img_yuv = cv2.cvtColor(concat_image, cv2.COLOR_BGR2YUV)

# equalize the histogram of the Y channel
#img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2,2))
img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])

# convert the YUV image back to RGB format
img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

cv2.imshow('image', img_output)
cv2.waitKey(0)
cv2.destroyAllWindows()
