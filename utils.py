# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 16:03:13 2014

@author: Gaspard, Thomas, Arnaud
"""

import time, urllib
from bs4 import BeautifulSoup


debug_mode = True


class Chrono:
    def __init__(self):
        pass
    
    def start(self, nbIterations):
        self.total = nbIterations
        self.strTotal = str( self.total )
        self.i = 0
        self.previous = 0
        self.startTime = time.time()
        self.previousTime = self.startTime
        
    def tick(self, iterations = 1):
        self.i += iterations
    
    def remaining(self):
        t = time.time()
        remaining = int( (self.total - self.i) * (t - self.previousTime) / (self.i - self.previous) )
        self.previous = self.i
        self.previousTime = t
        return remaining
    
    def printRemaining(self):
        debug('Chrono: ' + str( self.i ) + ' / ' + self.strTotal + '  Remaining: ' + prettyPrintTime(self.remaining()) )


def debug(msg):
    if debug_mode:
        print "Debug : " + msg;
    

def printError(msg):
    print "Erreur : " + msg + " !!!";



def printObject(arg, prefix = ""):
    if type(arg) == type(dict()):
        for i in arg:
            printObject( arg[i], prefix + " " + i )
    elif type(arg) == type([]):
            for i in range(len(arg)):
                printObject( arg[i], prefix + " " + str(i+1) )
    else:
        print prefix + " : " + str(arg)



class Clock:
    def __init__(self):
        self.time = 0
    
    def clock(self):
        t = time.time()
        result = t - self.time
        self.time = t
        return result
    
    def strClock(self):
        return "Time: " + str(self.clock())

def prettyPrintTime(s):
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return ('%sh %smin %ssec' % (hours, minutes, seconds) )
    elif minutes > 0:
        return ('%smin %ssec' % (minutes, seconds) )
    else:
        return ('%ssec' % (seconds) )


def urlOpen(url):
    a = urllib.urlopen(url)
    # handle timeout here
    return a

def getDOM(url):
    return BeautifulSoup( urlOpen(url) )


def getHTML(url):
    return urlOpen(url).read()
