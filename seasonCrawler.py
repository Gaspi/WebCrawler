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




def getTourFromRow(row, needLink = True):
    col = row.find_all('td')
    link = col[4].find_all('a')
    if needLink:
        pass
    else:
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
            return { 'IDTournament': self.ID,
                     'e':e,  'y':y,
                     'Indoor': 0 if col[2].contents[0] == u'Outdoor' else 1,
                    'TournamentType': t,
                    'TournamentCategory': c    }

class Seasons:
    
    def __init__(self, fs):
        self.codes = []
        self.ID = 0
        self.tournamentsCodes = fs.tournaments_codes
    
    def addTournamentsFromTY(self, t, y, needLink = True):
        dom = getDOM( url_tournament + '?t='+str(t)+'&y='+str(y) )
        tournaments = dom.find_all('tr','calendarFilterItem')
        
        for tr in tournaments:
            col = tr.find_all('td')
            link = col[4].find_all('a')
            if len(link) > 0 and link[0].contents[0][0:3] == 'SGL':
                a = re.findall('e=([0-9]+)\&y\=([0-9]+)' , link[0].attrs['href'])[0]
                e = int(a[0])
                y = int(a[1])
                cat = getCategory( col[1].contents[-1] )
                tour =  {
                    'IDTournament': self.ID,
                    'e':e,
                    'y':y,
                    'Indoor': 0 if col[2].contents[0] == u'Outdoor' else 1,
                    'TournamentType': t,
                    'TournamentCategory': cat }
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
    
    
def getAllTournamentsFromTY(t, y):
    dom = getDOM( url_tournament + '?t='+str(t)+'&y='+str(y) )
    tournaments = dom.find_all('tr','calendarFilterItem')
    res = []
    for tr in tournaments:
        col = tr.find_all('td')
        name  = col[1].contents[0].contents[0]
        place = col[1].contents[2].contents[0]
        cat   = col[1].contents[4]
        indoor = col[2].contents[0]
        res.append( {'StartDate':col[0].contents[0],
                     'Name': " ".join( [name, place, cat] ),
                     'Indoor': int(indoor == u'Indoor'),
                     'TournamentType': t,
                     'TournamentCategory': getCategory( cat )    }  )
    return res



def getCategory(cat):
    if   cat == u'Grand Slams':
        return 0
    elif cat == u'ATP World Tour Masters 1000':
        return 1
    elif cat == u'ATP World Tour 500':
        return 2
    elif cat == u'ATP World Tour 250':
        return 3
    elif cat == u'ATP Challenger Tour':
        return 4
    else:
        return -1
