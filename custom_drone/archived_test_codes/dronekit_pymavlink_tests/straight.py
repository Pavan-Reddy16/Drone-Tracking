#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
import multiprocessing
import time
from pymavlink import mavutil

#######################Connection String##################################
import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='tcp:0.0.0.0:5762')
args = parser.parse_args()

connection_string = args.connect
sitl = None
#################################################################################

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

print(vehicle.location.global_frame)

def get_location_metres(original_location, dNorth, dEast):
    
    earth_radius=6378137.0 
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    print(newlat,newlon)
    return LocationGlobal(newlat, newlon,original_location.alt)


def get_distance_metres(aLocation1, aLocation2):
    
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5



def distance_to_current_waypoint():
    
    nextwaypoint = vehicle.commands.next
    if nextwaypoint==0:
        return None
    missionitem=vehicle.commands[nextwaypoint-1] #commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint


def download_mission():
    
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

def adds_square_mission(cur_location, alt, x, y):
    
    cmds = vehicle.commands
    print(" Clear any existing commands")
    cmds.clear() 
    print(" Define/add new commands.")
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, alt))
    point = get_location_metres(cur_location, x, y)
    print(point)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point.lat, point.lon, alt))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point.lat, point.lon, alt))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point.lat, point.lon, alt))

    print(" Upload new commands to vehicle")
    cmds.upload()


def arm_and_takeoff(aTargetAltitude):

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)
    vehicle.groundspeed = 1
    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) 

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)

def get_curr_loc():
    loc = vehicle.location.global_frame
    return [loc.lat, loc.lon]

    
# if __name__ == '__main__':
def mission():
    print("mission")
    print("Enter l, b, altitude and speed in cm/s")
    l, b, alt, speed = [int(x) for x in input().split()]
    # l, b, dist, alt, speed = 10, 10, 10, 10, 300
    radius = math.sqrt(2)*l + 10
    rtl_altitude = alt*100 
    #############################################
    #Set parameters safety part
    vehicle.parameters['WPNAV_SPEED'] = speed
    vehicle.parameters['FENCE_ENABLE'] = 1
    vehicle.parameters['FENCE_RADIUS'] = radius
    vehicle.parameters['FENCE_ACTION'] = 1
    vehicle.parameters['FENCE_ALT_MAX'] = alt + 5
    vehicle.parameters['RTL_ALT'] = rtl_altitude
    vehicle.parameters['RTL_SPEED'] = speed
    # if vehicle.battery.level <= 20 :
    #     vehicle.mode = VehicleMode("RTL")
    
    #############################################
    
    print('Create a new mission (for current location)')
    adds_square_mission(vehicle.location.global_frame,alt,l,b)
    print(vehicle.location.global_frame)
    ###########Takeoff Altitude###################
    arm_and_takeoff(alt)
    ############################################

    print("Starting mission")
    vehicle.commands.next=0
    vehicle.mode = VehicleMode("AUTO")

    while True:
        nextwaypoint=vehicle.commands.next
        print('Distance to waypoint (%s): %s' % (nextwaypoint, distance_to_current_waypoint()))
        if nextwaypoint==vehicle.commands.count: 
            print("Exit 'standard' mission when start heading to final waypoint ")
            break
        if vehicle.battery.level <= 20 :
            vehicle.mode = VehicleMode("RTL")
        time.sleep(1)

    print('Return to launch')
    vehicle.mode = VehicleMode("RTL")


    #Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()


# if __name__ == '__main__':
#     x,y = get_curr_loc()
#     print("current location function :")
#     print(x,y)
#     f2 = multiprocessing.Process(name='f2', target=mission())
#     f2.start()