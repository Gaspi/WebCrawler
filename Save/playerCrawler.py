# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:28:49 2014
@author: Gaspard, Thomas, Arnaud
"""


import urllib
import re
import sets
import csv
from bs4 import BeautifulSoup

from utils  import *
from bdd    import *

players_fields = [
    'ID',
    'Code',
    'IDPlayer',
    'DayBirth',
    'MonthBirth',
    'YearBirth',
    'Height',
    'Weight',
    'RightHanded',
    'TurnedPro' ]

class Players:
    
    def __init__(self):
        self.dic = dict()
        self.codes = sets.Set()
        self.ID  = 0
    
    def addPlayer(self, code, verbose=True):
        self.codes.add(code)
    
    def addPlayers(self, l):
        for i in l:
            self.addPlayer(i)
    
    def fetchInfoPlayers(self):
        length = len( self.codes )
        chrono = Chrono()
        chrono.start( length )
        length = str(length)
        for code in self.codes:
            try:
                url = urllib.urlopen( 'http://www.atpworldtour.com/tennis/players/' + code + '.aspx' )
                dom = BeautifulSoup(url)
                aux = infoFromDOM(dom)
                playerURL = playersFromURL(url)
                aux.update( {
                    "ID"        : self.ID,
                    "Code"      : code,
                    "IDPlayer"  : playerURL
                    } )
                self.dic[playerURL] = aux
                chrono.tick()
                if chrono.i % 20 == 0:
                    chrono.printRemaining()
                self.ID += 1
            except:
                debug("Error !!! Parameters: " + str(code) )
    
    
    def addPlayersFromTournament(self, e, y):
        url = 'http://www.atpworldtour.com/Share/Event-Draws.aspx?e='+str(e)+'&y='+str(y)
        content = urllib.urlopen(url).read()
        self.addPlayers( re.findall('players\/(.*)\.asp', content) )
    
    
    def saveCodes(self, filename):
        with open(filename, 'wb') as csvfile:
            w = csv.writer(csvfile, delimiter=' ', quotechar='|')
            w.writerow( list(self.codes) )
    
    def savePlayers(self, filename):
        with open(filename, 'wb') as csvfile:
            w = getWriter(csvfile, players_fields )
            w.writerows( sorted(self.dic.values(), key=lambda k: k['ID']) )
            
    def loadCodes(self, filename):
        with open(filename, 'rb') as csvfile:
            r = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.codes = r.next()
    
    def loadPlayers(self, filename):
        with open(filename, 'rb') as csvfile:
            self.dic = dict()
            for p in getReader( csvfile ):
                self.dic[ p['IDPlayer'] ] = { 'ID':p['ID'] }


def playersFromURL(url):
    return re.findall('Players\/(.*).aspx', url.geturl() )[0]



def infoFromDOM(dom):
    f = dom.find('ul', {'id':'playerBioInfoList'} ).find_all('li')
    birth       = ['-1','-1','-1']
    height      = -1
    weight      = -1
    handed      = -1
    turnedPro   = -1
    for li in f:
        field = li.find('span').contents[0]
        if field == u'Age:':
            birth = re.findall('\(([0-9]*)\.([0-9]*)\.([0-9]*)\)', li.getText() )[0]
        elif field == u'Height:':
            height = int( re.findall('\(([0-9]*) cm\)', li.getText())[0] )
        elif field == u'Weight:':
            weight = int( re.findall('\(([0-9]*) kg\)', li.getText())[0] )
        elif field == u'Turned Pro:':
            turnedPro = int( re.findall(' ([0-9]+)', li.getText())[0] )
        elif field == u'Plays:':
            if re.findall('Right', li.getText()):
                handed = 1
            elif re.findall('Left', li.getText()):
                handed = 0
    return {
        'DayBirth'      : int( birth[0] ),
        'MonthBirth'    : int( birth[1] ),
        'YearBirth'     : int( birth[2] ),
        'Height'        : height,
        'Weight'        : weight,
        'RightHanded'   : handed,
        'TurnedPro'     : turnedPro
    }




