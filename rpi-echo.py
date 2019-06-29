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
        if name == "home hub on":
            # Alexa, turn on home hub; or Alexa, turn home hub on
            Log.printMsg("act: on " + name + " from client @ " + str(client_address))
        elif name == "home hub off":
            # Alexa, turn off home hub; or Alexa, turn home hub off
            Log.printMsg("act: off " + name + " from client @ " + str(client_address))
        elif name == "home hub shutdown":
            # Alexa, turn on home hub shutdown
            Log.printMsg("act: shutdown " + name + " from client @ " + str(client_address))
            cmd = "sudo shutdown -h 0"
            subprocess.call(cmd, shell=True)
        elif name == "home hub restart":
            # Alexa, turn on home hub restart
            Log.printMsg("act: reboot " + name + " from client @ " + str(client_address))
            cmd = "sudo reboot"
            subprocess.call(cmd, shell=True)
        else:
            Log.printMsg("unhandled command received: " + name)
        return True


if __name__ == "__main__":
    Log.printMsg("Stating wemo server")
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()

    # Name the device and the action and unique port
    fauxmo.fauxmo("home hub on", u, p, None, 5001, d)
    fauxmo.fauxmo("home hub off", u, p, None, 5002, d)
    fauxmo.fauxmo("home hub shutdown", u, p, None, 5003, d)
    fauxmo.fauxmo("home hub restart", u, p, None, 5004, d)

    # Loop and poll for incoming Echo requests
    Log.printMsg("Entering wemo polling loop")
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
        Log.printMsg("Stopping wemo server")
        Log.closeLogFile()
