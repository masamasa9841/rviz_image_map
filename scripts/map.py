#! /usr/bin/env python
import rospy
from PIL import Image
from std_msgs.msg import Header
from nav_msgs.msg import MapMetaData, OccupancyGrid
from geometry_msgs.msg import Pose, Point, Quaternion
from sensor_msgs.msg import Joy

class map(object):
    def __init__(self):
        rospy.init_node('tinpopo')
        self.x = 0 
        self.y = 0 
        self.pub = rospy.Publisher('/uedaoniityann', OccupancyGrid, queue_size=1)
        self.sub = rospy.Subscriber('joy', Joy, self.joy_callthrow, queue_size = 1)
        self.header = Header()
        self.pose = Pose()
        self.point = Point()
        self.quaternion = Quaternion()
        self.info = MapMetaData()
        self.bar = OccupancyGrid()
        self.header.seq = 0
        im = Image.open("./tinpopo.jpg")
        rgb_im = im.convert('RGB')
        self.size = rgb_im.size
        im2 = Image.new('RGBA', self.size)
        self.hoge = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                r, g, b  = rgb_im.getpixel((x,y))
                r = r * 100 / 255
                self.hoge.append(r)
    
    def joy_callthrow(self, msg):
        print msg
        self.x -= msg.axes[3] * 0.1
        self.y += msg.axes[4] * 0.1

    def run(self):
        while not rospy.is_shutdown():
            self.header.seq += 1
            self.header.stamp = rospy.Time.now()
            self.header.frame_id = 'map'
            
            self.point.x = self.x 
            self.point.y = self.y
            self.point.z = 0.0

            self.quaternion.x = 0.0
            self.quaternion.y = 0.0
            self.quaternion.z = 0.0
            self.quaternion.w = 1.0

            self.pose.position = self.point
            self.pose.orientation = self.quaternion

            self.info.map_load_time = rospy.Time.now()
            self.info.resolution = 0.1
            self.info.width = self.size[0]
            self.info.height = self.size[1]
            self.info.origin = self.pose

            self.bar.info = self.info
            self.bar.header = self.header
            self.bar.data = self.hoge
            self.pub.publish(self.bar)

if __name__ == '__main__':
    h = map()
    h.run()
