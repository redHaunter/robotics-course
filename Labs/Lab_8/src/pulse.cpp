#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include "geometry_msgs/msg/twist.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;
using namespace std::chrono_literals;

/* This example creates a subclass of Node and uses std::bind() to register a
 * member function as a callback from the timer. */

class MinimalNode : public rclcpp::Node
{
public:
  MinimalNode()
  : Node("minimal_node")
  {
    
    subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
      "lidar", 10, std::bind(&MinimalNode::topic_callback, this, _1));
    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);
  }



private:
 void topic_callback(const sensor_msgs::msg::LaserScan::SharedPtr _msg) const
 {
  bool allMore = true;
  geometry_msgs::msg::Twist message;
  // RCLCPP_INFO(this->get_logger(), "Publishing: '%f'", _msg->ranges[0]);
  for (int i = 0; i < sizeof(_msg->ranges); i++)
  {
    if (_msg->ranges[i] < 2)
    {
      RCLCPP_INFO(this->get_logger(), "Publishing: '%f' index: '%d'", _msg->ranges[i], i);
      allMore = false;
      break;
    }
  }
  if (allMore) //if all bigger than one
  {
    message.linear.x = 0.5;
    message.angular.z = 0.0;
  }
  else
  {
    message.linear.x = -0.5;
    message.angular.z = 0.5;
  }
  publisher_->publish(message);

 }
 rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
 rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
};


int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalNode>());
  rclcpp::shutdown();
  return 0;
}
