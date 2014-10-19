# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:12:51 2014

@author: Gaspard, Thomas, Arnaud
"""

import datetime
import time
import re

from utils import *
from matchCrawler import *



def createChronology(date, round_):
    return int(time.mktime(datetime.datetime.strptime(date,"%d.%m.%Y").timetuple()))*10 + int(round_)


tournaments_fields = [
    'Year',
    'RoundNumber',
    'WinnerScores',
    'LoserScores',
    'TieBreakScores',
    'Tournament',
    'TournamentPrize',
    'Surface',
    'Draw',
    'Country',
    'IDTournament',
    'TournamentStart',
    'TournamentEnd',
    'Retirement',
    'Timestamp',
    't', 'y', 'r', 'p' ]


def getTournamentHTML(e,y):
    return getHTML( 'http://www.atpworldtour.com/Share/Event-Draws.aspx?e=' +
            str(e) + '&y=' + str(y) )

def parseTournamentInfos(content, infos):
    draw        = re.findall("Draw: <\/span>([0-9]+)<\/p>", content)[0]
    surface     = re.findall("Surface: <\/span>(.*)<\/p>", content)[0]
    prizeMoney  = re.findall("Prize Money: <\/span>(.*)<\/p>", content)[0].replace(",","")
    tournament  = re.findall("<a class=\"tournamentTitle\".*>(.*)<\/a><\/h3>", content)
    if len( tournament ) == 0:
        tournament = re.findall("<span class=\"tournamentTitle\"><strong>(.*)</strong></span><\/h3>", content)
    subtitle = re.findall("<p class=\"tournamentSubTitle\">(.*) - (.*)-(.*)<\/p>", content)[0]
    country         = subtitle[0]
    tournamentStart = subtitle[1]
    tournamentEnd   = subtitle[2]
    res = infos.copy()
    res.update( {
            'Tournament'        : tournament[0] ,
            'TournamentPrize'   : prizeMoney,
            'Surface'           : surface,
            'Draw'              : draw,
            'Country'           : country,
            'TournamentStart'   : tournamentStart,
            'TournamentEnd'     : tournamentEnd     } )
    return res

def getTournamentInfos(e, y, infos):
    res = parseTournamentInfos( getTournamentHTML(e, y), infos)
    res['e'] = e
    res['y'] = y
    return res


def getAllTournamentInfos(dico):
    content = getTournamentHTML( dico['e'], dico['y'] )
    return (re.findall('players\/(.*)\.asp', content) ,
            parseTournamentInfos(content, dico) )


def getTournament(e, y, infos):
    content = getTournamentHTML(e,y)
    
    tournamentInfos = parseTournamentInfos(content, infos)
    del tournamentInfos['Country']
    del tournamentInfos['Tournament']
    
    occurences = re.findall("openWin\(\'\/Share\/Match\-Facts\-Pop\-Up\.aspx\?t\=([0-9]+)&y\=([0-9]+)&r\=([0-9]+)\&p=([A-Z0-9]+)\'.*\>([0-9].*)<\/a>", content)
    result = []
    
    for i in range(len(occurences)):
        occurence = occurences[i]
        if re.findall('\) RET', occurence[4]):
            sets = []
            winnerScores = ["RETWIN"]
            loserScores = ["RETLOSE RET"]
        else:
            sets = occurence[4].split(", ")
            winnerScores = [s.split("-")[0] for s in sets]
            loserScores = [s.split("-")[1].split("(")[0] for s in sets]
        
        retirement = False
        if loserScores[-1][-3:] == "RET":
            loserScores[-1] = loserScores[-1][:-4]
            retirement = True
        tieBreakScores = []
        for s in sets:
            tmp = s.split("-")[1].split("(")
            if (len(tmp) > 1):
                tieBreakScores.append(tmp[1][:-1])
            else:
                tieBreakScores.append("-1")

        matchInfo = tournamentInfos.copy()
        matchInfo.update( {
            't' : occurence[0],
            'y' : occurence[1],
            'r' : occurence[2],
            'p' : occurence[3],
            'Year'              : int(occurence[1]),
            'RoundNumber'       : int(occurence[2]),
            'WinnerScores'      : winnerScores,
            'LoserScores'       : loserScores,
            'TieBreakScores'    : tieBreakScores,
            'Retirement'        : int( retirement ),
            'Timestamp'         : createChronology( matchInfo['TournamentStart'], int(occurence[2]) )
        })
        result.append( matchInfo )
    return result




def getMatchesOfTournament(e, y, infos, dicoPlayers, verbose=None, sleep=None):
    tournament = getTournament(e,y, infos)
    result = []
    index = 0
    l = len(tournament)
    for m in tournament:
        index += 1
        tab = addMatchInfos(m, dicoPlayers)
        result.append( tab[0] )
        result.append( tab[1] )
        if sleep  : time.sleep( sleep )
        if verbose: debug( str(index) + " / " + str(l) )
    return result
    



