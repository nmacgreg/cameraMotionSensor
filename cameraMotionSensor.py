#!/usr/bin/python

# https://hacks.mozilla.org/2018/05/creating-web-things-with-python-node-js-and-java/
# I want to create a binary Thing, that can exist in one of two modes: { Motion, No Motion } aka { True, False}
# This Thing has a query interface: you can ask it for it's current state (is motion detected, or not?)
# 
# This Thing has an update interface: you can tell it what state to assume. 
# 
# The idea is to have the "motion" software use an external command, to inform this Thing whenever a motion
# event starts or stops


from webthing import Action, Event, Property, Thing, Value, WebThingServer

# Define our thing

# This Thing includes an event
class MotionEvent(Event): 
    def __init__(self,thing,data):
        Event.__init__(self, thing, 'motion', data=data)


# This is a motion sensor, based on a camera, and the software called "motion"
class cameraMotionSensor(Thing):
    def __init__(self):
        Thing.__init__(self, 'Motion Sensor', 'motionSensor', 'Camera Motion Sensor')

        status = self.get_status()

        
        # https://iot.mozilla.org/wot/#property-resource
        # define the properties of our thing
        self.add_property(
            Property(self,
             'motion',
             Value(self.get_motion(status), self.set_motion),
             metadata={
                 'type': 'boolean',
                 'description': 'state of motion',
             }))
