import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Joy
L = 0.475;                       #  // distance between two horizontal wheels
B = 0.095;                      #  // distance between vertical wheel and horizontal wheel
R = 0.029;                        # // radius of free wheel
N = 600;                          #// pulse per revolution
cm_per_tick = (2 * math.pi * R) / (N); #// 2*pi*R/N where N is ppr 0.0523
odom_wi = 0
PI = math.pi
def cos(a):
    return math.cos(a)
def sin(a):
    return math.sin(a)

odom_x,odom_y=0,0

class mark(Node):

    def __init__(self):
        super().__init__('mark')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscriber = self.create_subscription(Joy,'/joy',self.joy_callback,10)
        self.subscriber = self.create_subscription(Odometry,'/odom',self.bno_callback,10)
        self.lockin = False
        self.x = 0
        self.y = 0
        self.currentangle = 0.0
        self.prev_button = 0.0
        self.target_angle = 0.0 

    def basket_angle(self):
        x2 = 5.0
        y2 = 5.0
        del_x = x2-self.x
        del_y = y2-self.y
        if del_x==0:
            if del_y>0:
                self.b_angle = math.pi/2  
            else:
                self.b_angle = 1.5*math.pi  
        else:
            self.b_angle = math.atan(del_y/del_x)
        if del_x>0:
        
            if (del_y<0):
            
                self.b_angle = 2*math.pi-abs(self.b_angle)
                
        elif (del_x<0):
        
            self.b_angle = math.pi+self.b_angle
        if self.b_angle>math.pi:
            self.b_angle = self.b_angle-2*math.pi
        return self.b_angle
    
    def PID(self):
        k = 5.0 
        error = self.target_angle-self.currentangle
        print(f"target = {self.target_angle}")
        print(f"current = {self.currentangle}")
        if abs(error)>0.0005:
            velocity = float(k*2*error)
        elif abs(error)<2*(math.pi)-0.0005:
            velocity = float(k*2*error)
        else:
            velocity = 0.0
        return velocity

    def bno_callback(self,data:Odometry):
        curentangle = data.pose.pose.orientation.z
        self.angl_vel = data.pose.pose.orientation.x
        self.enc1 = data.pose.pose.position.x
        self.enc2 = data.pose.pose.position.y
        self.enc3 = data.pose.pose.position.z
        self.position(self.enc1,self.enc2,self.enc3,curentangle,self.angl_vel)
        # print(f"angle 1={data.pose.pose.orientation.z}")

    def position(self,a_tick,b_tick,c_tick,theta,angvel):
        global odom_y, odom_x , odom_wi
        odom_dx = (cm_per_tick * ((a_tick + b_tick) / 2));                                    #// dx with respect to robot frame calculated every loop
        odom_dy = (cm_per_tick * c_tick ) - (B * cm_per_tick * ((b_tick - a_tick / L))) #// dy with respect to robot frame calculated every loop
        odom_wf = (360 - theta) * (PI / 180)
        odom_dw = odom_wf - odom_wi
        avg_w = odom_wi + (odom_dw)/2.0
        odom_wi = odom_wf

        odom_gx = (odom_dx * cos(avg_w)) - (odom_dy * sin(avg_w)) * 10  #global transform
        odom_gy = (odom_dx * sin(avg_w)) + (odom_dy * cos(avg_w)) * 10
        odom_vw = angvel
        odom_angle = odom_dx/0.05
        e = odom_wf - odom_angle
        odom_x += odom_gx #// we are adding a small value delta x = odom_dx*cos(theta)-odom_dy*sin(theta) to x
        odom_y += odom_gy
        self.x = odom_x
        self.y = odom_y
        if odom_wf>math.pi:
            self.currentangle = odom_wf - 2*math.pi
        else:
            self.currentangle = odom_wf
        # print(f"angle ={theta}")
        # print(f"x = {self.x}")
        # print(f"y = {self.y}")

        return odom_x,odom_y,odom_wf,e

    def joy_callback(self, msg:Joy):
        self.vel = Twist()
        global_vx = float(10*msg.axes[1])
        global_vy = float(10*msg.axes[0])
        current_button = msg.buttons[0]
        self.vel.linear.x =  global_vx*math.cos(self.currentangle) + global_vy*math.sin(self.currentangle)
        self.vel.linear.y = -global_vx*math.sin(self.currentangle) + global_vy*math.cos(self.currentangle)
        if self.prev_button==0 and current_button==1:
            self.lockin = not (self.lockin)
        if msg.axes[3]:
            self.target_angle = self.currentangle
            self.vel.angular.z = float(5*msg.axes[3])
        else :
            if self.lockin:
                self.get_logger().info('Locked in')
                self.target_angle = self.basket_angle()
            # else:
                # self.get_logger().info('Free to move')
            self.vel.angular.z = self.PID()
        self.publisher_.publish(self.vel)
        self.prev_button = current_button

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = mark()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()