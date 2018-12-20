from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math

class DroneKit:

    vehicle = None

    def __init__(self):
        # settings
        connectionString = '127.0.0.1:14540' # or 14550
        MAV_MODE_AUTO = 4
        # Parse connection argument
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--connect", help="connection string")
        args = parser.parse_args()
        if args.connect:
            connectionString = args.connect
        # init
        # Connect to the Vehicle
        print("Connecting")
        print(connectionString)
        self.vehicle = connect(connectionString, wait_ready=True)

        print("Пущ-пущ-пущ!")
        print(" Mode: %s" % vehicle.mode.name)

        return None

    def PX4setMode(mavMode):
        self.vehicle._master.mav.command_long_send(self.vehicle._master.target_system, self.vehicle._master.target_component,
                                                mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
                                                mavMode,
                                                0, 0, 0, 0, 0, 0)

    def getLocationOffsetMeters(original_location, dNorth, dEast, alt):
        """
        Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
        specified `original_location`. The returned Location adds the entered `alt` value to the altitude of the `original_location`.
        The function is useful when you want to move the vehicle around specifying locations relative to
        the current vehicle position.
        The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
        For more information see:
        http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
        """
        earthRadius = 6378137.0 #Radius of "spherical" earth
        #Coordinate offsets in radians
        dLat = dNorth / earthRadius
        dLon = dEast / (earthRadius * math.cos(math.pi * original_location.lat / 180))
        #New position in decimal degrees
        newlat = original_location.lat + (dLat * 180/math.pi)
        newlon = original_location.lon + (dLon * 180/math.pi)
        return LocationGlobal(newlat, newlon,original_location.alt + alt)


'''
################################################################################################
# Init
################################################################################################

################################################################################################
# Listeners
################################################################################################

home_position_set = False

#Create a message listener for home position fix
@vehicle.on_message('HOME_POSITION')
def listener(self, name, home_position):
    global home_position_set
    home_position_set = True

################################################################################################
# Start mission example
################################################################################################

# wait for a home position lock
while not home_position_set:
    print "Waiting for home position..."
    time.sleep(1)

# Display basic vehicle state
print " Type: %s" % vehicle._vehicle_type
print " Armed: %s" % vehicle.armed
print " System status: %s" % vehicle.system_status.state
print " GPS: %s" % vehicle.gps_0
print " Alt: %s" % vehicle.location.global_relative_frame.alt

# Change to AUTO mode
PX4setMode(MAV_MODE_AUTO)
time.sleep(1)

# Load commands
cmds = vehicle.commands
cmds.clear()

home = vehicle.location.global_relative_frame

# takeoff to 10 meters
wp = getLocationOffsetMeters(home, 0, 0, 10)
cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
cmds.add(cmd)

# move 10 meters north
wp = getLocationOffsetMeters(wp, 10, 0, 0)
cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
cmds.add(cmd)

# move 10 meters east
wp = getLocationOffsetMeters(wp, 0, 10, 0)
cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
cmds.add(cmd)

# move 10 meters south
wp = getLocationOffsetMeters(wp, -10, 0, 0)
cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
cmds.add(cmd)

# move 10 meters west
wp = getLocationOffsetMeters(wp, 0, -10, 0)
cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
cmds.add(cmd)

# land
wp = getLocationOffsetMeters(home, 0, 0, 10)
cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
cmds.add(cmd)

# Upload mission
cmds.upload()
time.sleep(2)

# Arm vehicle
vehicle.armed = True

# monitor mission execution
nextwaypoint = vehicle.commands.next
while nextwaypoint < len(vehicle.commands):
    if vehicle.commands.next > nextwaypoint:
        display_seq = vehicle.commands.next+1
        print "Moving to waypoint %s" % display_seq
        nextwaypoint = vehicle.commands.next
    time.sleep(1)

# wait for the vehicle to land
while vehicle.commands.next > 0:
    time.sleep(1)

# Disarm vehicle
vehicle.armed = False
time.sleep(1)

# Close vehicle object before exiting script
vehicle.close()
time.sleep(1)
'''
