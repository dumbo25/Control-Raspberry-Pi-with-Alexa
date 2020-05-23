#!/usr/bin/env python

#########################
#
# Python script using fauxmo to control Raspberry Pi
#
# To Do List:
#   - add to systemd
#   - add as an optional step to raspbian setup
#   - create script to autodeploy
#   - add scripts to github
#   - update to python3
#   - do something useful
#
# The scripts here are based on this Instructable
#   https://www.instructables.com/id/Control-Raspberry-Pi-GPIO-Using-Amazon-Echo-Fauxmo/
#
#########################

#########################
#
# To run the script:
#    $ python rpi-echo.py
#
# Once the script is running, say to Amazon Alexa: Alexa, discover devices
# wait 20 seconds or so
#
# Delete discovered devices from Alexa app on smartphone
# Add new commands in two places below
# Each command needs its own port
#
#########################

#########################
import mylog
global Log
Log = mylog.mylog('/home/pi/rpi-echo', 'rpi-echo.log')
mylog.setLogObject(Log)

import fauxmo
import time
import datetime
import subprocess

#########################
Log.setDebug(True)


def getLogHandler():
#!/usr/bin/env python

#########################
#
# Python script using Amazon Alexa or Echo to control Raspberry Pi using an older version 
# fauxmo. It only supports one device and two commands.
#
# To control a device say:
#
#   Alexa, turn <device> <command>
#
# The scripts here are based on this Instructable
#   https://www.instructables.com/id/Control-Raspberry-Pi-GPIO-Using-Amazon-Echo-Fauxmo/
#
# The script can be run on the command or as a systemd servioce:
# To run the script from the command line use:
#
#    $ python rpi-echo.py
#
# Once the script is running, say to Amazon Alexa: Alexa, discover devices
#
#    $ ps aux | grep rpi-echo
#
#    should show two entries for rpi-echo, one is the command above and the other is the script
#
# Wait for dsicovery to complete
#
# If a mistake is made, then delete discovered devices from Alexa app on smartphone
#
# MAKE THE CHANGES IS INDICATED IN THE CODE BELOW
#
# Nothing else needs to be added to this script or any of the others
#
# be sure to rm *.pyc if any changes are made
#
#########################

#########################
# the following lines must go here, otherwise fauxmo does not initialize properly
import mylog
global Log
Log = mylog.mylog('/home/pi', 'rpi-echo.log')
mylog.setLogObject(Log)

import fauxmo
import time
import datetime
import subprocess

# set to True when debugging, otherwise set to False
Log.setDebug(False)

#   Starting port, which should be greater than 1024. Each command requires a unique port
#   The starting port doesn't need to be changed
startingPort = 5070



# THE BELOW ITEMS SHOULD BE THE ONLY CHANGES REQUIRED

#   Enter your device name for Alex/Echo
device = ['security']

#   These are the actions to be taken when the echo command is received
#
#   The number of actions must equal the number of commands
#
#   An action is any command that can be executed from the command line
#   example actions:
#      sudo shutdown -h 0
#      sudo reboot
#      python script.py
actions = ['python /usr/local/bin/sleep.py', 'python /usr/local/bin/disarm.py']

# THE ABOVE ITEMS SHOULD BE THE ONLY CHANGES REQUIRED


# I modified these lines in fauxmo.py, which hard codes ON and OFF.
# The commented lines are the originals.
#   # success = self.action_handler.on(client_address[0], self.name)
#   success = self.action_handler.on(client_address[0], 'ON')
#
#   # success = self.action_handler.off(client_address[0], self.name)
#   success = self.action_handler.off(client_address[0], 'OFF')
#
# If the commands are changed, then you must change fuaxmo.py
commands = ['ON', 'OFF']

#########################
def getLogHandler():
    return Log

class debounce_handler(object):
    # prevent multiple Echos from responding to one voice command

    DEBOUNCE_SECONDS = 0.3

    def __init__(self):
        self.lastEcho = time.time()

    def on(self, client_address, name):
        if self.debounce():
            return True
        return self.act(client_address, True, name)

    def off(self, client_address, name):
        if self.debounce():
            return True
        return self.act(client_address, False, name)

    def act(self, client_address, state):
        pass

    def debounce(self):
        if (time.time() - self.lastEcho) < self.DEBOUNCE_SECONDS:
            return True

        self.lastEcho = time.time()
        return False


class device_handler(debounce_handler):
    def trigger(self, port, state):
        Log.printMsg('trigger: port: ' + str(port) )

    def act(self, client_address, state, name):
        global commands
	global actions

	notFound = True

        try:
            i = 0
            for cmd in commands:
                if name == cmd:
                    Log.printMsg("action: " + name + " from Echo " + str(client_address))
		    subprocess.call(actions[i], shell=True)
                    notFound = False
                i = i + 1
	except:
            Log.printMsg("rpi-echo: device_handler: act: try failed: " + name)

        if notFound:
            Log.printMsg("unhandled command received: " + name)
        return True

if __name__ == "__main__":
    Log.printMsg("*** STARTING WEMO SERVER ***")

    # setup parameters for fauxmo
    #   Plug-and-Play Listener
    l = fauxmo.upnp_broadcast_responder()
    l.init_socket()

    #   Poller
    p = fauxmo.poller()
    p.add(l)

    #   Register the device callback for handler
    d = device_handler()


    # Name the device
    #   fauxmo.fauxmo corresponds to fauxmo.py: fauxmo: __init__
    port = startingPort
    for dev in device:
        fauxmo.fauxmo(dev, l, p, None, port, d)
        port = port + 1


    # Loop forever waiting for incoming Echo requests
    Log.printMsg("Entering WeMo polling loop")
    try:
        while True:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)


    except Exception, e:
        Log.printMsg("ERROR: critical exception occurred: " + str(e))

    except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
        Log.printMsg("keyboard exception occurred")

    except Exception as ex:
        Log.printMsg("ERROR: an unhandled exception occurred: " + str(ex))

    finally:
        Log.printMsg("** STOPPING WEMO SERVER ***")
        Log.closeLogFile()

