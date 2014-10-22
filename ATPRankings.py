# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 10:50:14 2014

@author: Gaspard
"""

import csv, sets
from bdd import *

class ATPRankings:
    
    def __init__(self, rankPath='', matchesPath=''):
        self.rankPath = rankPath
        self.matchesPath = matchesPath
        self.playersNb = 0
        self.tab = []
        self.tournaments = []
    
    def setNumberOfPlayers(self, nb):
        self.playersNb = nb
        self.tab = [ sets.Set() for i in range(n) ]
    
    def setTournaments(self, tournaments):
        self.tournaments = tournaments
    
    def feedMatch(self, m):
        tab[ int(m['IDPlayer']) ].add( int(m['IDTournament']) )
    
    def startFeedingMatches(self):
        with open( self.matchesPath , 'rb') as f:
            for m in getDictReader(f):
                self.feedMatch(m)
    
    def loadRankings(self, ID):
        with open(self.getPath(ID), 'rb') as f:
            return [e for e in csv.DictReader(f) ]
    
    def getPath(self, ID):
        return self.rankPath + "p" + str(ID) + "p.csv"
    
    
    





