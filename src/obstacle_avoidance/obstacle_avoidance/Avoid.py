from operator import ifloordiv
import sys
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from time import sleep


class Obstacle_Avoidnace(Node):    
    #A node with a obstacle avoidance.
    def __init__(self):
        # Calls Node.__init__('Obstacle_Avoidnace')
        super().__init__('Obstacle_Avoidnace')
        self.sub = self.create_subscription(Float32, 'fwd_distance', self.fwd_distance_callback, 1)
        self.sub = self.create_subscription(Float32, 'left_distance', self.lft_distance_callback, 1)
        self.sub = self.create_subscription(Float32, 'right_distance', self.rt_distance_callback, 1)
        self.sub = self.create_subscription(Int32, 'left_limit_state', self.left_limit_state_callback, 1)
        self.sub = self.create_subscription(Int32, 'right_limit_state', self.right_limit_state_callback, 1)
        self.sub  # prevent unused variable warning
        # Publishes cmd_vel
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        # Vehicle parameters
        #self.speed = 0.2
        self.angle_correction = 0.01

        # Initialze parameters
        self.fwd_distance_callback
        self.lft_distance_callback
        self.rt_distance_callback
        self.left_limit_state_callback
        self.right_limit_state_callback
        #self.Deltas = 0
        self.cmd = Twist()
        #self.stop = False               
        #self.count = 0
        #self.count_threshold = 10
        self.fwd_distance_threshould = 0
        self.lft_distance_threshould = 0
        self.rt_distance_threshould = 0
        self.left_limit_state = 1
        self.right_limit_state = 1
        self.fdw_limit = 40
        self.side_limit = 15

    def forward(self):
            self.cmd.linear.x = 0.2
            self.cmd.angular.z = 0.0
            self.publisher_.publish(self.cmd)
            print(".....going forward")

    def reverse(self):
            self.cmd.linear.x = -0.2
            self.cmd.angular.z = 0.0
            self.publisher_.publish(self.cmd)
            sleep(0.5)            
            print(".....reverse")              

    def Stop(self):
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
            self.publisher_.publish(self.cmd)
            sleep(0.2) 
            print(".....stop")

    def left(self):
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.2
            self.publisher_.publish(self.cmd)
            sleep(0.5)             
            print("....tutn left")             

    def right(self):
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = -0.2
            self.publisher_.publish(self.cmd)            
            sleep(0.5)             
            print("....tutn right")  

    def Obstacle_Avoidance_module(self):
        # Constant Velocity
        #self.cmd.linear.x = self.speed
        if self.lft_distance_threshould == 0:
            self.lft_distance_threshould = self.side_limit

        if self.rt_distance_threshould == 0:
            self.rt_distance_threshould = self.side_limit

        if self.fwd_distance_threshould == 0:
            self.fwd_distance_threshould = self.fdw_limit
        
        if self.fwd_distance_threshould >= self.fdw_limit and self.lft_distance_threshould >= self.side_limit and self.rt_distance_threshould >= self.side_limit and self.left_limit_state != 0 and self.right_limit_state !=0:
            self.forward()

        elif self.left_limit_state ==0:
            print('left limit breached .........STOPPING') 
            #self.get_logger().info('left limit breached .........STOPPING') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.right()
            self.Stop()
            self.forward() 
        
        elif self.right_limit_state ==0:
            print('right limit  breached .......STOPPING') 
            #self.get_logger().info('right limit  breached .......STOPPING') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.left()
            self.Stop() 
            self.forward()

        elif self.fwd_distance_threshould < self.fdw_limit  and self.lft_distance_threshould>self.rt_distance_threshould:
            print('fwd_distance_threshould  breached ...STOPPING...going left') 
            #self.get_logger().info('fwd_distance_threshould  breached ...STOPPING...going left') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.left()
            self.Stop()
            self.forward()   

        elif self.fwd_distance_threshould < self.fdw_limit  and self.lft_distance_threshould<self.rt_distance_threshould:
            print('fwd_distance_threshould  breached ...STOPPING....going right') 
            #self.get_logger().info('fwd_distance_threshould  breached ...STOPPING....going right') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.right()
            self.Stop()
            self.forward() 

        elif self.fwd_distance_threshould < self.fdw_limit  and self.lft_distance_threshould==self.rt_distance_threshould:
            #self.get_logger().info('fwd_distance_threshould  breached ...STOPPING equal distance going left ') 
            print('fwd_distance_threshould  breached ...STOPPING equal distance going left ') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.left()
            self.Stop() 
            self.forward()

        elif self.fwd_distance_threshould >= self.fdw_limit and self.lft_distance_threshould<self.side_limit and self.rt_distance_threshould>self.side_limit:
            #self.get_logger().info('left_distance_threshould  breached ...STOPPING going right') 
            print('left_distance_threshould  breached ...STOPPING going right') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.right()
            self.Stop()
            self.forward()

        elif self.fwd_distance_threshould >= self.fdw_limit and self.rt_distance_threshould<self.side_limit and self.lft_distance_threshould>self.side_limit:
            print('right_distance_threshould  breached ...STOPPING going left') 
            #self.get_logger().info('right_distance_threshould  breached ...STOPPING going left') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.left()
            self.Stop()
            self.forward()

        elif self.fwd_distance_threshould >= self.fdw_limit and self.rt_distance_threshould<self.side_limit and self.lft_distance_threshould<self.side_limit:
            print('both side_distance_threshould  breached ...STOPPING trying left') 
            #self.get_logger().info('both side_distance_threshould  breached ...STOPPING trying left') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.left()
            self.Stop()
            self.forward()
        
        else:
            pass


   
    def left_limit_state_callback(self, msg):
        #blink_code.LedInput = msg.data
        #self.get_logger().info('left limit is......: "%d"' % msg.data) 
        self.left_limit_state = msg.data
        #print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module()

    def right_limit_state_callback(self, msg):
        #blink_code.LedInput = msg.data
        #self.get_logger().info('right limit is ......: "%d"' % msg.data) 
        self.right_limit_state = msg.data
        #print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module()
    
    def fwd_distance_callback(self, msg):
        #blink_code.LedInput = msg.data
        #self.get_logger().info('Forward distance is ......: "%d"' % msg.data) 
        self.fwd_distance_threshould = msg.data
        #print(type(self.lft_distance_threshould))
        self.Obstacle_Avoidance_module()

    def lft_distance_callback(self, msg):
        #blink_code.LedInput = msg.data
        #self.get_logger().info('Left distance is ......: "%d"' % msg.data) 
        self.lft_distance_threshould = int(msg.data)
        #print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module()
    
    def rt_distance_callback(self, msg):
        #blink_code.LedInput = msg.data
        #self.get_logger().info('Right distance is ......: "%d"' % msg.data) 
        self.rt_distance_threshould = msg.data
        #print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module()
    


def main(args=None): 
    rclpy.init(args=args)
    try:
        while(1):
            obstacle_avoidnace = Obstacle_Avoidnace()
            rclpy.spin(obstacle_avoidnace)
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        rclpy.try_shutdown()
        obstacle_avoidnace.destroy_node()

