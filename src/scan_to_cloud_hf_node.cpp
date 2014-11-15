#include "scan_to_cloud_hf_node.h"

namespace capra_lidar {

    ScanToCloudHf::ScanToCloudHf(ros::NodeHandle nh, ros::NodeHandle nh_private):
      nh_(nh),
      nh_private_(nh_private)
    {
      ROS_INFO("Starting ScanToCloudHf");

      cloud_publisher_ = nh_.advertise<sensor_msgs::PointCloud2>(
        "cloud", 1);
      scan_subscriber_ = nh_.subscribe(
        "scan", 1, &ScanToCloudHf::scanCallback, this);
    }

    ScanToCloudHf::~ScanToCloudHf()
    {
      ROS_INFO("Destroying ScanToCloudHf");
    }

    void ScanToCloudHf::scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan_in)
    {
        //ROS_INFO("Got scan");
        //From http://wiki.ros.org/laser_geometry
        if(!listener_.waitForTransform(
                scan_in->header.frame_id,
                "/base_link",
                scan_in->header.stamp + ros::Duration().fromSec(scan_in->ranges.size()*scan_in->time_increment),
                ros::Duration(1.0))){
             return;
          }

          sensor_msgs::PointCloud2 cloud;
          projector_.transformLaserScanToPointCloud("/base_link",*scan_in,
                  cloud,listener_);

      // Do something with cloud.

      cloud_publisher_.publish(cloud);
    }

} //namespace scan_tools


int main (int argc, char **argv)
{
  ros::init (argc, argv, "ScanToCloudHf");
  ros::NodeHandle nh;
  ros::NodeHandle nh_private("~");
  capra_lidar::ScanToCloudHf ScanToCloud(nh, nh_private);
  ros::spin();
  return 0;
}