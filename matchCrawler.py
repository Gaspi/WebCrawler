# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 16:56:45 2014

@author: Gaspard, Thomas, Arnaud
"""

from utils import *

import urllib
from bs4 import BeautifulSoup

import re, os


mc_url_matches = "http://www.atpworldtour.com/Share/Match-Facts-Pop-Up.aspx"

mc_fields = {
#    'Tournament'                : [ 0 , 'a' , None  ],
#    'Round'                     : [ 1 , 'td', None  ],
#    'Name'                      : [ 4 , 'a' , 'str' ],
#    'Country'                   : [ 5 , 'p' , 'str' ],
    'Aces'                      : [ 6 , 'td', 'int' ],
    'DoubleFaults'              : [ 7 , 'td', 'int' ],
    'FirstServe'                : [ 8 , 'td', 'stat'],
    'FirstServePointsWon'       : [ 9 , 'td', 'stat'],
    'SecondServePointsWon'      : [ 10, 'td', 'stat'],
    'BreakPointsSaved'          : [ 11, 'td', 'stat'],
    'ServiceGamesPlayed'        : [ 12, 'td', 'int' ],
    'FirstServeReturnPointsWon' : [ 13, 'td', 'stat'],
    'SecondServeReturnPointsWon': [ 14, 'td', 'stat'],
    'BreakPointsConverted'      : [ 15, 'td', 'stat'],
    'ReturnGamesPlayed'         : [ 16, 'td', 'int' ],
    'TotalServicePointsWon'     : [ 17, 'td', 'stat'],
    'TotalReturnPointsWon'      : [ 18, 'td', 'stat'],
    'TotalPointsWon'            : [ 19, 'td', 'stat']
    }



class Matches:
    
    def __init__(self):
        self.matchesPath = ''
        self.dicoPlayers = dict()
    
    def getPath(self, e, y):
        return self.matchesPath + "y" + str(t['y']) + "e" + str(t['e'])
    
    def isTreated(self, path):
        try :
            os.path.isfile( path  )
            return True
        except:
            return False
    
    def treatTournament(self, t):
        e = int( t['e'] )
        y = int( t['y'] )
        path = self.getPath(e, y)
        if not self.isTreated(path):
            matches = getMatchesOfTournament( t['e'], t['y'],
                    {'IDTournament': t['IDTournament'],
                     'Indoor':t['Indoor'] },
                    self.dicoPlayers )
            save(path, matches)
    
    def save(self, path, matches):
        with open(path+"u", 'wb') as f:
                w = getMatchWriter(f)
                writeTournament(w, matches)
                os.rename( path+"u", path)





def parseSimple(line, balise):
    return line.find(balise).contents[0]

def parseStr(line, balise):
    aux = line.find_all(balise)
    return [ aux[0].contents[0], aux[1].contents[0] ]

def parseInt(line, balise):
    aux = parseStr(line,balise)
    return [ int(aux[0]), int(aux[1]) ]

def parseStat(line, balise):
    aux = parseStr(line,balise)
    s1 = re.findall( "\((.*)/(.*)\)", aux[0])[0]
    s2 = re.findall( "\((.*)/(.*)\)", aux[1])[0]
    return [ int(s1[0]), int(s1[1]), int(s2[0]), int(s2[1]) ]


def getInfoRows(t,y,r,p):
    dom = getDOM( mc_url_matches + "?t=" + t + "&y=" + y + "&r=" + r + "&p=" + p)
    a = dom.find_all('tr', 'infoRow')
    if len(a) != 20:
        return printError("Mauvaise longueur : " + str(len(a)) + " != 20")
    return a

def getMatchInfos(t,y,r,p):
    a = getInfoRows(t,y,r,p)
    result = [ dict(), dict() ]
    
    for k,v in mc_fields.iteritems():
        line   = a[v[0]]
        balise = v[1]
        if v[2] == 'str':
            l = parseStr(line, balise)
            result[0][k] = l[0]
            result[1][k] = l[1]
        elif v[2] == 'int':
            l = parseInt(line, balise)
            result[0][k] = l[0]
            result[1][k] = l[1]
        elif v[2] == 'stat':
            l = parseStat(line, balise)
            result[0][k]            = l[0]
            result[0][k + "Total"]  = l[1]
            result[1][k]            = l[2]
            result[1][k + "Total"]  = l[3]
        else:
            result[0][k] = parseSimple(line, balise)
            result[1][k] = parseSimple(line, balise)
    
    
    duration = int( re.findall('([0-9]+)', parseSimple(a[2], 'td'))[0] )
    result[0]['Duration'] = duration
    result[1]['Duration'] = duration
    
    result[0]["IDPlayer"] = re.findall('Players\/(.*).aspx\'\,\'_blank', a[4].find_all('a')[0].attrs['onclick'] )[0]
    result[1]["IDPlayer"] = re.findall('Players\/(.*).aspx\'\,\'_blank', a[4].find_all('a')[1].attrs['onclick'] )[0]
    result[0]['IDOpponent'] = result[1]['IDPlayer']
    result[1]['IDOpponent'] = result[0]['IDPlayer']
    
    namePlayers = parseStr(   a[4], 'a')
    win         = parseSimple(a[3], 'a')
    result[0]['Win'] = int(win == namePlayers[0] )
    result[1]['Win'] = int(win == namePlayers[1] )
    
    return result


def addMatchInfos(match, dicoPlayers):
    m = getMatchInfos( match['t'], match['y'], match['r'], match['p'] )
    for field in match:
        m[0][field] = match[field]
        m[1][field] = match[field]
    m[0]['Scores'] =  m[0]['WinnerScores'] if m[0]['Win'] else m[0]['LoserScores']
    m[1]['Scores'] =  m[1]['WinnerScores'] if m[1]['Win'] else m[1]['LoserScores']
    
    # May generate errors !!!
    m[0]['IDOpponent'] = dicoPlayers[ m[0]['IDOpponent'] ]['ID']
    m[1]['IDOpponent'] = dicoPlayers[ m[1]['IDOpponent'] ]['ID']
    m[0]['IDPlayer']   = dicoPlayers[ m[0]['IDPlayer'  ] ]['ID']
    m[1]['IDPlayer']   = dicoPlayers[ m[1]['IDPlayer'  ] ]['ID']
    
    return m








