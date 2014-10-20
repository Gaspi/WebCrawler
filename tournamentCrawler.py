# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:12:51 2014

@author: Gaspard, Thomas, Arnaud
"""

import datetime, time, re
from utils import *


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





