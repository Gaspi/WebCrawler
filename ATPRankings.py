# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 10:50:14 2014

@author: Gaspard
"""

import csv, sets, os
from bdd import *
from utils import *




def findRankingFromDate(date, rankTab):
    if len(rankTab) == 0:
        return -1
    time = timestamp(date)
    if time > timestamp(rankTab[0][0]):
        return -1
    index = findIndexFromDate(time, rankTab, 0, len(rankTab)-1 )
    if index == len(rankTab)-1:
        return -1
    else:
        return rankTab[index][1]


def findIndexFromDate(time, rankTab, start, end):
    if end <= start + 1:
        return end
    middle = (start + end) // 2
    if timestamp( rankTab[middle][0] ) > time:
        return findIndexFromDate(time,rankTab, middle, end)
    else:
        return findIndexFromDate(time,rankTab, start, middle)


class ATPRankings:
    
    def __init__(self, rankPath='', matchesPath='', savePath='', cleanMatchesPath=''):
        self.rankPath = rankPath
        self.matchesPath = matchesPath
        self.savePath = savePath
        self.cleanMatchesPath = cleanMatchesPath
        self.playersNb = 0
        self.playedTourn = []
        self.ranks = []
        self.tournaments = []
    
    
    def feedMatch(self, m):
        self.playedTourn[ int(m['IDPlayer']) ].add( int(m['IDTournament']) )
    
    def startFeedingMatches(self):
        self.playedTourn = [ sets.Set() for i in range(self.playersNb) ]
        with open( self.matchesPath , 'rb') as f:
            for m in getDictReader(f):
                self.feedMatch(m)
    
    def startComputingRanks(self):
        self.ranks = [ sets.Set() for i in range(self.playersNb)]
        for IDplayer in range(self.playersNb):
            tournamentsP = self.playedTourn[IDplayer]
            rankings = self.loadRankings(IDplayer)
            for tID in tournamentsP:
                tStart = self.tournaments[tID]['TournamentStart']
                rank = findRankingFromDate(tStart, rankings)
                self.ranks[IDplayer].add( (tID,rank) )
        print self.ranks
    
    
    def loadRankings(self, ID):
        with open(self.getPath(ID), 'rb') as f:
            return [e for e in csv.reader(f) ]

    def getPath(self, ID):
        return self.rankPath + "p" + str(ID) + "p.csv"
    
    
    # Saving / loading functions for playedTourn
    def savePlayedTournaments(self):
        with open(self.savePath, 'wb') as f:
            w = csv.writer(f, delimiter='|')
            for p in self.playedTourn:
                w.writerow( [ str( list(p) ) ] )
    
    def loadPlayedTournaments(self):
        if os.path.isfile( self.savePath ):
            with open(self.savePath, 'rb') as f:
                r = csv.reader(f, delimiter='|',quotechar='|')
                self.playedTourn = []
                for p in r:
#                    print str( p[0][1:-1].split(',') )
                    l = [ int(e) for e in p[0][1:-1].split(',') ]
                    self.playedTourn.append( sets.Set(l) )
            self.playersNb = len(self.playedTourn)

    # Saving / loading functions for playedTourn
    def saveRanks(self):
        with open(self.savePath+"r", 'wb') as f:
            w = csv.writer(f, delimiter='|')
            for r in self.ranks:
                w.writerow( [ str( list(r) ) ] )
    
    
    def getRank(self,idPlayer,idTournament):
        for r in self.ranks[idPlayer]:
            if int(r[0]) == idTournament:
                return int( r[1] )
        raise Exception('Player ' + idPlayer + 'has not played in tournament ' + idTournament + '!!')
        
    def clean(self):
        self.ID = 0
        with open( self.cleanMatchesPath, 'wb') as f:
            w = getWriter(f, ['IDMatch'] + match_field_names + ['Rank'] )
            with open(self.cleanMatchesPath + "id", 'rb') as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow( self.defaultMatchCleanFunction(e) )
    
    def defaultMatchCleanFunction(self, entry):
        entry['Rank'] = self.getRank( int( entry['IDPlayer'] ), int( entry['IDTournament']) )
        return entry
        