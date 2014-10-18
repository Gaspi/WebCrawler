# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:28:49 2014
@author: Gaspard, Thomas, Arnaud
"""

import urllib
import re

from utils import *
from bdd   import *
from tournamentCrawler import *


url_tournament = 'http://www.atpworldtour.com/Scores/Archive-Event-Calendar.aspx'

tournaments_codes_fields = [ 'IDTournament', 'e', 'y', 'Indoor', 'TournamentType' ]


class Seasons:
    
    def __init__(self):
        self.codes = []
        self.ID = 0
    
    def addTournamentsFromTY(self, t, y):
        url = url_tournament + '?t='+str(t)+'&y='+str(y)
        dom = BeautifulSoup( urllib.urlopen(url) )
        tournaments = dom.find_all('tr','calendarFilterItem')
        
        for tr in tournaments:
            col = tr.find_all('td')
            link = col[4].find_all('a')
            if len(link) > 0 and link[0].contents[0][0:3] == 'SGL':
                a = re.findall('e=([0-9]+)\&y\=([0-9]+)' , link[0].attrs['href'])[0]
                e = int(a[0])
                y = int(a[1])
                tour =  {
                    'IDTournament': self.ID,
                    'e':e,
                    'y':y,
                    'Indoor': 0 if col[2].contents[0] == u'Outdoor' else 1,
                    'TournamentType':t   }
                self.codes.append( tour )
                self.ID += 1
    
    
    def addTournamentsFromAllTY(self, tList, yStart, yEnd):
        for t in tList:
            for y in range(yStart, yEnd+1):
                self.addTournamentsFromTY(t, y)
    
    
    def saveCodes(self, filename):
        with open(filename, 'wb') as csvfile:
            w = getWriter(csvfile, tournaments_codes_fields)
            w.writerows(self.codes)
    
    
    def loadCodes(self, filename):
        with open(filename, 'rb') as csvfile:
            self.codes = getReader( csvfile )
    
    
    
    
    
    

