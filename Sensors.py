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


class IcarusData(object):
    """
    Adapted from:
    my_vehicle.py
    © Copyright 2015-2016, 3D Robotics.

    Custom Vehicle subclass to peform data sensor fusion from MAVLINK Common Message.
    The Sensors readings for the usual GPS, barometer, and 9DOF sensor setup.
    This contains the true raw values without any scaling to allow data capture and system debugging.
    http://mavlink.org/messages/common
    """

    def __init__(self, time_unix_usec=None, millis=None, ax=None, ay=None, az=None, gx=None, gy=None,
                 gz=None, mx=None, my=None, mz=None, accx=None, accy=None, accz=None, gyrox=None, gyroy=None,
                 gyroz=None, magx=None, magy=None, magz=None, roll_rate=None, pitch_rate=None, yaw_rate=None,
                 roll=None, pitch=None, yaw=None, x=None, y=None, z=None, vx=None, vy=None, vz=None, lat=None,
                 lon=None, alt=None, relative_alt=None, gps_vx=None, gps_vy=None, gps_vz=None, hdg=None, speed=None,
                 latitude=None, longitude=None, altitude=None, course=None, hdop=None, vdop=None, fix=None,
                 sat_view=None, airspeed=None, groundspeed=None, heading=None, throttle=None, barometer=None,
                 climb=None, press_abs=None, press_diff=None, temp=None, desired_roll=None, desired_pitch=None,
                 desired_heading=None, target_bearing=None, wp_dist=None, alt_error=None, aspd_error=None,
                 xtrack_error=None, snr=None, vibration_x=None, vibration_y=None, vibration_z=None):
        """
        Sensors object constructor.
        """
        self.time_unix_usec = time_unix_usec
        # self.date = date
        self.millis = millis
        self.ax = ax
        self.ay = ay
        self.az = az
        self.gx = gx
        self.gy = gy
        self.gz = gz
        self.mx = mx
        self.my = my
        self.mz = mz
        self.accx = accx
        self.accy = accy
        self.accz = accz
        self.gyrox = gyrox
        self.gyroy = gyroy
        self.gyroz = gyroz
        self.magx = magx
        self.magy = magy
        self.magz = magz
        self.roll_rate = roll_rate
        self.pitch_rate = pitch_rate
        self.yaw_rate = yaw_rate
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.relative_alt = relative_alt
        self.gps_vx = gps_vx
        self.gps_vy = gps_vy
        self.gps_vz = gps_vz
        self.hdg = hdg  # Heading
        self.speed = speed
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.course = course  # That is the direction of movement in degrees, not heading.
        self.hdop = hdop
        self.vdop = vdop
        self.fix = fix
        self.sat_view = sat_view
        self.airspeed = airspeed
        self.groundspeed = groundspeed
        self.heading = heading  # Heading in degrees
        self.throttle = throttle
        self.barometer = barometer
        self.climb = climb
        self.press_abs = press_abs
        self.press_diff = press_diff
        self.temp = temp
        self.desired_roll = desired_roll
        self.desired_pitch = desired_pitch
        self.desired_heading = desired_heading
        self.target_bearing = target_bearing
        self.wp_dist = wp_dist
        self.alt_error = alt_error
        self.aspd_error = aspd_error
        self.xtrack_error = xtrack_error
        self.snr = snr
        self.flag = False
        self.vibration_x = vibration_x
        self.vibration_y = self.vibration_y
        self.vibration_z = self.vibration_z

    def __str__(self):
        """
        String representation of the Sensors object
        :param return: Object IcarusData
        """
        values = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                 "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                 "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                 "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                 "%s, %s, %s, %s, %s, %s, %s, %s\n" \
                 % (
                     self.time_unix_usec, self.millis, self.ax, self.ay, self.az, self.gx, self.gy, self.gz,
                     self.mx, self.my, self.mz, self.accx, self.accy, self.accz, self.gyrox, self.gyroy, self.gyroz,
                     self.magx, self.magy, self.magz, self.roll_rate, self.pitch_rate, self.yaw_rate, self.roll,
                     self.pitch, self.yaw, self.x, self.y, self.z, self.vx, self.vy, self.vz, self.lat, self.lon,
                     self.alt, self.relative_alt, self.gps_vx, self.gps_vy, self.gps_vz, self.hdg, self.speed,
                     self.latitude, self.longitude, self.altitude, self.course, self.hdop, self.vdop, self.fix,
                     self.sat_view, self.airspeed, self.groundspeed, self.heading, self.throttle, self.barometer,
                     self.climb, self.press_abs, self.press_diff, self.temp, self.desired_roll, self.desired_pitch,
                     self.desired_heading, self.target_bearing, self.wp_dist, self.alt_error, self.aspd_error,
                     self.xtrack_error, self.snr, self.vibration_x, self.vibration_y, self.vibration_z)
        return values

    def export_csv(self):
        """
        Write csv file
        """
        import csv
        import os
        from datetime import datetime

        date = datetime.now().strftime("%Y-%m-%d-%H")
        file_path = str("input/" + date + "h.csv")
        try:
            with open(file_path, 'a') as csvfile:
                fieldnames = ['SYSTEM_TIME_time_unix_usec', 'SYSTEM_TIME_millis',
                              'IMU1_ax', 'IMU1_ay', 'IMU1_az', 'IMU1_gx', 'IMU1_gy', 'IMU1_gz', 'IMU1_mx', 'IMU1_my',
                              'IMU1_mz', 'IMU2_ax', 'IMU2_ay', 'IMU2_az', 'IMU2_gx', 'IMU2_gy', 'IMU2_gz', 'IMU2_mx',
                              'IMU2_my', 'IMU2_mz', 'ATTITUDE_roll_rate', 'ATTITUDE_pitch_rate', 'ATTITUDE_yaw_rate',
                              'ATTITUDE_roll', 'ATTITUDE_pitch', 'ATTITUDE_yaw', 'INS_x', 'INS_y', 'INS_z', 'INS_vx',
                              'INS_vy', 'INS_vz', 'GPS_lat', 'GPS_lon', 'GPS_alt', 'GPS_relative_alt', 'GPS_vx',
                              'GPS_vy', 'GPS_vz', 'GPS_hdg', 'GPS_RAW_INT_speed', 'GPS_RAW_INT_latitude',
                              'GPS_RAW_INT_longitude', 'GPS_RAW_INT_altitude', 'GPS_RAW_INT_course',
                              'GPS_RAW_INT_hdop', 'GPS_RAW_INT_vdop', 'GPS_RAW_INT_fix', 'GPS_RAW_INT_sat_view',
                              'VFR_HUD_airspeed', 'VFR_HUD_groundspeed', 'VFR_HUD_heading', 'VFR_HUD_throttle',
                              'VFR_HUD_barometer', 'VFR_HUD_climb', 'SCALED_PRESSURE_press_abs',
                              'SCALED_PRESSURE_press_diff', 'SCALED_PRESSURE_temp', 'NAV_CTRL_OUT_desired_roll',
                              'NAV_CTRL_OUT_desired_pitch', 'NAV_CTRL_OUT_desired_heading',
                              'NAV_CTRL_OUT_target_bearing', 'NAV_CTRL_OUT_wp_dist', 'NAV_CTRL_OUT_alt_error',
                              'NAV_CTRL_OUT_aspd_error', 'NAV_CTRL_OUT_xtrack_error', 'GPS_STATUS_satellite_snr',
                              'vibration_x', 'vibration_y', 'vibration_z']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # If file is empty write headers
                if 0 == os.stat(file_path).st_size:
                    writer.writeheader()

                # Fields
                writer.writerow({'SYSTEM_TIME_time_unix_usec': str(self.time_unix_usec),
                                 'SYSTEM_TIME_millis': self.millis,

                                 'IMU1_ax': self.ax, 'IMU1_ay': self.ay,   # RAW_IMU
                                 'IMU1_az': self.az, 'IMU1_gx': self.gx, 'IMU1_gy': self.gy, 'IMU1_gz': self.gz,
                                 'IMU1_mx': self.mx, 'IMU1_my': self.my, 'IMU1_mz': self.mz,

                                 'IMU2_ax': self.accx, 'IMU2_ay': self.accy, 'IMU2_az': self.accz,  # SCALED_IMU
                                 'IMU2_gx': self.gyrox, 'IMU2_gy': self.gyroy, 'IMU2_gz': self.gyroz,
                                 'IMU2_mx': self.magx, 'IMU2_my': self.magy, 'IMU2_mz': self.magz,

                                 'ATTITUDE_roll_rate': self.roll_rate, 'ATTITUDE_pitch_rate': self.pitch_rate,
                                 'ATTITUDE_yaw_rate': self.yaw_rate, 'ATTITUDE_roll': self.roll,
                                 'ATTITUDE_pitch': self.pitch, 'ATTITUDE_yaw': self.yaw,

                                 'INS_x': self.x, 'INS_y': self.y, 'INS_z': self.z,
                                 'INS_vx': self.vx, 'INS_vy': self.vy, 'INS_vz': self.vz,

                                 'GPS_lat': self.lat, 'GPS_lon': self.lon, 'GPS_alt': self.alt,
                                 'GPS_relative_alt': self.relative_alt, 'GPS_vx': self.gps_vx,
                                 'GPS_vy': self.gps_vy, 'GPS_vz': self.gps_vz, 'GPS_hdg': self.hdg,

                                 'GPS_RAW_INT_speed': self.speed, 'GPS_RAW_INT_latitude': self.latitude,
                                 'GPS_RAW_INT_longitude': self.longitude, 'GPS_RAW_INT_altitude': self.altitude,
                                 'GPS_RAW_INT_course': self.course, 'GPS_RAW_INT_hdop': self.hdop,
                                 'GPS_RAW_INT_vdop': self.vdop, 'GPS_RAW_INT_fix': self.fix,
                                 'GPS_RAW_INT_sat_view': self.sat_view,

                                 'VFR_HUD_airspeed': self.airspeed, 'VFR_HUD_groundspeed': self.groundspeed,
                                 'VFR_HUD_heading': self.heading, 'VFR_HUD_throttle': self.throttle,
                                 'VFR_HUD_barometer': self.barometer, 'VFR_HUD_climb': self.climb,

                                 'SCALED_PRESSURE_press_abs': self.press_abs,
                                 'SCALED_PRESSURE_press_diff': self.press_diff, 'SCALED_PRESSURE_temp': self.temp,

                                 'NAV_CTRL_OUT_desired_roll': self.desired_roll,
                                 'NAV_CTRL_OUT_desired_pitch': self.desired_pitch,
                                 'NAV_CTRL_OUT_desired_heading': self.desired_heading,
                                 'NAV_CTRL_OUT_target_bearing': self.target_bearing,
                                 'NAV_CTRL_OUT_wp_dist': self.wp_dist, 'NAV_CTRL_OUT_alt_error': self.alt_error,
                                 'NAV_CTRL_OUT_aspd_error': self.aspd_error,
                                 'NAV_CTRL_OUT_xtrack_error': self.xtrack_error,

                                 'GPS_STATUS_satellite_snr': self.snr,

                                 'vibration_x': self.vibration_x,
                                 'vibration_y': self.vibration_y,
                                 'vibration_z': self.vibration_z
                                 })
        except Exception as e:
            raise "Could not open %s. An error was detected: %s" % (file_path, e)
