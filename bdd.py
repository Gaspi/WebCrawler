# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:28:49 2014

@author: Gaspard, Thomas, Arnaud


"""

import csv




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


def getDictReader(csvFile):
    return csv.DictReader(csvFile, restval='?', delimiter='|')

def getReader(csvFile):
    return [ e for e in getDictReader(csvFile) ]








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


match_field_names_clean = [
    'IDMatch',
    'IDTournament',
    'Year',
    'Duration',
    'Timestamp',
    'Draw',
    'Indoor',
    'Surface',
    'TournamentPrize',
    'TournamentCurrency',
    'TournamentPrizeUSD',
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



tournaments_codes_fields = ['IDTournament',
                            'Indoor',
                            'TournamentType',
                            'TournamentCategory', 'e', 'y' ]  # Field de Sylvain


tournaments_infos_fields = [
    'IDTournament',
    'Tournament',
    'Indoor',
    'TournamentType',   # Field du site [1,2,4]
    'TournamentCategory',   # Field de Sylvain
    'Surface',
    'Country',
    'TournamentPrize',
    'Draw',
    'TournamentStart',
    'TournamentEnd', 'e', 'y' ]

tournaments_infos_fields_clean = [
    'IDTournament',
    'Tournament',
    'Indoor',
    'TournamentType',   # Field du site [1,2,4]
    'TournamentCategory',   # Field de Sylvain
    'Surface',
    'Country',
    'TournamentPrize',
    'TournamentCurrency',
    'TournamentPrizeUSD',
    'Draw',
    'TournamentStart',
    'TournamentEnd', 'e', 'y' ]



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
    
clean_players_fields = [
    'ID',
    'Code',
    'IDPlayer',
    'RealName',
    'DayBirth',
    'MonthBirth',
    'YearBirth',
    'Height',
    'Weight',
    'RightHanded',
    'TurnedPro',
    'Country'  ]




