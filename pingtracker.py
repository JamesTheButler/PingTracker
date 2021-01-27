import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter as strFormatter
import numpy as np
from numpy import random
from collections import deque
from tcp_latency import measure_latency
import threading
  
maxGoodPing = 50
minBadPing = 100
entryCount = 50
pingInterval = 1
timeout = 500
host = "8.8.8.8"

def GetPing():
    ping = measure_latency(host = host, runs=1, timeout = timeout/1000)[0]
    if(ping == None):
        return timeout
    else:
        return round(ping)

def GetPlotColor(ping):
    if ping>maxGoodPing:
        if ping>minBadPing:
            return 'r'
        else:
            return 'y'
    else: 
        return 'g'

def Main():
    timeScale = range(0, entryCount)
    pingEntries = deque(np.full(entryCount, 0))

    plt.rcParams['toolbar'] = 'None' 
    
    fig = plt.gcf()
    fig.canvas.set_window_title('Pinging ' + host)

    # plot limits
    plt.ylim(0, timeout+10)
    plt.xlim(50, 0-1)
    # vertical lines
    plt.axvline(x=0, color= '#808080', linewidth = 0.5)
    plt.axvline(x=10, color= '#808080', linewidth = 0.5)
    plt.axvline(x=20, color= '#808080', linewidth = 0.5)
    plt.axvline(x=30, color= '#808080', linewidth = 0.5)
    plt.axvline(x=40, color= '#808080', linewidth = 0.5)
    # horizontal lines
    plt.axhline(y=100, color= '#808080', linewidth = 0.5)
    plt.axhline(y=200, color= '#808080', linewidth = 0.5)
    plt.axhline(y=300, color= '#808080', linewidth = 0.5)
    plt.axhline(y=400, color= '#808080', linewidth = 0.5)
    # threshold lines
    #plt.axhline(y=maxGoodPing, color= '#bfc257', linewidth = 1)
    #plt.axhline(y=minBadPing, color= '#e37f7f', linewidth = 1)

    plt.gca().xaxis.set_major_formatter(strFormatter('%d s'))
    plt.gca().yaxis.set_major_formatter(strFormatter('%d ms'))


    while True:
        currentPing = GetPing()

        pingEntries.rotate(1)
        pingEntries[0] = currentPing
        plotColor = GetPlotColor(currentPing)

        pingText = plt.text(5, 480, str(currentPing) + ' ms', color = plotColor, fontweight='bold')
        line, = plt.plot(timeScale, pingEntries, color = plotColor, linewidth = 3) 
        point = plt.scatter(timeScale[0], pingEntries[0], color = plotColor)
        plt.pause(pingInterval - (currentPing/1000))
        line.remove()
        del line
        point.remove()
        del point
        pingText.remove()
        del pingText

##############################

#b = threading.Thread(name='background', target=Main)
#f = threading.Thread(name='foreground', target=foreground)
#
#b.start()
#f.start()
#
Main()