import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.action import RotateAbsolute
from rclpy.action import ActionClient
import random
import time

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('turtlesim_controller')
        # self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.declare_parameter('stop', True)
        self.state = "Stop"
        self.counter = 1000
        timer_period = 0.002  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.turtle_x_ = 0.0
        self.turtle_y_ = 0.0
        self.turtle_angle_ = 0.0

        self.position_subscriber_ = self.create_subscription(Pose, "turtle1/pose", self.set_turtle_position, 10)        
        self.velocity_publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.action_rotate = ActionClient(self, RotateAbsolute, "turtle1/rotate_absolute")
        
    
    def set_turtle_position(self, position):
        self.turtle_x_ = position.x
        self.turtle_y_ = position.y
        self.turtle_angle_ = position.theta

    def timer_callback(self):
        my_param = self.get_parameter('stop').get_parameter_value().bool_value
        if (my_param == False):
            if(self.state == "rotate"):
                my_new_param = rclpy.parameter.Parameter(
                'stop',
                rclpy.Parameter.Type.BOOL,
                True
                )
                all_new_parameters = [my_new_param]
                self.set_parameters(all_new_parameters)


            elif(self.state == "Forward"):
                self.set_forward()
            else:
                self.state = "Forward"
                self.set_forward()

        elif (my_param == True and self.state == "rotate"):
            x = random.uniform(0, 6.0)
            self.set_rotation(x)
            self.state = "rotating"
        elif (my_param == True and self.state == "rotating"):
            self.state = "rotating"
        # self.get_logger().info(str(my_param))

    def set_forward(self):
        if(self.counter < 1000):
            self.set_backward()


        elif (self.turtle_x_ > 11.0 or self.turtle_x_ < 0.1 or self.turtle_y_> 11.0 or self.turtle_y_ < 0.1):
            self.counter -= 1
            self.set_backward()

        else:
            tws = Twist()
            tws.linear.x = 1.0
            tws.linear.y = 0.0
            
            self.velocity_publisher_.publish(tws)
        # self.get_logger().info(str(self.turtle_y_))
        return 0

    def set_backward(self):
        self.counter -= 1
        if(self.counter == 0):
            self.counter = 1000
            self.state = "rotate"
            time.sleep(1)

        else:
            tws = Twist()
            tws.linear.x = -1.0
            tws.linear.y = 0.0
            self.velocity_publisher_.publish(tws)


            
    def set_rotation(self, order):
        goal_msg = RotateAbsolute.Goal()
        goal_msg.theta = order
        
        self.action_rotate.wait_for_server()

        self._send_goal_future = self.action_rotate.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return


        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
        

    def get_result_callback(self, future):
        # result = future.result().result
        self.get_logger().info('Result')
        self.state = "Forward"
        my_new_param = rclpy.parameter.Parameter(
        'stop',
        rclpy.Parameter.Type.BOOL,
        False
        )
        all_new_parameters = [my_new_param]
        self.set_parameters(all_new_parameters)
        # rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        # feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback')
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
