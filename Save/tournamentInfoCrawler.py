# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 10:31:07 2014

@author: Gaspard
"""

import os, sets
from utils import *
from bdd   import *
from tournamentCrawler import *
from ForexCrawler import *

url_tournament = 'http://www.atpworldtour.com/Scores/Archive-Event-Calendar.aspx'




def defaultTournamentCleanFunction(t):
    e   = int( t['e'] )
    cat = int( t['TournamentCategory'] )
    t['TournamentCategory'] = updateCategory(e,cat)
    
    a = re.findall('([^0-9]+)([0-9]*)', t['TournamentPrize'] )
    
    currency = currencyName[a[0][0]]
    
    t['TournamentPrize'] = int(a[0][1])
    t['TournamentCurrency'] = currency
    conversion = forexDate( t['TournamentStart'], currency)
    t['TournamentPrizeUSD'] = int( float(t['TournamentPrize']) / conversion )
    return t


class Tournaments:
    
    def __init__(self, fs):
        self.tournaments = []
        self.playerCodes = sets.Set()
        self.cleanTournamentsPath = fs.cleanTournamentsPath
        self.tournamentsPath = fs.tournamentsPath
        self.playerCodesPath = fs.playerCodesPath
        
        self.i = 0
        self.savePeriod = 20
    
    
    def isTreated(self, e, y):
        for t in self.tournaments:
            if int( t['e'] ) == int(e) and int(t['y']) == int(y):
                return True
        return False
    
    def addTournamentFromCode(self, code):
        e = code['e']
        y = code['y']
        if self.isTreated(e, y):
            return False
        else:
            (newPlayers, newTour) = getAllTournamentInfos(code)
            self.tournaments.append( newTour )
            for p in newPlayers:
                self.playerCodes.add(p)
            self.saveMaybe()
            return True
    
    
    def saveCodes(self):
        with open(self.playerCodesPath, 'wb') as csvfile:
            w = csv.writer(csvfile, delimiter=' ', quotechar='|')
            w.writerow( list(self.playerCodes) )
    def loadCodes(self):
        with open(self.playerCodesPath, 'rb') as csvfile:
            r = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.playerCodes = sets.Set(r.next())
    
    
    def saveTournaments(self):
        with open(self.tournamentsPath, 'wb') as csvfile:
            w = getWriter(csvfile, tournaments_infos_fields )
            w.writerows(self.tournaments)
    def loadTournaments(self):
        with open(self.tournamentsPath, 'rb') as csvfile:
            self.tournaments = getReader( csvfile )
            for t in self.tournaments:
                t['e'] = int( t['e'] )
                t['y'] = int( t['y'] )

    
    def save(self):
        self.saveCodes()
        self.saveTournaments()
    def load(self):
        self.loadCodes()
        self.loadTournaments()
    def canLoad(self):
        return  os.path.isfile(self.playerCodesPath) and os.path.isfile(self.tournamentsPath)

    def saveMaybe(self):
        self.i += 1
        if self.i % self.savePeriod == 0:
            debug("Saving")
            self.save()
    
    def clean(self, cleanFunction=defaultTournamentCleanFunction):
        with open( self.cleanTournamentsPath, 'wb') as f:
            w = getWriter(f, tournaments_infos_fields_clean )
            with open( self.tournamentsPath, 'rb' ) as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow( cleanFunction(e) )
    














