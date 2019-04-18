#!/usr/bin/python3
# Most helpful references: 
# https://iot.mozilla.org/wot/
# https://github.com/mrstegeman/virtual-things-adapter/blob/c94c0e239ff2051a794085905995c26764e83253/virtual-things-adapter.js

from asyncio import sleep, CancelledError, get_event_loop
from webthing import (Action, Event, MultipleThings, Property, Thing, Value,
                      WebThingServer)
import logging
import random
import time
import uuid
import os

class CameraMotionSensor(Thing):
    """A motion sensor based on motion detection triggered by a camera, which updates its measurement every few seconds."""

    def __init__(self):
        Thing.__init__(self, 'Motion Sensor', ['MotionSensor'], 'Motion detection based on video cam')

        self.level = Value(False)
        self.add_property(
            Property(self,
                     'motion',
                     self.level,
                     metadata={
                         '@type': 'MotionProperty',
                         'label': 'Motion',
                         'type': 'boolean',
                         'description': 'Motion detection based on camera data',
                     }))

def run_server():
    # Create a thing that represents my ultrasonic water depth sensor
    sensor = CameraMotionSensor()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([sensor], 'DepthDevice'), port=8884)
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


