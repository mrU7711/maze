#!/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# Define the global variable
turning_direction = 0  # 0: not turning, 1: turning left, -1: turning right

class ReactiveNavigation:
    def __init__(self):  
        rospy.init_node('reactive_navigation', anonymous=True) 
        self.cmd_vel = Twist()
        self.obstacle_distance = 100.0
        self.laser_msg = None  
        self.laser_sub = rospy.Subscriber("base_scan", LaserScan, self.laser_cb, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.rate = rospy.Rate(5)  # 5 Hz

    def laser_cb(self, msg):
        self.laser_msg = msg
    
    def calculate_command(self):
        global turning_direction
        
        if self.laser_msg is None:
            return 
        
        if isinstance(self.laser_msg.ranges, list) or isinstance(self.laser_msg.ranges, tuple):
            self.obstacle_distance = min(self.laser_msg.ranges)
        
        if self.obstacle_distance < 1.0:
            self.cmd_vel.linear.x = 0.0  # Stop moving forward
            
            if turning_direction == 0:
                # Choose a direction to turn based on `turning_direction`
                if self.laser_msg.ranges.index(self.obstacle_distance) < len(self.laser_msg.ranges) / 2:
                    turning_direction = 1  # Turn left
                else:
                    turning_direction = -1  # Turn right

            if turning_direction == 1:
                self.cmd_vel.angular.z = 0.3  # Continue turning left
            elif turning_direction == -1:
                self.cmd_vel.angular.z = -0.3  # Continue turning right

        else:
            self.cmd_vel.linear.x = 0.4  # Move forward
            self.cmd_vel.angular.z = 0.0  # Stop turning
            turning_direction = 0  # Reset turning direction when moving forward

        self.cmd_vel_pub.publish(self.cmd_vel)
        self.obstacle_distance = 100.0  

    def run(self):
        while not rospy.is_shutdown():
            self.calculate_command()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = ReactiveNavigation()
        controller.run()
    except rospy.ROSInterruptException:
        pass

