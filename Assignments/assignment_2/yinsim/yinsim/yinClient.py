import sys

from tutorial_interfaces.srv import Conv
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('yin_client_node')
        self.cli = self.create_client(Conv, 'yang_srv')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Conv.Request()

    def send_request(self, myMsg, myLegnth):
        self.req.msg = myMsg
        self.req.length = myLegnth
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    rclpy.init()

    yin_conv = ["I am Yin, some mistake me for an actual material entity but I am moreof a concept",
        "Interesting Yang, so one could say, in a philosophical sense, we aretwo polar elements",
        "We, Yang, are therefore the balancing powers in the universe.",
        "Difficult and easy complete each other.",
        "Long and short show each other.",
        "Noise and sound harmonize each other.",
        "You shine your light"
    ]
    
    minimal_client = MinimalClientAsync()
    myMsg = yin_conv[int(sys.argv[1])]
    response = minimal_client.send_request(myMsg, len(myMsg))
    minimal_client.get_logger().info(
        'Result : %d' %
        (response.checksum))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()