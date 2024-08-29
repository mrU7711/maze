#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
import tf
from tf.transformations import quaternion_from_euler

# Publishers for IR sensors
front_ir_pub = None
right_ir_pub = None
left_ir_pub = None

def pose_callback(msg):
    # Publish Odometry message on /odom topic
    odom = Odometry()
    odom.header.stamp = rospy.Time.now()
    odom.header.frame_id = "odom"

    # Set the position
    odom.pose.pose.position.x = msg.position.x
    odom.pose.pose.position.y = msg.position.y
    odom.pose.pose.position.z = msg.position.z

    # Set the orientation
    odom.pose.pose.orientation = msg.orientation

    # Set the velocity (optional, zero here)
    odom.child_frame_id = "base_link"
    odom.twist.twist.linear.x = 0.0
    odom.twist.twist.linear.y = 0.0
    odom.twist.twist.angular.z = 0.0

    # Publish the Odometry message
    odom_pub.publish(odom)

    # Broadcast the transform over tf
    odom_trans = tf.TransformBroadcaster()
    odom_trans.sendTransform(
        (msg.position.x, msg.position.y, msg.position.z),
        (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w),
        rospy.Time.now(),
        "base_link",
        "odom"
    )

def ir_front_callback(msg):
    ir_msg = Float32()
    ir_msg.data = msg.data
    front_ir_pub.publish(ir_msg)

def ir_right_callback(msg):
    ir_msg = Float32()
    ir_msg.data = msg.data
    right_ir_pub.publish(ir_msg)

def ir_left_callback(msg):
    ir_msg = Float32()
    ir_msg.data = msg.data
    left_ir_pub.publish(ir_msg)

if __name__ == '__main__':
    rospy.init_node('robot_driver', anonymous=True)

    # Initialize the odom publisher
    odom_pub = rospy.Publisher('odom', Odometry, queue_size=50)

    # Initialize IR sensor publishers
    front_ir_pub = rospy.Publisher('ir_front_sensor', Float32, queue_size=50)
    right_ir_pub = rospy.Publisher('ir_right_sensor', Float32, queue_size=50)
    left_ir_pub = rospy.Publisher('ir_left_sensor', Float32, queue_size=50)

    # Subscribe to the /pose topic
    rospy.Subscriber('pose', Pose, pose_callback)

    # Subscribe to the distance topics
    rospy.Subscriber('front_distance', Float32, ir_front_callback)
    rospy.Subscriber('right_distance', Float32, ir_right_callback)
    rospy.Subscriber('left_distance', Float32, ir_left_callback)

    # Spin to process callbacks
    rospy.spin()

