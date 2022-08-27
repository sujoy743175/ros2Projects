import numpy as np

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32, Float32

from scipy.optimize import minimize



def estimate_distance(power_received, params=None):
    """This function returns an estimated distance range
    given a single radio signal strength (RSS) reading
    (received power measurement) in dBm.


    Parameters:
        power_received (float): RSS reading in dBm
        params (4-tuple float): (d_ref, power_ref, path_loss_exp, stdev_power)
            d_ref is the reference distance in m
            power_ref is the received power at the reference distance
            path_loss_exp is the path loss exponent
            stdev_power is standard deviation of received Power in dB

    Returns:
        (d_est, d_min, d_max): a 3-tuple of float values containing
            the estimated distance, as well as the minimum and maximum
            distance estimates corresponding to the uncertainty in RSS,
            respectively, in meters rounded to two decimal points
    """

    if params is None:
        params = (1.0, -46.0, 2.0, 2.5)
    
    '''else :
        params = (1.0, -56.0, 2.0, 2.5)'''
        #params = (1,1,1,1)
        # the above values are arbitrarily chosen "default values"
        # should be changed based on measurements

    d_ref = params[0] # reference distance
    power_ref = params[1] # mean received power at reference distance
    path_loss_exp = params[2] # path loss exponent
    stdev_power = params[3] # standard deviation of received power

    uncertainty = 2*stdev_power # uncertainty in RSS corresponding to 95.45% confidence

    d_est = d_ref*(10**(-(power_received - power_ref)/(10*path_loss_exp)))
    d_min = d_ref*(10**(-(power_received - power_ref + uncertainty)/(10*path_loss_exp)))
    d_max = d_ref*(10**(-(power_received - power_ref - uncertainty)/(10*path_loss_exp)))

#return (np.round(d_est,2), np.round(d_min,2), np.round(d_max,2))
#return (np.round(d_est,2))
    

    return d_est


def gps_solve(distances_to_station, stations_coordinates):
        def error(x, c, r):
            return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

        l = len(stations_coordinates)
        S = sum(distances_to_station)
        # compute weight vector for initial guess
        W = [((l - 1) * S) / (S - w) for w in distances_to_station]
        # get initial guess of point location
        x0 = sum([W[i] * stations_coordinates[i] for i in range(l)])
        # optimize distance from signal origin to border of spheres
        return minimize(error, x0, args=(stations_coordinates, distances_to_station), method='Nelder-Mead').x

    



class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.sub = self.create_subscription(Int32, 'Investigator_rssi_pub', self.WifiPower_callback, 1)
        self.sub = self.create_subscription(Int32, 'Firefly_rssi_pub', self.FireFlyPower_callback, 1)
        self.sub = self.create_subscription(Int32, 'Bigboo_rssi_pub', self.BigbooPower_callback, 1)
        self.publisher_ = self.create_publisher(Float32, 'range_Investigator', 10)
        self.publisher1_ = self.create_publisher(Float32, 'range_FireFly', 10)
        self.publisher2_ = self.create_publisher(Float32, 'range_Bigboo', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
    
        self.investigator_power = 0
        self.FireFly_power = 0 
        self.Bigboo_power = 0 
           



        # # example usage, for testing
        '''if __name__ == '__main__':
            print("Example: say RSS = -70dBm")    
            d_est, d_min, d_max = estimate_distance(-70)
            print("Estimated distance in meters is: ", d_est)
            print("Distance uncertainty range in meters is: ", (d_min, d_max))
            print(estimate_distance(-70, (1.0, -55.0, 4, 3)))'''
    
    def WifiPower_callback(self, msg):
        #blink_code.LedInput = msg.data
        #self.get_logger().info('Forward distance is ......: "%d"' % msg.data) 
        self.investigator_power = msg.data
        print("InvestigatorPower received ", msg.data)
        #print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module() 
        return self.investigator_power

    def FireFlyPower_callback(self, msg):
        #blink_code.LedInput = msg.data
        #self.get_logger().info('Forward distance is ......: "%d"' % msg.data) 
        self.FireFly_power = msg.data
        print("FireFlyPower received ", msg.data)
        #print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module() 
        return self.FireFly_power

    def BigbooPower_callback(self, msg):
        #blink_code.LedInput = msg.data
        #self.get_logger().info('Forward distance is ......: "%d"' % msg.data) 
        self.Bigboo_power = msg.data
        print("BigbooPower received ", msg.data)
        #print(type(self.lft_distance_threshould))
        #self.Obstacle_Avoidance_module()
        return self.Bigboo_power 
           
    
    def timer_callback(self):
        msg1 = Float32()
        msg2 = Float32()
        msg3 = Float32()

        msg1.data = float(estimate_distance(self.investigator_power, (1.0, -45.0, 2.0, 2.5)))


        vertex= (estimate_distance(self.FireFly_power, (1.0, -45.0, 2.0, 2.5)))
        msg2.data = float(vertex)

        msg3.data = float(estimate_distance(self.Bigboo_power , (1.0, -40.0, 2.0, 2.5)))

        stations = list(np.array([[0,0], [0,6], [0,6]]))
        distances_to_station = [msg1.data , msg2.data, msg2.data ]
        print(gps_solve(distances_to_station, stations))
        
        #print("power received ", msg.data)
        self.publisher_.publish(msg1)
        self.publisher1_.publish(msg2)
        self.publisher2_.publish(msg3)

        self.get_logger().info('Investigator Distance : "%f"' % msg1.data)  
        self.get_logger().info('FireFly Distance "%f"' % msg2.data)
        self.get_logger().info('Bigboo Distance "%f"' % msg3.data) 
  


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






