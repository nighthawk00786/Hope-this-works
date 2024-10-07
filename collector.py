import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class collecter(Node):

    def __init__(self):
        super().__init__('collector')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
    def timer_callback(self):
        vel = Twist()
        velocity = input("GIMME VELOCITY(vx vy vw): ")
        velocity = velocity.split()
        if len(velocity) != 3:
            vel.linear.x = 0.0
            vel.linear.y = 0.0
            vel.angular.z = 0.0
            print("enter a value next time smartass") 
        # elif (type(velocity[0]) != (int or float)) or (type(velocity[1]) != (int or float)) or (velocity(list[2]) != (int or float)):
        #     print("what are numbers?")
        else:
            vel.linear.x = float(velocity[0])
            vel.linear.y = float(velocity[1])
            vel.angular.z = float(velocity[2])
        self.publisher_.publish(vel)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = collecter()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()