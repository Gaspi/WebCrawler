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
        self.absoluteTotal = self.total
        self.strTotal = str( self.absoluteTotal )
        self.i = 0
        self.previous = 0
        self.startTime = time.time()
        self.previousTime = self.startTime
    
    def tick(self, iterations = 1):
        self.i += iterations
    
    def decTotal(self, iterations = 1):
        self.total -= 1
    
    def elapsed(self):
        return time.time() - self.startTime
    
    def remaining(self, wholeSegment = True):
        t = time.time()
        remaining = 0
        if wholeSegment:
            remaining = (self.total - self.i) * self.elapsed() / self.i
        else:
            remaining = (self.total - self.i) * (t - self.previousTime) / (self.i - self.previous)
        self.previous = self.i
        self.previousTime = t
        return remaining
    
    def printRemaining(self, wholeSegment = True):
        r = self.remaining(wholeSegment)
        if self.absoluteTotal == self.total:
            debug('Chrono: ' + str( self.i ) + ' / ' + self.strTotal +
                  '  Remaining: ' + prettyPrintTime(r) )
        else:
            debug('Chrono: ' + str( self.i ) + ' / ' + str( self.total ) +
                  ' (Total: '+ self.strTotal +
                  ')  Remaining: ' + prettyPrintTime(r) )


class Clock:
    def __init__(self):
        self.time = 0
    
    def clock(self):
        t = time.time()
        result = t - self.time
        self.time = t
        return result
    
    def strClock(self):
        return "Time: " + prettyPrintTime(self.clock())
        

def debug(msg):
    if debug_mode:
        print "Debug : " + msg;
    

def printError(msg):
    print "Erreur : " + msg + " !!!";



def cleanLine(line):
   if line[-1] == '\n' or line[-1] == '\r':
      return cleanLine( line[:-1] )
   else:
      return line

def printObject(arg, prefix = ""):
    if type(arg) == type(dict()):
        for i in arg:
            printObject( arg[i], prefix + " " + i )
    elif type(arg) == type([]):
            for i in range(len(arg)):
                printObject( arg[i], prefix + " " + str(i+1) )
    else:
        print prefix + " : " + str(arg)





def prettyPrintTime(sec):
    s = int(sec)
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return ('%sh %smin %ssec' % (hours, minutes, seconds) )
    elif minutes > 0:
        return ('%smin %ssec' % (minutes, seconds) )
    else:
        ms = int( 100 * (sec - s))
        return ('%ssec %sms' % (seconds, ms) )


def urlOpen(url):
    a = urllib.urlopen(url)
    # handle timeout here
    return a

def getDOM(url):
    return BeautifulSoup( urlOpen(url) )


def getHTML(url):
    return urlOpen(url).read()




trueIndic  = ['yes', 'Yes', 'True', 'true', 'T']
falseIndic = ['no', 'No', 'False', 'false', 'F']

def getBool(s):
    if s in trueIndic:
        return True
    elif s in falseIndic:
        return False
    else:
        raise Exception("Wrong boolean indicator")