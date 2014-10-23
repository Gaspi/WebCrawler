# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 16:03:13 2014

@author: Gaspard, Thomas, Arnaud
"""

import time, datetime, urllib, sys
from bs4 import BeautifulSoup


# TODO put that in localurl
debug_mode = True



def timestamp(date):
    return int(time.mktime(datetime.datetime.strptime(date,"%d.%m.%Y").timetuple()))

def createChronology(date, round_):
    return timestamp(date)*10 + int(round_)



class Chrono:
    def __init__(self):
        self.sizeBar = 18
        self.periodTime = 1.0
    
    def start(self, nbIterations = 0):
        self.total = int( nbIterations )
        self.absoluteTotal = self.total
        self.strTotal = str( self.absoluteTotal )
        self.i = 0
        self.previous = 0
        self.startTime = time.time()
        self.previousTime = self.startTime
    
    def needPrint(self):
        return time.time()-self.previousTime > self.periodTime
    
    def tick(self, iterations = 1):
        self.i += iterations
    
    def decTotal(self, iterations = 1):
        self.total -= 1
        
    def remainingTime(self):
        remaining = (self.total - self.i) * self.elapsedTime() / self.i
        self.previous = self.i
        return remaining
    def remaining(self):
        return prettyPrintTime( self.remainingTime() )
    
    def elapsedTime(self):
        self.previousTime = time.time()
        return self.previousTime - self.startTime
    def elapsed(self):
        return prettyPrintTime( self.elapsedTime() )
    
    
    def getBar(self):
        return loadingBar(self.sizeBar, self.i,self.total)
    
    def printRemaining(self):
        r = self.remaining()
        if self.absoluteTotal == self.total:
            debug('Chrono: ' + str( self.i ) + ' / ' + self.strTotal +
                  '  Remaining: ' + r )
        else:
            debug('Chrono: ' + str( self.i ) + ' / ' + str( self.total ) +
                  ' (Total: '+ self.strTotal +
                  ')  Remaining: ' + r )


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
        
    def done(self):
        debug("Done. " + self.strClock())


currencyName = {'\xe2\x82\xac'  :'E',
                '$'             :'D',
                '\xc2\xa3'      :'P',
                '\xc3\x87'      :'E',
                '\xc3\xba'      :'P',
                'A$'            :'A'}        

def debug(msg):
    if debug_mode:
        print "D: " + msg;
    

def printError(msg):
    print "Error: " + msg + " !!!";



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






def restartLine():
    sys.stdout.write('\b\r')
    sys.stdout.flush()

def printLine(l):
    restartLine()
    sys.stdout.write(l)

def loadingBar(length, progress, total=1):
    progress = float(length * progress) / total
    n = int( progress )
    p = int( 10 * (progress - n) )
    return " |" + ('#' * n) + str(p) + ('_'*(length-n-1)) + "| "








