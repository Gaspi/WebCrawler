# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 10:50:14 2014

@author: Gaspard
"""

import csv, sets, os
from bdd import *
from utils import *

import numpy as np
import warnings
warnings.simplefilter('ignore', np.RankWarning)

hoursInMonth = 30.4375 *24




def rankTimestamp(t):
    return int( timestamp(t) / 3600 )

def getGrads(timestamps, rankings):
    t0 = timestamps[0]
    (ind1 , ind3 , ind6 , ind12 ) = (0,0,0,0)
    (grad1, grad3, grad6, grad12, interpol6d2, interpol6d3, interpol12d2, interpol12d3) = (0,) * 4 + (0,)*4
    for i,t in enumerate(timestamps):
        if t0 - t < hoursInMonth:
            ind1 = i
        if t0 - t < hoursInMonth * 3:
            ind3 = i
        if t0 - t < hoursInMonth * 6:
            ind6 = i
        if t0 - t < hoursInMonth * 12:
            ind12 = i
    grad1  = np.polyfit( timestamps[:ind1+1] , rankings[:ind1+1] , 1 )[0]*24*7
    grad3  = np.polyfit( timestamps[:ind3+1] , rankings[:ind3+1] , 1 )[0]*24*7
    grad6  = np.polyfit( timestamps[:ind6+1] , rankings[:ind6+1] , 1 )[0]*24*7
    grad12 = np.polyfit( timestamps[:ind12+1], rankings[:ind12+1], 1 )[0]*24*7
    
    t6  = t0 + 6  * 30 * 24
    
    c = np.polyfit( timestamps[:ind6+1] , rankings[:ind6+1] , 2 )
    interpol6d2 = c[0] * (t6 ** 2) + c[1] * t6 + c[2]
    
    c = np.polyfit( timestamps[:ind6+1] , rankings[:ind6+1] , 3 )
    interpol6d3 = c[0] * (t6 ** 3) + c[1] * (t6 ** 2) + c[2] * t6 + c[3]
    
    c = np.polyfit( timestamps[:ind12+1], rankings[:ind12+1], 2 )
    interpol12d2 = c[0] * (t6 ** 2) + c[1] * t6 + c[2]
    
    c = np.polyfit( timestamps[:ind12+1], rankings[:ind12+1], 3 )
    interpol12d3 = c[0] * (t6 ** 3) + c[1] * (t6 ** 2) + c[2] * t6 + c[3]
    
    if False:
        print t0
        print hoursInMonth
        print ind1
        print str( timestamps[:ind1+1] )
        print str( rankings[:ind1+1] )
        print ind3
        print str( timestamps[:ind3+1] )
        print str( rankings[:ind3+1] )
        print ind6
        print str( timestamps[:ind6+1] )
        print str( rankings[:ind6+1] )
        
    return ( grad1, grad3, grad6, grad12, interpol6d2, interpol6d3, interpol12d2, interpol12d3 )




def getInterpol(timestamps, rankings):
    return 0



def findIndexFromDate(time, timestamps):
    if len(timestamps) == 0:
        return -1
    index = findIndexAuxFromDate(time, timestamps, 0, len(timestamps)-1 )
    if index == len(timestamps) - 1:
        return -1
    else:
        return index


def findIndexAuxFromDate(time, timestamps, start, end):
    if end <= start + 1:
        return end
    middle = (start + end) // 2
    if timestamps[middle] > time:
        return findIndexAuxFromDate(time,timestamps, middle, end)
    else:
        return findIndexAuxFromDate(time,timestamps, start, middle)

def getTimestamps(rankings):
    timestamps = [ rankTimestamp(r[0]) for r in rankings ]
    for i in range(len(rankings) ):
        rankings[i] = int( rankings[i][1] )
    return timestamps
    


class ATPRankings:
    
    def __init__(self, fs):
        self.rankPath           = fs.ranksFolder
        self.matchesPath        = fs.matchesPath
        self.savePath           = fs.rankingsSave
        self.cleanMatchesPath   = fs.cleanMatchesPath
        self.playersNb = 0
        self.playedTourn = []
        self.ranks = []
        self.tournaments = []
    
    
    def feedMatch(self, m):
        try:
            self.playedTourn[ int(m['IDPlayer']) ].add( int(m['IDTournament']) )
            
        except:
            print str(len(self.playedTourn)), str(self.playersNb), str(m), str(self.playedTourn)
            raise Exception("Index problem")
    
    def startFeedingMatches(self):
        self.playedTourn = [ sets.Set() for i in range(self.playersNb) ]
        with open( self.matchesPath , 'rb') as f:
            for m in getDictReader(f):
                self.feedMatch(m)
    
    def startComputingRanks(self):
        self.ranks = [ sets.Set() for i in range(self.playersNb)]
        chrono = Chrono()
        chrono.start( self.playersNb )
        dechet = 0
        total = 0
        for IDplayer in range(self.playersNb):
            tournamentsP = self.playedTourn[IDplayer]
            rankings = self.loadRankings(IDplayer)
            timestamps = getTimestamps(rankings)
            for tID in tournamentsP:
                tStart = rankTimestamp( self.tournaments[tID]['TournamentStart'] )
                (rank, grad1, grad3, grad6, grad12, interpol6d2, interpol6d3, interpol12d2, interpol12d3) = (-1,) * 9
                index = findIndexFromDate(tStart, timestamps)
                if index >= 0:
                    rank = rankings[index]
                    timestampsAux = timestamps[index:]
                    rankingsAux   = rankings[index:]
                    grad1, grad3, grad6, grad12, interpol6d2, interpol6d3, interpol12d2, interpol12d3 = \
                            getGrads( timestampsAux, rankingsAux)
                else:
                    dechet += 1
                total += 1
                self.ranks[IDplayer].add( (tID,rank, grad1, grad3, grad6, grad12, interpol6d2, interpol6d3, interpol12d2, interpol12d3) )
            chrono.tick()
            if chrono.needPrint():
                printLine("Player " + str(chrono.i) + chrono.getBar() + " Remains " + chrono.remaining() )
        print "Dechet : " + str(dechet) + " / " + str(total)
    
    

    
    
    
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
                self.playedTourn = []
                for p in csv.reader(f, delimiter='|',quotechar='|'):
                    aux = p[0][1:-1]
                    if len(aux) == 0:
                        l = []
                    else:
                        l = [ int(e) for e in aux.split(',') ]
                    self.playedTourn.append( sets.Set(l) )
            self.playersNb = len(self.playedTourn)

    # Saving / loading functions for playedTourn
    def saveRanks(self):
        with open(self.savePath+"r", 'wb') as f:
            w = csv.writer(f, delimiter='|')
            for r in self.ranks:
                w.writerow( [ str( list(r) ) ] )
    
    
    def getRankInfos(self,idPlayer,idTournament):
        for r in self.ranks[idPlayer]:
            if int(r[0]) == idTournament:
                return r[1:]
        raise Exception('Player ' + idPlayer + 'has not played in tournament ' + idTournament + '!!')
    
    
    def clean(self):
        chrono = Chrono()
        chrono.start()
        self.ID = 0
        with open( self.cleanMatchesPath, 'wb') as f:
            w = getWriter(f, match_field_names_clean + new_match_fields )
            with open(self.cleanMatchesPath + "id", 'rb') as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow( self.defaultMatchCleanFunction(e) )
                    chrono.tick()
                    if chrono.needPrint():
                        debugCL("Matches " + str(chrono.i) + " Elapsed: " + chrono.elapsed() )
    
    def defaultMatchCleanFunction(self, entry):
        t = self.getRankInfos( int( entry['IDPlayer'] )  , int( entry['IDTournament']) )
        entry['Rank']           = t[0]
        entry['Grad1Month']     = t[1]
        entry['Grad3Months']    = t[2]
        entry['Grad6Months']    = t[3]
        entry['Grad12Months']   = t[4]
        entry['Interpol6MonthsDeg2']= t[5]
        entry['Interpol6MonthsDeg3']= t[6]
        entry['Interpol12MonthsDeg2']= t[7]
        entry['Interpol12MonthsDeg3']= t[8]
        t = self.getRankInfos( int( entry['IDOpponent'] ), int( entry['IDTournament']) )
        entry['RankOpponent']       = t[0]
        entry['Grad1MonthOpp']      = t[1]
        entry['Grad3MonthsOpp']     = t[2]
        entry['Grad6MonthsOpp']     = t[3]
        entry['Grad12MonthsOpp']    = t[4]
        entry['Interpol6MonthsOppDeg2'] = t[5]
        entry['Interpol6MonthsOppDeg3'] = t[6]
        entry['Interpol12MonthsOppDeg2'] = t[7]
        entry['Interpol12MonthsOppDeg3'] = t[8]
        return entry









