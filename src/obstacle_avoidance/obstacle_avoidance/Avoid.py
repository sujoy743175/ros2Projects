from operator import ifloordiv
import sys
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from time import sleep


class Obstacle_Avoidnace(Node):    
    #A node with a obstacle avoidance.
    def __init__(self):
        # Calls Node.__init__('Obstacle_Avoidnace')
        super().__init__('Obstacle_Avoidnace')
        self.sub = self.create_subscription(Int32, 'fwd_distance', self.fwd_distance_callback, 1)
        self.sub = self.create_subscription(Int32, 'left_distance', self.lft_distance_callback, 1)
        self.sub = self.create_subscription(Int32, 'right_distance', self.rt_distance_callback, 1)
        self.sub  # prevent unused variable warning
        # Publishes cmd_vel
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 1)

        # Vehicle parameters
        #self.speed = 0.2
        self.angle_correction = 0.01

        # Initialze parameters
        self.fwd_distance_callback
        self.lft_distance_callback
        #self.rt_distance_callback
        #self.Deltas = 0
        self.cmd = Twist()
        #self.stop = False               
        #self.count = 0
        #self.count_threshold = 10
        self.fwd_distance_threshould = 0
        self.lft_distance_threshould = 0
        #self.rt_distance_threshould = ""

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
            self.lft_distance_threshould =10

        if self.fwd_distance_threshould == 0:
            self.fwd_distance_threshould =30
        
        if self.fwd_distance_threshould >= 30 and self.lft_distance_threshould >= 10:
            self.forward()
        
        elif self.fwd_distance_threshould < 30 and self.lft_distance_threshould>30:
            #self.get_logger().info('fwd_distance_threshould  breached ...STOPPING') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.left()
            self.Stop()   

        elif self.fwd_distance_threshould >= 30 and self.lft_distance_threshould<10:
            #self.get_logger().info('fwd_distance_threshould  breached ...STOPPING') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.right()
            self.Stop()
        
        else:
            self.Stop()
            self.reverse()
            self.Stop()
            self.right()
            self.Stop() 
            
              

        #print(self.cmd) 
        # Correction parameters
        '''self.Deltas = self.fwd_distance_callback
        self.cmd.angular.z = self.angle_correction*self.Deltas'''

        # Logic for obstacle avoidance if distance forward crosses threshould limit
   
        
                      

        '''if self.stop:
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
        
        # Publish cmd_vel
        self.publisher_.publish(self.cmd)
        print(self.cmd)
        self.stop = False
        print(self.cmd)'''

   

    def lft_distance_callback(self, msg):
        #blink_code.LedInput = msg.data
        self.get_logger().info('Left distance is ......: "%d"' % msg.data) 
        self.lft_distance_threshould = msg.data
        print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module()

    
    def rt_distance_callback(self, msg):
        #blink_code.LedInput = msg.data
        self.get_logger().info('Right distance is ......: "%d"' % msg.data) 
        self.rt_distance_threshould = msg.data
        print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module()
    
    def fwd_distance_callback(self, msg):
        #blink_code.LedInput = msg.data
        self.get_logger().info('Forward distance is ......: "%d"' % msg.data) 
        self.fwd_distance_threshould = msg.data
        print(type(self.lft_distance_threshould))
        self.Obstacle_Avoidance_module()
    


def main(args=None): 
    rclpy.init(args=args)
    try:
        obstacle_avoidnace = Obstacle_Avoidnace()
        rclpy.spin(obstacle_avoidnace)
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        rclpy.try_shutdown()
        obstacle_avoidnace.destroy_node()

if __name__ == '__main__':
    # Runs a Obstacle_Avoidnace node when this script is run directly (not through an entrypoint)
    main()
