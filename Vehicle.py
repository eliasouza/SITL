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

import datetime
from dronekit import Vehicle
from Sensors import IcarusData


class Icarus(Vehicle):
    """
    Adapted from:
    my_vehicle.py
    © Copyright 2015-2016, 3D Robotics.

    Custom Vehicle subclass to peform data sensor fusion from MAVLINK Common Message.
    """

    def __init__(self, *args):
        super(Icarus, self).__init__(*args)

        # Create a Sensor object with initial values set to None.
        self._sensor_data = IcarusData()

        # Create a message listener using the decorator.
        # See: GPS_INPUT, WIND_COV, CONTROL_SYSTEM_STATE, DISTANCE_SENSOR, GPS_RTK, HIGHRES_IMU
        @self.on_message(['SYSTEM_TIME', 'RAW_IMU', 'SCALED_IMU2', 'ATTITUDE', 'LOCAL_POSITION_NED',
                          'GLOBAL_POSITION_INT', 'GPS_RAW_INT', 'GPS_STATUS', 'VFR_HUD', 'SCALED_PRESSURE', 'NAV_CONTROLLER_OUTPUT'])
        def read_mavlink(self, name, message):
            """
            The listener is called for messages that contain the string specified in the decorator,
            passing the vehicle, message name, and the message.

            The listener writes the message to the (newly attached) ``vehicle.sensor_data`` object
            and notifies observers.

            For more details, please go to the url: http://mavlink.org/messages/
            """
            import math

            # Update date and time
            now = datetime.datetime.now()

            if name == 'SYSTEM_TIME':
                self._sensor_data.time_unix_usec = datetime.datetime.fromtimestamp(
                    message.time_unix_usec / 1000000.).strftime('%Y-%m-%d %H:%M:%S.%f')  # %Y%m%d%H%M%S%f
                # self._sensor_data.date = str(now.strftime('%d%m%y%H%M%S'))
                self._sensor_data.millis = message.time_unix_usec  # Timestamp in microseconds since UNIX epoch

                # Allow data export
                if self._sensor_data.flag:
                    self._sensor_data.export_csv()

            # First IMU
            elif name == 'RAW_IMU':
                self._sensor_data.ax = message.xacc
                self._sensor_data.ay = message.yacc
                self._sensor_data.az = message.zacc
                self._sensor_data.gx = message.xgyro
                self._sensor_data.gy = message.ygyro
                self._sensor_data.gz = message.zgyro
                self._sensor_data.mx = message.xmag
                self._sensor_data.my = message.ymag
                self._sensor_data.mz = message.zmag

            # Second IMU
            elif name == 'SCALED_IMU2':
                self._sensor_data.accx = message.xacc
                self._sensor_data.accy = message.yacc
                self._sensor_data.accz = message.zacc
                self._sensor_data.gyrox = message.xgyro
                self._sensor_data.gyroy = message.ygyro
                self._sensor_data.gyroz = message.zgyro
                self._sensor_data.magx = message.xmag
                self._sensor_data.magy = message.ymag
                self._sensor_data.magz = message.zmag

            elif name == 'ATTITUDE':
                self._sensor_data.roll_rate = math.degrees(message.rollspeed)
                self._sensor_data.pitch_rate = math.degrees(message.pitchspeed)
                self._sensor_data.yaw_rate = math.degrees(message.yawspeed)
                self._sensor_data.roll = math.degrees(message.roll)
                self._sensor_data.pitch = math.degrees(message.pitch)
                self._sensor_data.yaw = math.degrees(message.yaw)

            elif name == 'LOCAL_POSITION_NED':
                self._sensor_data.x = message.x
                self._sensor_data.y = message.y
                self._sensor_data.z = message.z
                self._sensor_data.vx = message.vx
                self._sensor_data.vy = message.vy
                self._sensor_data.vz = message.vz

            elif name == 'GLOBAL_POSITION_INT':
                self._sensor_data.lat = message.lat  # degrees * 1E7
                self._sensor_data.lon = message.lon  # degrees * 1E7
                self._sensor_data.alt = message.alt  # meters
                self._sensor_data.relative_alt = message.relative_alt  # meters
                self._sensor_data.gps_vx = message.vx  # m/s * 100
                self._sensor_data.gps_vy = message.vy  # m/s * 100
                self._sensor_data.gps_vz = message.vz  # m/s * 100
                self._sensor_data.hdg = message.hdg  # Heading

            elif name == 'GPS_RAW_INT':
                self._sensor_data.speed = message.vel  # m/s * 100
                self._sensor_data.latitude = message.lat  # degrees * 1E7
                self._sensor_data.longitude = message.lon  # degrees * 1E7
                self._sensor_data.altitude = message.alt  # meter * 1000
                self._sensor_data.course = message.cog  # Direction of movement in degrees, not heading.
                self._sensor_data.hdop = message.eph
                self._sensor_data.vdop = message.epv
                self._sensor_data.fix = message.fix_type
                self._sensor_data.sat_view = message.satellites_visible

            elif name == 'GPS_STATUS':
                self._sensor_data.snr = message.satellite_snr

            elif name == 'VFR_HUD':
                self._sensor_data.airspeed = message.airspeed  # m/s
                self._sensor_data.groundspeed = message.groundspeed  # m/s
                self._sensor_data.heading = message.heading  # Heading in degrees
                self._sensor_data.throttle = message.throttle  # percent
                self._sensor_data.barometer = message.alt  # meters
                self._sensor_data.climb = message.climb  # meters/second

            elif name == 'SCALED_PRESSURE':
               self._sensor_data.press_abs = message.press_abs
               self._sensor_data.press_diff = message.press_diff
               self._sensor_data.temp = message.temperature

            elif name == 'NAV_CONTROLLER_OUTPUT':
                self._sensor_data.desired_roll = message.nav_roll
                self._sensor_data.desired_pitch = message.nav_pitch
                self._sensor_data.desired_heading = message.nav_bearing
                self._sensor_data.target_bearing = message.target_bearing
                self._sensor_data.wp_dist = message.wp_dist
                self._sensor_data.alt_error = message.alt_error
                self._sensor_data.aspd_error = message.aspd_error
                self._sensor_data.xtrack_error = message.xtrack_error

            elif name == 'VIBRATION':
                self._sensor_data.vibration_x = message.vibration_x
                self._sensor_data.vibration_y = message.vibration_y
                self._sensor_data.vibration_z = message.vibration_z


            # Notify all observers of new message (with new value)
            #   Note that argument `cache=False` by default so listeners
            #   are updated with every new message
            self.notify_attribute_listeners('sensor_data', self._sensor_data)

    @property
    def read_mavlink(self):
        return self._sensor_data