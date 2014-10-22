# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 15:03:09 2014

@author: Gaspard
"""
import os
from bdd    import *
from utils  import *



class MatchMerger:
    
    def __init__(self,matchesFolder = '',targetPath  = '',cleanMatchesPath=''):
        self.matchesFolder = matchesFolder
        self.targetPath    = targetPath
        self.cleanMatchesPath=cleanMatchesPath
        self.ID = 0
    
    def startMerging(self, tournaments):
        with open( self.targetPath , 'wb') as f:
            w = getMatchWriter(f)
            for t in tournaments:
                writeTournament(w, self.load( int(t['e']) , int(t['y'])))
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
    
    
    def clean(self):
        self.ID = 0
        with open( self.cleanMatchesPath + "id" , 'wb') as f:
            w = getWriter(f, ['IDMatch'] + match_field_names )
            with open(self.targetPath, 'rb') as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow( self.defaultMatchCleanFunction(e) )
    
    def defaultMatchCleanFunction(self, entry):
        entry['IDMatch'] = self.ID // 2
        self.ID += 1
        return entry










    