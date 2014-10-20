# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 15:03:09 2014

@author: Gaspard
"""

from bdd import *

class MatchMerger:
    
    def __init__(self):
        self.matchesFolder = ''
        self.targetPath  = ''
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
        with open( self.getPath(e, y)+".csv", 'rb') as f:
            r = getReader(f)
        return r
    
    
    