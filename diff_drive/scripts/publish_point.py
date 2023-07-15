

 #!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
import tf
import random
import numpy as np
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


def callback(msg): 
    global x,y,z
    point = PointStamped()
    point.header.stamp = rospy.Time.now()
    point.header.frame_id = "/map"

    point.point.x = msg.point.x      
    point.point.y = msg.point.y
    point.point.z = msg.point.z
    rospy.loginfo("coordinates:x=%f y=%f" %(point.point.x, point.point.y))
#    rospy.loginfo("x = %f", point.point.x)
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    
   
    goal.target_pose.pose.position.x = point.point.x
    goal.target_pose.pose.position.y = msg.point.y
    goal.target_pose.pose.orientation.z =  msg.point.z
#   goal.target_pose.pose.orientation.w = 0.456
    
        
        

   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result() 

def listener():
    rospy.init_node('goal_publisher', anonymous=True)
    rospy.point_pub = rospy.Subscriber('/clicked_point', PointStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()