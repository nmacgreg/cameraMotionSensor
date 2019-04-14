#!/usr/bin/python3

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
                         #'readOnly': True,
                     }))

        logging.debug('starting the sensor update looping task')
        self.sensor_update_task = \
            get_event_loop().create_task(self.update_level())

    async def update_level(self):
        try:
            while True:
                await sleep(3)
                new_level = self.read_motion()
                logging.debug('setting motion detection: %s', new_level)
                self.level.notify_of_external_update(new_level)
        except CancelledError:
            # We have no cleanup to do on cancellation so we can just halt the
            # propagation of the cancellation exception and let the method end.
            logging.debug('auto-update has been cancelled')
            pass
        except: 
            logging.debug('Unexpected error: ', sys.exc_info()[0])
            raise
    
    def cancel_update_level_task(self):
        self.sensor_update_task.cancel()
        get_event_loop().run_until_complete(self.sensor_update_task)

    @staticmethod
    def read_motion():
        # test for the existence of a file
        exists = os.path.isfile('/tmp/motion_detected')
        return exists
        

def run_server():
    # Create a thing that represents my ultrasonic water depth sensor
    sensor = CameraMotionSensor()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([sensor], 'DepthDevice'), port=8885)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        sensor.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()


