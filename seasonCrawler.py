# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:28:49 2014
@author: Gaspard, Thomas, Arnaud
"""

import re

from utils import *
from bdd   import *
from tournamentCrawler import *


url_tournament = 'http://www.atpworldtour.com/Scores/Archive-Event-Calendar.aspx'

tournaments_codes_fields = ['IDTournament',
                            'Indoor',
                            'TournamentType',
                            'TournamentCategory', 'e', 'y' ]  # Field de Sylvain


class Seasons:
    
    def __init__(self, tournamentCodes=''):
        self.codes = []
        self.ID = 0
        self.tournamentsCodes = tournamentCodes
    
    def addTournamentsFromTY(self, t, y):
        dom = getDOM( url_tournament + '?t='+str(t)+'&y='+str(y) )
        tournaments = dom.find_all('tr','calendarFilterItem')
        
        for tr in tournaments:
            col = tr.find_all('td')
            link = col[4].find_all('a')
            if len(link) > 0 and link[0].contents[0][0:3] == 'SGL':
                a = re.findall('e=([0-9]+)\&y\=([0-9]+)' , link[0].attrs['href'])[0]
                e = int(a[0])
                y = int(a[1])
                cat = col[1].contents[-1]
                c = -1
                if   cat == u'Grand Slams':
                    c = 0
                elif cat == u'ATP World Tour Masters 1000':
                    c = 1
                elif cat == u'ATP World Tour 500':
                    c = 2
                elif cat == u'ATP World Tour 250':
                    c = 3
                elif cat == u'ATP Challenger Tour':
                    c = 4
                tour =  {
                    'IDTournament': self.ID,
                    'e':e,
                    'y':y,
                    'Indoor': 0 if col[2].contents[0] == u'Outdoor' else 1,
                    'TournamentType': t,
                    'TournamentCategory': c }
                self.codes.append( tour )
                self.ID += 1
    
    
    def addTournamentsFromAllTY(self, tList, yStart, yEnd):
        for t in tList:
            for y in range(yStart, yEnd+1):
                self.addTournamentsFromTY(t, y)
    
    
    def saveCodes(self):
        with open(self.tournamentsCodes, 'wb') as csvfile:
            w = getWriter(csvfile, tournaments_codes_fields)
            w.writerows(self.codes)
    
    
    def loadCodes(self):
        with open(self.tournamentsCodes, 'rb') as csvfile:
            self.codes = getReader( csvfile )
    
    
    
    
    
    

