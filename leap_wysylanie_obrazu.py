################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
import sys
import Leap
import thread
import time
import ctypes
import rospy
import roslib
import numpy as np
import sensor_msgs.msg
import std_msgs.msg
import Image
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import string

rospy.init_node('leap_kamery')
pub_left = rospy.Publisher('kamera_lewa', sensor_msgs.msg.Image)
pub_right = rospy.Publisher('kamera_prawa', sensor_msgs.msg.Image)
pub_stereo = rospy.Publisher('stereo', sensor_msgs.msg.CameraInfo)



class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

        # Enable camera images
        controller.set_policy(Leap.Controller.POLICY_IMAGES);
        controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        self.frame = frame


        imgs = self.frame.images
        image_left = imgs[0]
        image_right = imgs[1]

        leap_encoding = ['mono8']

####### Publisher left

        leap_obraz = sensor_msgs.msg.Image()
        leap_obraz.height = image_left.height
        leap_obraz.width = image_left.width
        leap_obraz.encoding = "mono8"
        leap_obraz.is_bigendian = 1
        leap_obraz.step = image_left.width
        
        imdata = ctypes.cast(image_left.data.cast().__long__(), ctypes.POINTER(image_left.width*image_left.height*ctypes.c_ubyte)).contents

        #print list(np.array(imdata,'B')
        leap_obraz.data=str(bytearray(np.array(imdata,'B').tolist()))
        #leap_obraz.data=str(imdata)        
        #print leap_obraz.data
        #obraz_z_kamery_left=np.reshape(np.array(imdata,'int'),(image_left.height,image_left.width))

        #leap_obraz.data = str(np.array(obraz_z_kamery_left).tolist())
        #leap_obraz.data=str(imdata)        
        #leap_obraz.data=str(obraz_z_kamery_left.data.view('uint8')[:,::4])

        h = std_msgs.msg.Header()
        h.stamp = rospy.Time.now()
        leap_obraz.header = h

        pub_left.publish(leap_obraz)

####### Publisher stereo
	
        D = [-0.004005, 0.0028, 0.000323,0]
        K = [[61.496921, 0, 140.872031],[ 0, 61.573815, 112.621188],[ 0, 0, 1]]
        R = [[0.999983, 0.002757, 0.00513],[ -0.002759, 0.999996, 0.000278],[ -0.005129, -0.000293, 0.999987]]
        P = [[69.014347, 0, 138.582992, 0],[0, 69.014347, 112.596736, 0],[ 0, 0, 1, 0]]
        leap_image = sensor_msgs.msg.CameraInfo()
        leap_image.height = image_left.height
        leap_image.width = image_left.width
        leap_image.distortion_model = "plumb_bob"
        leap_image.D = D
        leap_image.K = K
        leap_image.R = R
        leap_image.P = P
        leap_image.binning_x = 1
        leap_image.binning_y = 1

        leap_image.roi=sensor_msgs.msg.RegionOfInterest()
        leap_image.roi.x_offset = 0
        leap_image.roi.y_offset = 0
        leap_image.roi.height = image_left.height
        leap_image.roi.width = image_left.width
        leap_image.roi.do_rectify = False

        h = std_msgs.msg.Header()
        h.stamp = rospy.Time.now()
        leap_image.header = h

#        pub_stereo.publish(leap_image)


#        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
#              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

#        # Get hands
#        for hand in frame.hands:

#            handType = "Left hand" if hand.is_left else "Right hand"

#            print "  %s, id %d, position: %s" % (
#                handType, hand.id, hand.palm_position)

#            # Get the hand's normal vector and direction
#            normal = hand.palm_normal
#            direction = hand.direction

#            # Calculate the hand's pitch, roll, and yaw angles
#            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
#                direction.pitch * Leap.RAD_TO_DEG,
#                normal.roll * Leap.RAD_TO_DEG,
#                direction.yaw * Leap.RAD_TO_DEG)

#            # Get arm bone
#            arm = hand.arm
#            print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
#                arm.direction,
#                arm.wrist_position,
#                arm.elbow_position)

#            # Get fingers
#            for finger in hand.fingers:

#                print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
#                    self.finger_names[finger.type()],
#                    finger.id,
#                    finger.length,
#                    finger.width)

#                # Get bones
#                for b in range(0, 4):
#                    bone = finger.bone(b)
#                    print "      Bone: %s, start: %s, end: %s, direction: %s" % (
#                        self.bone_names[bone.type],
#                        bone.prev_joint,
#                        bone.next_joint,
#                        bone.direction)

#        # Get tools
#        for tool in frame.tools:

#            print "  Tool id: %d, position: %s, direction: %s" % (
#                tool.id, tool.tip_position, tool.direction)

#        # Get gestures
#        for gesture in frame.gestures():
#            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
#                circle = CircleGesture(gesture)

#                # Determine clock direction using the angle between the pointable and the circle normal
#                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
#                    clockwiseness = "clockwise"
#                else:
#                    clockwiseness = "counterclockwise"

#                # Calculate the angle swept since the last frame
#                swept_angle = 0
#                if circle.state != Leap.Gesture.STATE_START:
#                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
#                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

#                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
#                        gesture.id, self.state_names[gesture.state],
#                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

#            if gesture.type == Leap.Gesture.TYPE_SWIPE:
#                swipe = SwipeGesture(gesture)
#                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
#                        gesture.id, self.state_names[gesture.state],
#                        swipe.position, swipe.direction, swipe.speed)

#            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
#                keytap = KeyTapGesture(gesture)
#                print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
#                        gesture.id, self.state_names[gesture.state],
#                        keytap.position, keytap.direction )

#            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
#                screentap = ScreenTapGesture(gesture)
#                print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
#                        gesture.id, self.state_names[gesture.state],
#                        screentap.position, screentap.direction )

#        if not (frame.hands.is_empty and frame.gestures().is_empty):
#            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
