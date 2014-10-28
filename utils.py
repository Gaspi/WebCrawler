# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 16:03:13 2014

@author: Gaspard, Thomas, Arnaud
"""

import time, datetime, urllib, sys
from math import ceil, log
from bs4 import BeautifulSoup


# TODO put that in localurl
debug_mode = True



def timestamp(date):
    return int(time.mktime(datetime.datetime.strptime(date,"%d.%m.%Y").timetuple()))

def createChronology_old(date, round_):
    return timestamp(date)*10 + int(round_)


def createChronology(startDate, endDate, round_, draw ):
    nRounds = float( ceil( log(int(draw)) / log(2)) )
    start = timestamp(startDate)
    end = 86400 + timestamp(endDate)
    interv = float(end - start)
    return start + int(interv/(2.0*nRounds) + float(int(round_)-8+nRounds)*interv/nRounds)


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
            debugCL('Chrono: ' + str( self.i ) + ' / ' + self.strTotal +
                  '  Remaining: ' + r )
        else:
            debugCL('Chrono: ' + str( self.i ) + ' / ' + str( self.total ) +
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











def updateCategory(e, cat):
    if   cat==4: return 5   # ATP Challenger Tour
    elif cat==3: return 4   # ATP World Tour 250
    elif cat==2: return 3   # ATP World Tour 500
    elif cat==1: return 2   # ATP World Tour Masters 1000
    elif cat ==-1:
        if   e == 96:   # Olympics
            return 1
        elif e in {352,403,404,410,416,421,422,1536,357}:
            return 2            # ATP World Tour Masters 1000
        elif e in {328,329,402,407,414,418,425,495,573,747,807,408}:
            return 3            # ATP World Tour 500
        elif e in { 301,306,308,311,314,315,316,321,337,338,339,341,360,375,
                    419,423,424,429,438,439,440,451,468,496,499,500,505,506,
                    533,568,717,741,773,891,1720,2276,3348,317,409,309,359,
                    620,481,615,890,336,433,441,3465,475,325,73,327,319 }:
            return 4            # ATP World Tour 250
    return cat





# -------------------------------------------------------------
# ----------- DEBUGGING ---------------------------------------
# -------------------------------------------------------------

debugFileOut = 'NoFile'
debugNewline = True

def setDebugFileOut(fileOut):
    global debugFileOut
    debugFileOut = fileOut
    debugPrintTime("Starting:")
    
def debugPrintTime(prefix=''):
    debugLines(["", "-"*(35 + len(prefix)),
                "   {1}  {0.tm_mday} / {0.tm_mon} / {0.tm_year}   {0.tm_hour}:{0.tm_min}:{0.tm_sec}".format(time.localtime(), prefix),
                "-"*(35 + len(prefix)), "" ] )

def debug(line = ''):
    global debugNewline
    if not debugNewline:
        print
    debugNewline = True
    ln = str(line) + '\n'
    sys.stdout.write(   ln )
    debugFileOut.write( ln )

def debugLines(lines):
    for l in lines:
        debug(l)
    
def debugCL(line = ''):
    global debugNewline
    if not debugNewline:
        sys.stdout.write('\b\r')
        sys.stdout.flush()
    debugNewline = False
    ln = str(line)
    sys.stdout.write(   ln )
    debugFileOut.write( ln + '\n' )

#
#def debug(msg):
#    if debug_mode:
#        Debug.println("D: " + msg)
#    
def printError(msg):
    debug( "Error: " + msg + " !!!" )



def restartLine():
    sys.stdout.write('\b\r')
    sys.stdout.flush()

def printLine(l):
    debugCL(l)

def loadingBar(length, progress, total=1):
    progress = float(length * progress) / total
    n = int( progress )
    p = int( 10 * (progress - n) )
    return " |" + ('#' * n) + str(p) + ('_'*(length-n-1)) + "| "



