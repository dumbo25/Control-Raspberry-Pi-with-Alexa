#########################
#
# Python module to print messages to a log file
#
# this should probably be replaced with python module: logger
#
# The intent is for this to be imported into another script
#
#########################

#########################
import time
import datetime

global LogObject

def setLogObject(o):
    global LogObject

    LogObject = o

def getLogObject():
    return LogObject

#########################
class mylog:
    def __init__(self, path, logfile):
        self.Path = path
        self.LogFile = self.Path + "/" + logfile
        # changing to append so it can be added to action scripts
        self.LogFileObject = open(self.LogFile, 'a+')
        self.Debug = False

    def closeLogFile(self):
        self.LogFileObject.close()

    def setDebug(self, debug):
        self.Debug = debug

    # Log messages should be time stamped
    def timeStamp(self):
        t = time.time()
        s = datetime.datetime.fromtimestamp(t).strftime('%Y/%m/%d %H:%M:%S - ')
        return s

    # Write messages in a standard format
    def printMsg(self, s):
        if s == '':
            self.LogFileObject.write("\n")
        else:
            self.LogFileObject.write(self.timeStamp() + s + "\n")
            if self.Debug:
                print(self.timeStamp() + s)

        self.LogFileObject.flush()

