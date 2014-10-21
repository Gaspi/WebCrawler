# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 15:03:09 2014

@author: Gaspard
"""
import os
from bdd    import *
from utils  import *

def defaultMatchCleanFunction(entry):
    return entry

class MatchMerger:
    
    def __init__(self,matchesFolder = '',targetPath  = ''):
        self.matchesFolder = matchesFolder
        self.targetPath    = targetPath
        self.ID = 0
    
    def startMerging(self, tournaments):
        with open( self.targetPath , 'wb') as f:
            w = getMatchWriter(f)
            for t in tournaments:
                writeTournament(w, self.load(int( t['e'] ) , int( t['y'] )))
                self.ID += 1
    
    def getPath(self, e, y):
        return self.matchesFolder + "y" + str(y) + "e" + str(e)
    
    def load(self, e, y):
        r = []
        try:
            with open( self.getPath(e, y)+".csv", 'rb') as f:
                r = getReader(f)
        except:
            printError("Missing tournament: y " + str(y) + "  |  e " + str(e) )
        return r
    
    
    def clean(self, cleanFunction=defaultMatchCleanFunction):
        path2 = self.targetPath + "2"
        os.rename( self.targetPath, path2 )
        with open( self.targetPath , 'wb') as f:
            w = getMatchWriter(f)
            with open( path2, 'rb' ) as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow(cleanFunction(e))
                
    










    