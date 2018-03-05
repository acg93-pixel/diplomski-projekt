import cv2
import numpy as np
from config import conf
import time


def preprocess_morph_erosion (image, kernel_size=5):
    kernel = np.ones((kernel_size, kernel_size),np.uint8)
    erosion = cv2.erode(image,kernel,iterations = 1)
    return erosion

#def gaussian(img_erosion):
    #gaussian_3 = cv2.GaussianBlur(img_erosion, (9, 9), 10.0)
    #unsharp_image = cv2.addWeighted(img_erosion, 1.5, gaussian_3, -0.5, 0, img_erosion)
    #return unsharp_image

def canny_edge_detection(img_erosion):
    edges = cv2.Canny(img_erosion,50,150)
    return edges

def hough_transform_and_crop(img_edges, image):
    lines = cv2.HoughLines(img_edges,1,np.pi/180,80)
    if lines is None:
        print("No horizon detected")
        return image, False
    for ro, theta in lines[0]:
        if theta == 0.0:
            x1 = int(ro)
            x2 = int(ro)
            y1 = 0
            y2 = image.shape[0]

            cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
            cropped = image[:,0:x1]
        else:
            a = -1/np.tan(theta)
            b = ro/np.sin(theta)
            y1 = 0
            x1 = max(0, int( -b/a))
            y2 = image.shape[0]
            x2 = min(image.shape[1], int((y2-b)/a))

            cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
            #border
            xb = max(x1,x2)

            cropped = image [:, 0:xb]
    return cropped, True


if __name__ == '__main__':
    data_list = []

    for i in range (0, 2820):
        name = 'frame%04d.jpg' % i
        img = cv2.imread(conf.data_folder + name,0)

        start = time.time()
        erosion = preprocess_morph_erosion(img)
        #unsharp_image = gaussian(erosion)
        edges = canny_edge_detection(erosion)
        cropped, status = hough_transform_and_crop(edges,img)
        end = time.time()
        if status is True:
            print("Process time: {:.2f}ms".format(1000 * (end - start)))


            data_list.append(1000 * (end - start))


        if conf.save_data:
            np.save(conf.report_folder + 'stats' ,data_list)


        if conf.save_data:
            cv2.imwrite(conf.image_folder + name, 255 * (cropped.astype('uint8')))


#cv2.imshow("image", cropped)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
