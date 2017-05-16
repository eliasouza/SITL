#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Computer Engineering Section
The Military Institute of Engineering
Rio de Janeiro, Brazil
June 28, 2016
author: Elias Gonçalves
email: esgoncalves@ime.eb.br
"""

from Vehicle import Icarus
import dronekit
from dronekit import connect
import socket
import exceptions
import logging
import time
from subprocess import call

try:
    # Start logging
    logging.basicConfig(filename='input/icarus_exec.log', format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S', level=logging.INFO)  # %m/%d/%Y %I:%M:%S %p

    # Connect to the Vehicle
    vehicle = connect('127.0.0.1:14551', wait_ready=True, vehicle_class=Icarus)

    # Logging vehicle info
    logging.info("Autopilot Firmware version: %s" % vehicle.version)
    logging.info(vehicle.battery)
    logging.info("Channels: %s" % vehicle.channels)

    # Callback method
    def sensor_data_callback(self, attr_name, obj_values):
        if not obj_values.flag:
            obj_values.flag = True

    logging.info("Vehicle Home: %s" % vehicle.home_location)

    logging.info("Waiting for mode AUTO...")
    while not vehicle.mode.name == 'AUTO':
        time.sleep(1)

    logging.info("Waiting for arming...")
    while not vehicle.armed:
        time.sleep(1)

    logging.info("Starting mission...")
    vehicle.add_attribute_listener('sensor_data', sensor_data_callback)
    call(["./imu"])

    while vehicle.armed:
        time.sleep(2)

    logging.info("Mission Finished.")
    call(["exit"])
    vehicle.remove_attribute_listener('sensor_data', sensor_data_callback)

    # Close vehicle connection
    logging.info(vehicle.battery)
    vehicle.close()

# Bad TCP connection
except socket.error as sk_e:
    logging.WARNING('TCP: No server exists! -> %s' % sk_e)

# Bad TTY connection
except exceptions.OSError as os_e:
    logging.WARNING('TTY: No serial exists! -> %s' % os_e)

# API Error
except dronekit.APIException as dk_e:
    logging.WARNING('API: Timeout! -> %s' % dk_e)

# Other error
except Exception as e:
    logging.WARNING('Other error! -> %s' % e)
