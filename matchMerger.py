# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 15:03:09 2014

@author: Gaspard
"""
import re
from bdd    import *
from utils  import *
from ForexCrawler import *

class MatchMerger:
    
    def __init__(self,fs):
        self.matchesFolder   = fs.matchesFolder
        self.targetPath      = fs.matchesPath
        self.cleanMatchesPath= fs.cleanMatchesPath
        self.tournaments = None
        self.ID = 0
    
    def startMerging(self, tournaments):
        chrono = Chrono()
        size = len(tournaments)
        with open( self.targetPath , 'wb') as f:
            w = getMatchWriter(f)
            chrono.start(size)
            for t in tournaments:
                writeTournament(w, self.load( int(t['e']) , int(t['y'])))
                chrono.tick()
                if chrono.i % 20 == 0:
                    printLine("Tournaments " + str(chrono.i) + " / " + str(size) +
                    chrono.getBar() + " Remaining: " + chrono.remaining() )
                self.ID += 1
        print # New line after loading bar
    
    
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
    
    
    def clean(self, chrono):
        self.ID = 0
        with open( self.cleanMatchesPath + "id" , 'wb') as f:
            w = getWriter(f, match_field_names_clean)
            with open(self.targetPath, 'rb') as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow( self.defaultMatchCleanFunction(e) )
                    chrono.tick()
                    if chrono.needPrint():
                        printLine("Matches " + str(chrono.i) + " Elapsed: " + chrono.elapsed() )
        print # new line after loading bar
    
    def defaultMatchCleanFunction(self, entry):
        e = self.tournaments[ int(entry['IDTournament']) ]['e']
        cat = int( entry['TournamentCategory'] )
        entry['TournamentCategory'] = updateCategory(e,cat)
        entry['IDMatch'] = self.ID // 2
        a = re.findall('([^0-9]+)([0-9]*)', entry['TournamentPrize'] )
        currency = currencyName[a[0][0]]
        entry['TournamentPrize'] = int( a[0][1] )
        entry['TournamentCurrency'] = currency
        conversion = forexDate( entry['TournamentStart'], currency)
        entry['TournamentPrizeUSD'] = int( float(entry['TournamentPrize']) / conversion )
        self.ID += 1
        return entry










    