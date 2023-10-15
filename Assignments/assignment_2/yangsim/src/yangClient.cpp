#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "rclcpp_components/register_node_macro.hpp"

#include "tutorial_interfaces/srv/conv.hpp"
#include "yinyang_msgs/action/myact.hpp"

#include <chrono>
#include <cstdlib>
#include <memory>

using namespace std::chrono_literals;

// void goal_response_callback(){

// }

// void feedback_callback(){

// }

// void result_callback(){

// }


int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);

  std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("yang_client_node");
  rclcpp::Client<tutorial_interfaces::srv::Conv>::SharedPtr client =
    node->create_client<tutorial_interfaces::srv::Conv>("yin_srv");

  node->declare_parameter("shout", false);
  node->declare_parameter("opacity", 100);

  std::string yang_conv[7] = {
    "Hi Yin, I am Yang the opposite of you.",
    "Yes, Yin; we ourselves, do not mean anything since we are only employed to express a relation",
    "Precisely, Yin; we are used to describe how things function in relation to each other and to the universe.",
    "For what is and what is not beget each other.",
    "High and low place each other.",
    "Before and behind follow each other.",
    "And you fade into the darkness."
  };

  auto request = std::make_shared<tutorial_interfaces::srv::Conv::Request>();
  
  // auto send_goal_options = rclcpp_action::Client<yinyang_msgs::action::Myact>::SendGoalOptions();
  // send_goal_options.goal_response_callback = 
  //   std::bind(&goal_response_callback, node, std::placeholders::_1);
  // send_goal_options.feedback_callback =
  //   std::bind(&feedback_callback, node, std::placeholders::_1);
  // send_goal_options.result_callback = std::bind(&result_callback, node, std::placeholders::_1);
  // send_goal_options.feedback_callback
  // node->client_ptr_->async_send_goal(goal_msg, send_goal_options);

  int index;
  sscanf(argv[1], "%d", &index);
  // if(index == 7){
    
  // }
  std::string myMsg = yang_conv[index];

  while (!client->wait_for_service(1s)) {
    if (!rclcpp::ok()) {
      RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Interrupted while waiting for the service. Exiting.");
      return 0;
    }
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "service not available, waiting again...");
  }
  // std::vector<rclcpp::Parameter> all_new_parameters{rclcpp::Parameter("shout", true)};
  // node->set_parameters(all_new_parameters);
  if (node->get_parameter("shout").get_parameter_value().get<bool>() == true){
    myMsg = "**"+myMsg+"**";
  }
  request->msg = myMsg;
  request->length = myMsg.length();

  auto result = client->async_send_request(request);
  // Wait for the result.
  if (rclcpp::spin_until_future_complete(node, result) ==
    rclcpp::FutureReturnCode::SUCCESS)
  {
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Sum: %ld", result.get()->checksum);
  } 
  else {
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call service");
  }
  // rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}

