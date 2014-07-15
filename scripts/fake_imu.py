#! /usr/bin/env python

import roslib; roslib.load_manifest('capra_lidar')
import rospy
import csv
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Pose2D, Quaternion
import time
import math
from tf.transformations import quaternion_from_euler

def callback(data):
    imu = Imu()
    imu.orientation = quaternion_from_euler(0, 0, data.theta)
    imu.header.stamp = rospy.Time.now()
    imu.header.frame_id = "/base_link"
    
    global pub
    pub.publish(imu)

rospy.init_node('fake_imu', anonymous=True)
pub = rospy.Publisher('/imu_data', Imu, queue_size=10)
rospy.Subscriber("/pose2D", Pose2D, callback)
rospy.spin()
