# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 10:31:07 2014

@author: Gaspard
"""

import urllib
import re
import sets
import numpy as np

from utils import *
from bdd   import *
from tournamentCrawler import *


url_tournament = 'http://www.atpworldtour.com/Scores/Archive-Event-Calendar.aspx'

tournaments_codes_fields = [ 'e', 'y' ]
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
        self.tour = []
        self.ID = 0
        
        self.codes = []
        
        self.path
        self.playerCodesPath
        self.tournamentsPath
        self.playerCodes = sets.Set()
    
    
    
    def saveCodes(self):
        with open(self.playerCodesPath, 'wb') as csvfile:
            w = csv.writer(csvfile, delimiter=' ', quotechar='|')
            w.writerow( list(self.codes) )
    def loadCodes(self):
        with open(self.playerCodesPath, 'rb') as csvfile:
            r = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.codes = sets.Set(r.next())
    
    def saveTournamentsFromCode(self, code):
        e = code['e']
        y = code['y']
        filename = self.path + str(y) + 'e' + str(e) + '.csv'
        if not os.path.exists( filename ):
            (newPlayers, newTour) = getAllTournamentInfos(code)
            self.tour.append( newTour )
    
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
                t =  {'e':e,'y':y}
                if not t in self.codes:
                    self.codes.append( t )
                    indoor = 0 if col[2].contents[0] == u'Outdoor' else 1
                    newTour = getTournamentInfos(e, y, {'IDTournament': self.ID, 'Indoor':indoor, 'TournamentType':t } )
                    self.tour.append( newTour )
                    self.ID += 1
                else:
                    print str(t)
    
    
    
    
    def addTournamentsFromYears(self, t, start, end):
        for y in range(start,end+1):
            self.addTournamentsFromTY(t, y)
            debug("Type: " + str(t) + " , Year: " + str(y) + "  -> Done.")
    
    
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
    
    
    def saveCodes(self, filename):
        with open(filename, 'wb') as csvfile:
            w = getWriter(csvfile, tournaments_codes_fields)
            w.writerows(self.codes)
    
    def loadCodes(self, filename):
        with open(filename, 'rb') as csvfile:
            self.codes = getReader( csvfile )
    
    def saveTournaments(self, filename):
        with open(filename, 'wb') as csvfile:
            w = getWriter(csvfile, tournaments_infos_fields )
            w.writerows(self.tour)
    def loadTournaments(self, filename):
        with open(filename, 'rb') as csvfile:
            self.tour = getReader( csvfile )
    




