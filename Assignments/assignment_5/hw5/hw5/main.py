import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import numpy as np
import time
class MyNode(Node):
    def __init__(self):
        super().__init__('mynode')
        self.subscription = self.create_subscription(Image, '/kinect_rgbd_camera/image', self.listener_callback, 10)
        self.subscription
        self.publisher_ = self.create_publisher(Twist, '/model/eddiebot/cmd_vel', 1)
        self.state = "forward"
    def listener_callback(self, msg):
        img = np.array(msg.data).reshape((msg.height, msg.width, (msg.step//msg.width)))
        img_points = np.zeros((4, 3))
        img_points[0] = img[5][10]
        img_points[1] = img[5][630]
        img_points[2] = img[475][10]
        img_points[3] = img[475][630]
        # self.get_logger().info('Yellow: "%s"' % str(img_points.shape))
        # crop_img = img[90:390 , 120:520 , :]
        # threshold = int(crop_img.shape[0] * crop_img.shape[1] * 0.83)
        isGreen = 0
        isRed = 0
        isYellow = 0

        message = Twist()

        for pixel in img_points:
            if((pixel[0] == 99 and pixel[1] == 99 and pixel[2] == 0) 
            or (pixel[0] == 58 and pixel[1] == 82 and pixel[2] == 0)
            or (pixel[0] == 59 and pixel[1] == 83 and pixel[2] == 0)
            or (pixel[0] == 100 and pixel[1] == 100 and pixel[2] == 0)):
            # or (pixel[0] == 218 and pixel[1] == 218 and pixel[2] == 218)
            # or (pixel[0] == 217 and pixel[1] == 217 and pixel[2] == 217)
            # or (pixel[0] == 196 and pixel[1] == 196 and pixel[2] == 196)
            # or (pixel[0] == 197 and pixel[1] == 197 and pixel[2] == 197)):
                isYellow+=1

            if((pixel[0] > 50 and pixel[1] < 50 and pixel[2] < 50)):
                isRed+=1

            if((pixel[0] == 0 and pixel[1] == 99 and pixel[2] == 0) 
            or (pixel[0] == 0 and pixel[1] == 100 and pixel[2] == 0)):
                isGreen+=1
            
        if (isYellow == 4):
            if(self.state != "yellow"):
                self.state = "yellow"
                self.get_logger().info('yellow')

        elif (isRed == 4):
            if(self.state != "red"):
                self.state = "red"
                self.get_logger().info('red')
        elif (isGreen == 4):
            if(self.state != "green"):
                self.state = "green"
                self.get_logger().info('green')


        if(self.state == "yellow"):
            # message.linear.x = 0.0
            message.angular.z = -(1.0)
            # message.angular.x = 0.0
            # message.angular.y = 0.0
            self.publisher_.publish(message)
            time.sleep(2.19)
            # message.linear.x = 0.0
            # message.angular.z = 0.0
            # message.angular.x = 0.0
            # message.angular.y = 0.0
            # self.publisher_.publish(message)
            # time.sleep(2)
            self.state = "forward"
        elif(self.state == "red"):
            # message.linear.x = 0.0
            message.angular.z = 1.0
            # message.angular.x = 0.0
            # message.angular.y = 0.0
            self.publisher_.publish(message)
            time.sleep(2.19)
            # message.linear.x = 0.0
            # message.angular.z = 0.0
            # message.angular.x = 0.0
            # message.angular.y = 0.0
            # self.publisher_.publish(message)
            # time.sleep(1)
            self.state = "forward"
        elif(self.state == "green"):
            # message.linear.x = 0.0
            message.angular.z = 1.0
            # message.angular.x = 0.0
            # message.angular.y = 0.0
            self.publisher_.publish(message)
            time.sleep(10)

        elif(self.state == "forward"):
            message.linear.x = 0.4
            # message.angular.z = 0.0
            # message.angular.x = 0.0
            # message.angular.y = 0.0
            self.publisher_.publish(message)
        
        # self.get_logger().info('state: "%s"' % self.state)
        
        
        # self.get_logger().info('Yellow: "%s"' % str(isYellow))
        # self.get_logger().info('Green: "%s"' % str(isGreen))
        # self.get_logger().info('Red: "%s"' % str(isRed))
def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()