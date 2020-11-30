#!/bin/sh
# run using: sudo bash getScripts.sh

# get the fauxmo scripts
cd /usr/local/bin
wget https://raw.githubusercontent.com/dumbo25/Control-Raspberry-Pi-with-Alexa/master/fauxmo.py
wget https://raw.githubusercontent.com/dumbo25/Control-Raspberry-Pi-with-Alexa/master/mylog.py 
wget https://raw.githubusercontent.com/dumbo25/Control-Raspberry-Pi-with-Alexa/master/rpi-echo.py
wget https://raw.githubusercontent.com/dumbo25/Control-Raspberry-Pi-with-Alexa/master/disarm.py 
wget https://raw.githubusercontent.com/dumbo25/Control-Raspberry-Pi-with-Alexa/master/sleep.py 

# make the sripts executable
sudo chmod +x fauxmo.py
sudo chmod +x mylog.py
sudo chmod +x rpi-echo.py
sudo chmod +x disarm.py 
sudo chmod +x sleep.py 

