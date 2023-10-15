import rclpy
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from rclpy.node import Node

class ChaserNode(Node):
    def __init__(self):
        super().__init__('chaser')

        spawn_client = self.create_client(Spawn, 'spawn')

        while not spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('spawn service not available, waiting again...')

        req1 = Spawn.Request()
        req1.name = 'turtle2'
        req1.x = 2.0
        req1.y = 2.0
        req1.theta = 0.0

        future1 = spawn_client.call_async(req1)

        rclpy.spin_until_future_complete(self, future1)

        if future1.result() is not None:
            self.get_logger().info('Turtle 1 spawned successfully')
        else:
            self.get_logger().warning('Failed to spawn turtle 1')

        # req2 = Spawn.Request()
        # req2.name = 'turtle3'
        # req2.x = 8.0
        # req2.y = 8.0
        # req2.theta = 0.0

        # future2 = spawn_client.call_async(req2)

        # rclpy.spin_until_future_complete(self, future2)

        # if future2.result() is not None:
        #     self.get_logger().info('Turtle 2 spawned successfully')
        # else:
        #     self.get_logger().warning('Failed to spawn turtle 2')



def main():
    rclpy.init()

    chaser_node = ChaserNode()
    rclpy.spin(chaser_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
