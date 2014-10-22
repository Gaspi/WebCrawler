# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 10:31:07 2014

@author: Gaspard
"""

import os, sets

from utils import *
from bdd   import *
from tournamentCrawler import *

url_tournament = 'http://www.atpworldtour.com/Scores/Archive-Event-Calendar.aspx'

tournaments_infos_fields = [
    'IDTournament',
    'Tournament',
    'Indoor',
    'TournamentType',   # Field du site [1,2,4]
    'TournamentCategory',   # Field de Sylvain
    'Surface',
    'Country',
    'TournamentPrize',
    'Draw',
    'TournamentStart',
    'TournamentEnd', 'e', 'y' ]


def defaultTournamentCleanFunction(t):
    e   = int( t['e'] )
    cat = int( t['TournamentCategory'] )
    if   cat==4: cat=6
    elif cat==3: cat=5
    elif cat==2: cat=4
    elif cat==1: cat=3
    elif cat ==-1:
        if   e == 96:
            cat = 1
        elif e == 605:
            cat = 2
        elif e in {352,403,404,410,416,421,422,1536,357}:
            cat = 3
        elif e in {328,329,402,407,414,418,425,495,573,747,807,408}:
            cat = 4
        elif e in { 301,306,308,311,314,315,316,321,337,338,339,341,360,375,
                    419,423,424,429,438,439,440,451,468,496,499,500,505,506,
                    533,568,717,741,773,891,1720,2276,3348,317,409,309,359,
                    620,481,615,890,336,433,441,3465,475,325,73,327,319 }:
            cat = 5
    t['TournamentCategory'] = cat
    return t



class Tournaments:
    
    def __init__(self, tournamentsPath = '', playerCodesPath = ''):
        self.tournaments = []
        self.playerCodes = sets.Set()
        
        self.tournamentsPath = tournamentsPath
        self.playerCodesPath = playerCodesPath
        
        self.i = 0
        self.savePeriod = 20
    
    
    def isTreated(self, e, y):
        for t in self.tournaments:
            if t['e'] == e and t['y'] == y:
                return True
        return False
    
    def addTournamentFromCode(self, code):
        e = code['e']
        y = code['y']
        if self.isTreated(e, y): return False
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
        path2 = self.tournamentsPath + "2"
        os.rename( self.tournamentsPath, path2 )
        with open( self.tournamentsPath , 'wb') as f:
            w = getWriter(f, tournaments_infos_fields )
            with open( path2, 'rb' ) as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow( cleanFunction(e) )
    














