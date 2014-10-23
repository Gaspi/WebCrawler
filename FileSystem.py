# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 16:10:38 2014

@author: Gaspard
"""

import os
from utils import *

class FileSystem:

    def __init__(self,infoReader):
        self.folder              = infoReader.readLine()
        self.matches_folder      = infoReader.readLine()
        self.ranksFolder         = infoReader.readLine()
        self.cleanFolder         = infoReader.readLine()
        
        try:    os.stat( self.folder)
        except: os.mkdir(self.folder)
        try:    os.stat( self.matches_folder)
        except: os.mkdir(self.matches_folder)
        try:    os.stat( self.ranksFolder)
        except: os.mkdir(self.ranksFolder)
        try:    os.stat( self.cleanFolder)
        except: os.mkdir(self.cleanFolder)
        
        self.tournaments_codes = self.folder + "tournamentCodes.csv"
        self.tournaments_save  = self.folder + "tournaments.csv"
        self.player_codes      = self.folder + "playerCodes.csv"
        self.player_save       = self.folder + "players.csv"
        self.treated_path      = self.folder + "treated.csv"
        self.matches_path      = self.folder + "matches.csv"
        self.rankingsSave      = self.folder + "rankingsSave.csv"

        self.cleanPlayerPath     = self.cleanFolder + "players.csv"
        self.cleanTournamentsPath= self.cleanFolder + "tournaments.csv"
        self.cleanMatchesPath    = self.cleanFolder + "matches.csv"
    
    
    
    
    
class InfoReader:
    
    def __init__(self, path):
        with open(path, 'rb') as f:
            self.lines = f.readlines()
        self.i = 0
    
    def readLine(self):
        res = self.lines[ self.i ]
        self.i += 1
        return cleanLine(res)
    
    def readInt(self):
        self.readLine()
        return int( self.readLine() )
    def readBool(self):
        self.readLine()
        return getBool( self.readLine() )
    def readIntList(self):
        self.readLine()
        return [ int(e) for e in  self.readLine().split(',') ]
    
    def start(self, nbIterations):
        self.total = nbIterations
        self.absoluteTotal = self.total
        self.strTotal = str( self.absoluteTotal )
        self.i = 0
        self.previous = 0
        self.startTime = time.time()
        self.previousTime = self.startTime
    
    
    
    
    
    
    