# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:28:49 2014

@author: Gaspard, Thomas, Arnaud


"""

import csv


match_field_names = [
    'IDTournament',
    'Year',
    'Duration',
    'Timestamp',
    'Draw',
    'Indoor',
    'Surface',
    'TournamentPrize',
    'IDPlayer',
    'IDOpponent',
    'Win',
    'RoundNumber',
    'TournamentStart',
    'TournamentEnd',
    'TournamentCategory',
    'Scores',
    'WinnerScores',
    'LoserScores',
    'TieBreakScores',
    'Retirement',
    'Aces',
    'BreakPointsConverted',
    'BreakPointsConvertedTotal',
    'BreakPointsSaved',
    'BreakPointsSavedTotal',
    'DoubleFaults',
    'FirstServe',
    'FirstServePointsWon',
    'FirstServePointsWonTotal',
    'FirstServeReturnPointsWon',
    'FirstServeReturnPointsWonTotal',
    'FirstServeTotal',
    'ReturnGamesPlayed',
    'SecondServePointsWon',
    'SecondServePointsWonTotal',
    'SecondServeReturnPointsWon',
    'SecondServeReturnPointsWonTotal',
    'ServiceGamesPlayed',
    'TotalPointsWon',
    'TotalPointsWonTotal',
    'TotalReturnPointsWon',
    'TotalReturnPointsWonTotal',
    'TotalServicePointsWon',
    'TotalServicePointsWonTotal',
    'p',
    'r',
    't',
    'y'
]


def getWriter(csvFile, fields):
    w = csv.DictWriter(csvFile, fields,
                       restval='?', extrasaction='raise', delimiter='|')
    w.writeheader()
    return w

def getMatchWriter(csvFile):
    return getWriter(csvFile, match_field_names)


def writeMatch(writer, match):
    writer.writerow(match)

def writeTournament(writer, tournament):
    writer.writerows(tournament)



def getReader(csvFile):
    r = csv.DictReader(csvFile, restval='?', delimiter='|')
    res = [ e for e in r]
    return res

def getMatchReader(csvFile):
    return getReader(csvFile, match_field_names)


def readMatch(reader, match):
    reader.writerow(match)

def readTournament(reader, tournament):
    reader.writerows(tournament)









