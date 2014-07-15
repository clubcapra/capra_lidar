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
    quat = quaternion_from_euler(0, 0, data.theta)
    imu.orientation.z = quat[2]
    imu.orientation.w = quat[3]
    imu.orientation_covariance = [0.001225, 0,        0,
                                  0,        0.001225, 0,
                                  0,        0,        0.001225]
                                  
    imu.header.stamp = rospy.Time.now()
    imu.header.frame_id = "/base_footprint"
    
    global pub
    pub.publish(imu)
    pass

rospy.init_node('fake_imu', anonymous=True)
pub = rospy.Publisher('/imu_data', Imu, queue_size=10)
rospy.Subscriber("/pose2D", Pose2D, callback)
rospy.spin()
