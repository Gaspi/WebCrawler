# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 10:50:14 2014

@author: Gaspard
"""

import csv, sets, os
from bdd import *

class ATPRankings:
    
    def __init__(self, rankPath='', matchesPath='', savePath=''):
        self.rankPath = rankPath
        self.matchesPath = matchesPath
        self.savePath = savePath
        self.playersNb = 0
        self.tab = []
        self.tournaments = []
    
    def setNumberOfPlayers(self, nb):
        self.playersNb = nb
        self.tab = [ sets.Set() for i in range(nb) ]
    
    def setTournaments(self, tournaments):
        self.tournaments = tournaments
    
    def feedMatch(self, m):
        self.tab[ int(m['IDPlayer']) ].add( int(m['IDTournament']) )
    
    def startFeedingMatches(self):
        with open( self.matchesPath , 'rb') as f:
            for m in getDictReader(f):
                self.feedMatch(m)
    
    def loadRankings(self, ID):
        with open(self.getPath(ID), 'rb') as f:
            return [e for e in csv.DictReader(f) ]
    
    def getPath(self, ID):
        return self.rankPath + "p" + str(ID) + "p.csv"
    
    # Aux functions
    def save(self):
        with open(self.savePath, 'wb') as f:
            w = csv.writer(f, delimiter='|')
            for p in self.tab:
                w.writerow( [ str( list(p) ) ] )
    
    def load(self):
        if os.path.isfile( self.savePath ):
            with open(self.savePath, 'rb') as f:
                r = csv.reader(f, delimiter='|',quotechar='|')
                self.tab = []
                for p in r:
                    print str( p[0][1:-1].split(',') )
                    l = [ int(e) for e in p[0][1:-1].split(',') ]
                    tab.append( sets.Set(l) )





