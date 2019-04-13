#!/usr/bin/python3

# https://hacks.mozilla.org/2018/05/creating-web-things-with-python-node-js-and-java/
# I want to create a binary Thing, that can exist in one of two modes: { Motion, No Motion } aka { True, False}
# This Thing has a query interface: you can ask it for it's current state (is motion detected, or not?)
# 
# This Thing has an update interface: you can tell it what state to assume. 
# 
# The idea is to have the "motion" software use an external command, to inform this Thing whenever a motion
# event starts or stops


from webthing import (Action, Event, MultipleThings, Property, Thing, Value,
                              WebThingServer)
import logging


# Define our thing

# This Thing includes an event
class MotionEvent(Event): 
    def __init__(self,thing,data):
        Event.__init__(self, thing, 'motion', data=data)


# This is a motion sensor, based on a camera, and the software called "motion"
class cameraMotionSensor(Thing):
    def __init__(self):
        Thing.__init__(self, 'Motion Sensor', ['binarySensor'], 'Garage Motion Sensor')
        

        self.motion_status = False # initialization

         
        # https://iot.mozilla.org/wot/#property-resource
        # define the properties of our thing
        self.add_property(
            Property(self,
             'motion',
             Value(self.get_motion(), self.set_motion(self.motion_status)),
             metadata={
                 '@type': 'MotionProperty',
                 'label': 'Garage Motion Sensor',
                 'description': 'Motion detection within the garage, via camera data',
                 'type': 'boolean',

             }))

    def get_motion(self):
        return self.motion_status

    
    def set_motion(self,value):
        self.motion_status = value  # if value == or value == false (maybe the values On or Off apply to to a motion sensor? 
        return self.motion_status


def run_server():
    # Create a thing that represents a motion sensor
    sensor = cameraMotionSensor()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([sensor], 'cameraMotionSensor'), port=8885)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')

if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()

