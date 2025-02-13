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


import argparse
 
class image_converter:

   def __init__(self):
     self.image_pub = rospy.Publisher("image_topic_2",Image, queue_size=10)
     self.bridge = CvBridge()
     self.image_sub = rospy.Subscriber("/kinect2/sd/image_color_rect",Image,self.callback)
 
   def callback(self,data):
     try:
       cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
     except CvBridgeError as e:
       print(e)
 
     (rows,cols,channels) = cv_image.shape
     #if cols > 60 and rows > 60 :
     #  cv2.circle(cv_image, (50,50), 10, 255)
 	
	 # define the list of boundaries
	 boundaries = [
	 ([17, 15, 100], [50, 56, 200])]


	# loop over the boundaries
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
 
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(cv_image, lower, upper)
		output = cv2.bitwise_and(cv_image, image, mask = mask)
 
	# show the images
	cv2.imshow("images", np.hstack([image, output]))
	cv2.waitKey(0)


#     cv2.imshow("Image window", cv_image)

     c = cv2.waitKey(10)
          
 
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
	

