# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:28:49 2014
@author: Gaspard, Thomas, Arnaud
"""

import re, os
from bs4 import BeautifulSoup

from utils  import *
from bdd    import *

url_players = 'http://www.atpworldtour.com/tennis/players/'

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
    'TurnedPro',
    'Country'  ]

def defaultPlayerCleanFunction(entry):
    return entry


class Players:
    
    def __init__(self, playerPath='', cleanPlayerPath=''):
        self.dic = dict()
        self.ID  = 0
        self.playersPath = playerPath
        self.cleanPlayerPath = cleanPlayerPath
        self.i = 0
        self.savePeriod = 20
    
    def isTreated(self, code):
        for t in self.dic:
            if self.dic[t]['Code'] == code:
                return True
        return False

    def addInfoPlayer(self, code):
        if self.isTreated(code):
            return False
        else:
            url = urlOpen( url_players + code + '.aspx' )
            dom = BeautifulSoup(url)
            aux = infoFromDOM(dom)
            playerURL = playersFromURL(url)
            aux.update( {
                "ID"        : self.ID,
                "Code"      : code,
                "IDPlayer"  : playerURL  } )
            self.dic[playerURL] = aux
            self.ID += 1
            self.saveMaybe()
            return True
    
    def save(self):
        with open(self.playersPath, 'wb') as csvfile:
            w = getWriter(csvfile, players_fields)
            w.writerows( sorted(self.dic.values(), key=lambda k: k['ID']) )
    def load(self):
        with open(self.playersPath, 'rb') as csvfile:
            self.dic = dict()
            self.ID = 0
            for p in getReader( csvfile ):
                p['ID'] = int( p['ID'] )
                if p['ID'] >= self.ID:
                    self.ID = p['ID'] + 1
                self.dic[ p['IDPlayer'] ] = p
    
    
    def saveMaybe(self):
        self.i += 1
        if self.i % self.savePeriod == 0:
            debug("Saving")
            self.save()
    
    def canLoad(self):
        return os.path.isfile(self.playersPath)
    
    
    def clean(self, cleanFunction=defaultPlayerCleanFunction):
        with open( self.cleanPlayerPath , 'wb') as f:
            w = getWriter(f, players_fields)
            with open( self.playersPath, 'rb' ) as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow( cleanFunction(e) )
    
    


def playersFromURL(url):
    return re.findall('Players\/(.*).aspx', url.geturl() )[0]



def infoFromDOM(dom):
    country = "NotFound"
    try :
        country = dom.find('div', {'id':'playerBioInfoFlag'} ).find('p').contents[0]
    except:
        printError("No country found !")
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
        elif field == u'Birthdate:':
            birth = re.findall('([0-9]*)\.([0-9]*)\.([0-9]*)', li.getText() )[0]
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
        'TurnedPro'     : turnedPro,
        'Country'       : country
    }

