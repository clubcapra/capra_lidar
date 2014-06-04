#! /usr/bin/env python

import roslib; roslib.load_manifest('capra_lidar')
import rospy
import csv
from sensor_msgs.msg import LaserScan
import time

rf_data = None
sg_data = None
new_data = False

def rf_callback(data):
    global rf_data
    rf_data = data
    new_data = True
    
def sg_callback(data);
    global sg_data
    sg_data = data
    new_data = True

def get_most_recent_timestamp(rf, sg):
    # Timestamp (on prend le plus recent)
    stamp = 0
    if rf:
        stamp = rf.header.stamp
    if sg:
        if sg.header.stamp > stamp:
            stamp = sg.header.stamp
    return stamp

def merge_scans(rf, sg):
    scan = LaserScan()
    scan.header.frame_id = 'laser'
    scan.header.stamp = get_most_recent_timestamp(rf, sg)    


    return scan

rospy.init_node('laser_scan_merger', anonymous=True)
pub = rospy.Publisher('/base_scan', LaserScan)
rospy.Subscriber("/scan", LaserScan, rf_callback)
rospy.Subscriber("/SeaGoatRosClient/VisionScan", LaserScan, sg_callback)


while not rospy.is_shutdown():
    if new_data:
        scan = merge_scans(rf_data, sg_data)
        pub.publish(scan)
    time.sleep(0.001)

rospy.spin()
