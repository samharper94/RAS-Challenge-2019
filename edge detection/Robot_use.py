#!/usr/bin/env python
from __future__ import print_function
import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import cv2
import numpy as np
from matplotlib import pyplot as plt
 
class image_converter:

   def __init__(self):
     self.image_pub = rospy.Publisher("image_topic_2",Image, queue_size=10)
     ct = 1

     # Load template

     self.template = cv2.imread('template.jpg',0)
     self.w, self.h = self.template.shape[::-1]
     # All the 6 methods for comparison in a list
     self.methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
     
     self.bridge = CvBridge()
     self.image_sub = rospy.Subscriber("/kinect2/sd/image_color_rect",Image,self.callback)
 
   def callback(self,data):
     try:
       cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
     except CvBridgeError as e:
       print(e)
 
     (rows,cols,channels) = cv_image.shape
     if cols > 60 and rows > 60 :
       cv2.circle(cv_image, (50,50), 10, 255)
 
     cv2.imshow("Image window", cv_image)

     c = cv2.waitKey(10)

     for meth in self.methods:
        img = cv_image.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,self.template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + self.w, top_left[1] + self.h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()    

#     if 's' == chr(c & 255):
#         cv2.imwrite('/home/ussl/Documents/EDGE' + str(ct) + '.jpg' ,cv_image)
#         print("saving image")
     
 
     try:
       self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
     except CvBridgeError as e:
       print(e)
 
def main(args):
   ic = image_converter()
   rospy.init_node('image_converter', anonymous=True)
   try:
     rospy.spin()
   except KeyboardInterrupt:
     print("Shutting down")
   cv2.destroyAllWindows()
 
if __name__ == '__main__':
   main(sys.argv)
