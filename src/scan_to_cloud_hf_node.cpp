#include "scan_to_cloud_hf.h"

int main (int argc, char **argv)
{
  ros::init (argc, argv, "ScanToCloudHf");
  ros::NodeHandle nh;
  ros::NodeHandle nh_private("~");
  capra_lidar::ScanToCloudHf ltcc(nh, nh_private);
  ros::spin();
  return 0;
}
