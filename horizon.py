import cv2
import numpy as np
from config import conf
import time
import datetime

img = cv2.imread(conf.data_folder + 'frame0134.jpg',0)



kernel = np.ones((7,7),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 1)
gaussian_3 = cv2.GaussianBlur(erosion, (9, 9), 10.0)
unsharp_image = cv2.addWeighted(erosion, 1.5, gaussian_3, -0.5, 0, erosion)


#cv2.imwrite(conf.detected_image_folder + 'erozija.jpg' , 255 * (erosion.astype('uint8')))

edges = cv2.Canny(erosion,100,200)
#cv2.imwrite(conf.detected_image_folder + 'canny.jpg' , 255 * (edges.astype('uint8')))

lines = cv2.HoughLines(edges,1,np.pi/180,80)

for ro, theta in lines[0]:
   if theta == 0.0:
       x1 = int(ro)
       x2 = int(ro)
       y1 = 0
       y2 = img.shape[0]

       cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
       cropped = img[:,0:x1]

   else:
    a = -1/np.tan(theta)
    b = ro/np.sin(theta)
    y1 = 0
    x1 = max(0, int( -b/a))
    y2 = img.shape[0]
    x2 = min(img.shape[1], int((y2-b)/a))
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    xb = max(x1,x2)
    cropped = img [:,0:xb]

#cv2.imwrite(conf.detected_image_folder + 'hough.jpg', 255 * (img.astype('uint8'))


#cv2.imwrite(conf.detected_image_folder + 'cropped2jpg', 255 * (cropped.astype('uint8')))


cv2.imshow("image", cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
