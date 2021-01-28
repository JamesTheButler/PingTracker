import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter as strFormatter
import numpy as np
from collections import deque
from tcp_latency import measure_latency
import signal
from enum import Enum

class PingStatus(Enum):
    NONE = 0
    GOOD = 1
    OK = 2
    BAD = 3

maxGoodPing = 50
minBadPing = 100
entryCount = 1200
pingInterval = 1
timeout = 500
host = "8.8.8.8"
vertLineInterval = 200
horiLineInterval = (int) (timeout / 5)

fullColor = {
    PingStatus.NONE : '#000000',
    PingStatus.GOOD : '#24a60f',
    PingStatus.OK : '#c7db14',
    PingStatus.BAD : '#db1e14',
}
lightColor = {
    PingStatus.NONE : '#3d3d3d',
    PingStatus.GOOD : '#7fc973',
    PingStatus.OK : '#f0eaaf',
    PingStatus.BAD : '#d67f7a',
}

yMin = 0 - (int)(timeout/20)
yMax = timeout + (int)(timeout/20)
xMin = entryCount
xMax = 0 - (int)(entryCount/50)

def GetPing():
    ping = measure_latency(host = host, runs=1, timeout = timeout/1000)[0]
    if(ping == None):
        return timeout
    else:
        return round(ping)

def GetPingStatus(ping):
    if ping > maxGoodPing:
        if ping > minBadPing:
            return PingStatus.BAD
        else:
            return PingStatus.OK
    else: 
        return PingStatus.GOOD

def AddFillTrace(ping):
    pass

def Main():
    # remove matplotlib toolbar
    plt.rcParams['toolbar'] = 'None' 
    
    # set window title
    fig = plt.gcf()
    fig.canvas.set_window_title('Pinging ' + host)

    # plot limits
    plt.ylim(yMin, yMax)
    plt.xlim(xMin, xMax)

    # vertical and horizontal lines
    for i in range(0, yMax, horiLineInterval):
        plt.axhline(y=i, color= '#808080', linewidth = 0.5)
    for i in range(0, xMin, vertLineInterval):
        plt.axvline(x=i, color= '#808080', linewidth = 0.5)
    
    # add seconds/milliseconds to axes
    plt.gca().xaxis.set_major_formatter(strFormatter('%d s'))
    plt.gca().yaxis.set_major_formatter(strFormatter('%d ms'))

    #plt.show()
    interrupted = False
    #def signal_handler(signal, frame):
    #    global interrupted
    #    print("exiting")
    #    interrupted = True
#
    #signal.signal(signal.SIGINT, signal_handler)
    
    timeScale = range(0, entryCount)
    pingEntries = deque(np.full(entryCount, 0))
    while True:
        currentPing = GetPing()

        pingEntries.rotate(1)
        pingEntries[0] = currentPing
        pingStatus = GetPingStatus(currentPing)

        pingText = plt.text(5, timeout-20, str(currentPing) + ' ms', color = fullColor[pingStatus], fontweight='bold')
        line, = plt.plot(timeScale, pingEntries, color = fullColor[pingStatus], linewidth = 3) 
        liveFill = plt.fill_between(timeScale, 0, pingEntries, color = lightColor[pingStatus])
        point = plt.scatter(timeScale[0], pingEntries[0], color = fullColor[pingStatus])

        plt.pause(pingInterval - (currentPing/1000))

        line.remove()
        del line
        point.remove()
        del point
        pingText.remove()
        del pingText
        liveFill.remove()
        del liveFill

        if interrupted:
            print("Exit.")
            break
    
    plt.close()



##############################
Main()