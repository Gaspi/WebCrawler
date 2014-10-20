# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 10:31:07 2014

@author: Gaspard
"""

import os
import sets
import numpy as np

from utils import *
from bdd   import *
from tournamentCrawler import *

url_tournament = 'http://www.atpworldtour.com/Scores/Archive-Event-Calendar.aspx'

tournaments_infos_fields = [
    'IDTournament',
    'Tournament',
    'Indoor',
    'TournamentType',
    'Surface',
    'Country',
    'TournamentPrize',
    'Draw',
    'TournamentStart',
    'TournamentEnd', 'e', 'y' ]



class Tournaments:
    
    def __init__(self):
        self.tournaments = []
        self.playerCodes = sets.Set()
        
        self.playerCodesPath = ''
        self.tournamentsPath = ''
        
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
        if not self.isTreated(e, y):
            (newPlayers, newTour) = getAllTournamentInfos(code)
            self.tournaments.append( newTour )
            for p in newPlayers:
                self.playerCodes.add(p)
            self.saveMaybe()
    
    
    
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

    

    def fetchAllMatches(self, filename, dicoPlayers, verbose=True):
        chrono = Chrono()
        with open(filename, 'wb') as f:
            w = getMatchWriter(f)
            chrono.start( len(self.tour) )
            for t in self.tour:
                matches = getMatchesOfTournament( t['e'], t['y'],
                    {'IDTournament': t['IDTournament'],
                     'Indoor':t['Indoor'] },
                    dicoPlayers )
                writeTournament(w, matches)
                chrono.tick()
                if verbose and ( chrono.i % 5 == 0 ):
                    chrono.printRemaining()



