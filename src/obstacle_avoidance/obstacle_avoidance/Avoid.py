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
        self.sub  # prevent unused variable warning
        # Publishes cmd_vel
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 1)

        # Vehicle parameters
        self.speed = 0.3
        self.angle_correction = 0.01

        # Initialze parameters
        self.fwd_distance_callback
        self.Deltas = 0
        self.cmd = Twist()
        self.stop = False               
        self.count = 0
        self.count_threshold = 10
        self.fwd_distance_threshould = 10

    def forward(self):
            self.cmd.linear.x = 0.3
            self.cmd.angular.z = 0.0
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
                          

            #self.publisher_.publish(self.cmd)
    
    def reverse(self):
            self.cmd.linear.x = -0.3
            self.cmd.angular.z = 0.0
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            print(".....reverse")
            sleep(0.5)   

    def Stop(self):
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            #print(self.cmd)
            sleep(0.1)      
            
    
    def left(self):
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.3
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            self.publisher_.publish(self.cmd)
            print("....tutn left")
            sleep(0.5)   

    def right(self):
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = -0.3


    def Obstacle_Avoidance_module(self):
        # Constant Velocity
        self.cmd.linear.x = self.speed
        #print(self.cmd) 
        # Correction parameters
        '''self.Deltas = self.fwd_distance_callback
        self.cmd.angular.z = self.angle_correction*self.Deltas'''

        # Logic for obstacle avoidance if distance forward crosses threshould limit
        if self.fwd_distance_threshould < 5:
            #self.get_logger().info('fwd_distance_threshould  breached ...STOPPING') 
            #self.stop = True
            self.Stop()
            self.reverse()
            self.Stop()
            self.left()
            self.Stop()

        self.forward()
        
                      

        '''if self.stop:
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
        
        # Publish cmd_vel
        self.publisher_.publish(self.cmd)
        print(self.cmd)
        self.stop = False
        print(self.cmd)'''

    def fwd_distance_callback(self, msg):
        #blink_code.LedInput = msg.data
        self.get_logger().info('I heard: "%d"' % msg.data) 
        self.fwd_distance_threshould = msg.data
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
