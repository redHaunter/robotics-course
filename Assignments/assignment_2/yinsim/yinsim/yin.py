from tutorial_interfaces.srv import Conv
import os
import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class MinimalService(Node):

    def __init__(self, opacity):
        super().__init__('yin_node')
        self.srv = self.create_service(Conv, 'yin_srv', self.calc_checksum)
        self.publisher_ = self.create_publisher(String, 'conversation', 10)
        self.opacity = opacity

    def calc_checksum(self, request, response):
        temp = 0
        myMsg = request.msg
        if "bye" in myMsg:
            self.opacity = 0
        
        for c in myMsg:
            temp += ord(c)

        response.checksum = temp
        msg = String()
        msg.data = "yang said: "+myMsg+","+str(len(myMsg))+","+str(temp)
        self.publisher_.publish(msg)
        return response

def main():
    rclpy.init()

    minimal_service = MinimalService(100)

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()