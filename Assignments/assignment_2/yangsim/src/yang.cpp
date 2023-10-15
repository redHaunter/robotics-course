#include "rclcpp/rclcpp.hpp"
#include "tutorial_interfaces/srv/conv.hpp"
#include "tutorial_interfaces/msg/conversation.hpp"
#include "std_msgs/msg/string.hpp"

#include <memory>
#include <chrono>
#include <functional>
#include <string>

using namespace std::chrono_literals;

class MinimalPublisher : public rclcpp::Node
{
  public:
  
    MinimalPublisher()
    : Node("yang_node")
    {
      service =
        this->create_service<tutorial_interfaces::srv::Conv>("yang_srv",
      std::bind(&MinimalPublisher::add, this, std::placeholders::_1, std::placeholders::_2));

      publisher_ = this->create_publisher<std_msgs::msg::String>("conversation", 10);
  
    }

  void add(const std::shared_ptr<tutorial_interfaces::srv::Conv::Request> request,     
            std::shared_ptr<tutorial_interfaces::srv::Conv::Response>       response)  
  {
    int temp = 0;
    std::string myMsg = request->msg;
    for (int i=0;i<request->length;i++){
      temp += int(myMsg.at(i));
    }
    response->checksum = temp;
    std_msgs::msg::String message;
    message.data = "yin said: "+myMsg+","+std::to_string(request->length)+","+std::to_string(temp);
    this->publisher_->publish(message);
    
  }
  private:
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::Service<tutorial_interfaces::srv::Conv>::SharedPtr service;
};



int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);

  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
}
