# Copyright 2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32

class Listener(Node):
    """
    A node with a single subscriber.

    This class creates a node which prints messages it receives on a topic. Creating a node by
    inheriting from Node is recommended because it allows it to be imported and used by
    other scripts.
    """

    def __init__(self):
        # Calls Node.__init__('listener')
        super().__init__('listener')
        self.sub = self.create_subscription(Int32, 'led_state', self.chatter_callback, 10)
        self.sub  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Int32, 'led_input', 10)

    def chatter_callback(self, msg):
        #blink_code.LedInput = msg.data
        self.get_logger().info('I heard: "%d"' % msg.data)        
        if msg.data == 1:
            msg.data = 0            
        else:
            msg.data = 1
        self.get_logger().info('publishing: "%d"' % msg.data)
        self.publisher_.publish(msg)
       


def main(args=None):
    """
    Run a Listener node standalone.

    This function is called directly when using an entrypoint. Entrypoints are configured in
    setup.py. This along with the script installation in setup.cfg allows a listener node to be run
    with the command `ros2 run examples_rclpy_executors listener`.

    :param args: Arguments passed in from the command line.
    """
    rclpy.init(args=args)
    try:
        listener = Listener()
        rclpy.spin(listener)
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        rclpy.try_shutdown()
        listener.destroy_node()


if __name__ == '__main__':
    # Runs a listener node when this script is run directly (not through an entrypoint)
    main()
