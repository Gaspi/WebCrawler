# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 09:16:48 2014
@authors: Gaspard, Thomas, Arnaud
"""

import os, sys
from utils                  import *
from tournamentCrawler      import *
from matchCrawler           import *
from bdd                    import *
from playerCrawler          import *
from tournamentInfoCrawler  import *
from seasonCrawler          import *
from matchMerger            import *
from ATPRankCrawler         import *
from ATPRankings            import *



folder = ''
matches_folder = ''
ranksFolder =  ''
yearStart = 0
yearEnd = 0
tournamentTypes = []
sleepingTime = 0
CrawlingSeasons     = True
CrawlingTournaments = True
CrawlPlayers        = True
CrawlATPRanks       = True
CrawlMatches        = True
MergeMatches        = True
CleaningTournaments = True
CleaningPlayers     = True
CleaningMatches     = True
AddRankings         = True
debugMode           = False
with open('localurl.txt', 'rb') as f:
    lines = f.readlines()
    folder          = cleanLine(lines[0])
    matches_folder  = cleanLine(lines[1])
    ranksFolder     = cleanLine(lines[2])
    yearStart       = int( cleanLine(lines[4]) )
    yearEnd         = int( cleanLine(lines[6]) )
    tournamentTypes = [ int(e) for e in  cleanLine(lines[8]).split(',')  ]
    sleepingTime    = int( cleanLine(lines[10]) )
CrawlingSeasons     = getBool(cleanLine(lines[12]))
CrawlingTournaments = getBool(cleanLine(lines[14]))
CrawlPlayers        = getBool(cleanLine(lines[16]))
CrawlATPRanks       = getBool(cleanLine(lines[18]))
CrawlMatches        = getBool(cleanLine(lines[20]))
MergeMatches        = getBool(cleanLine(lines[22]))
CleaningTournaments = getBool(cleanLine(lines[24]))
CleaningPlayers     = getBool(cleanLine(lines[26]))
CleaningMatches     = getBool(cleanLine(lines[28]))
AddRankings         = getBool(cleanLine(lines[30]))
debugMode           = getBool(cleanLine(lines[32]))
try:    os.stat( folder)
except: os.mkdir(folder)
try:    os.stat( matches_folder)
except: os.mkdir(matches_folder)
try:    os.stat( ranksFolder)
except: os.mkdir(ranksFolder)

tournaments_codes = folder + "tournamentCodes.csv"
tournaments_save  = folder + "tournaments.csv"
player_codes      = folder + "playerCodes.csv"
player_save       = folder + "players.csv"
treated_path      = folder + "treated.csv"
matches_path      = folder + "matches.csv"

debug("Done.")




def mainBody():
    
    debug("Initialisation...")
    
    seasons     = Seasons(    tournaments_codes )
    tournaments = Tournaments(tournaments_save, player_codes)
    players     = Players(    player_save       )
    matchCrawler= Matches(    matches_folder    )
    matchMerger = MatchMerger(matches_folder, matches_path  )
    atpRank     = ATPRank( ranksFolder )
    atpRankings = ATPRankings( ranksFolder, matches_path )
    chrono      = Chrono()
    clock       = Clock()
    clock.clock()
    debug("Done. ")
    
    
    if CrawlingSeasons:
        debug("Looking for all tournaments (types " + str(tournamentTypes) +
              ") from " + str(yearStart) + " to " + str(yearEnd) + "...")
        seasons.addTournamentsFromAllTY( tournamentTypes, yearStart, yearEnd )
        debug("Saving information...")
        seasons.saveCodes( )
    else:
        debug("Loading all tournaments (types " + str(tournamentTypes) +
              ") from " + str(yearStart) + " to " + str(yearEnd) + "...")
        seasons.loadCodes()
    
    lengthTour = str( len(seasons.codes) )
    debug("Done. " + clock.strClock())
    debug("Found: " + lengthTour + " tournaments")
    
    
    if tournaments.canLoad():
        debug("Loading...")
        tournaments.load()
    
    if CrawlingTournaments:
        debug("Crawling all tournaments (types " + str(tournamentTypes) +
            ") from " + str(yearStart) + " to " + str(yearEnd) + "...")
        chrono.start( int(lengthTour) )
        for code in seasons.codes:
            tournaments.addTournamentFromCode(code)
            chrono.tick()
            if chrono.i % 20 == 0:
                debug("Tournaments " + str(chrono.i) + " / " + lengthTour +
                      " treated. Players found: " + str(len(tournaments.playerCodes)))
                chrono.printRemaining()
        tournaments.save()
    
    debug("Done. " + clock.strClock())
    numberPlayers = str( len(tournaments.playerCodes) )
    debug("Found: " + numberPlayers + " players" )
    
    
    if players.canLoad():
        debug("Loading players...")
        players.load()
    
    if CrawlPlayers:
        debug("Looking for all " + numberPlayers + " players...")
    
        chrono.start( int(numberPlayers) )
        for code in tournaments.playerCodes:
            if players.addInfoPlayer(code):
                chrono.tick()
                if chrono.i % 20 == 0: chrono.printRemaining()
            else:
                chrono.decTotal()
        players.save()
    matchCrawler.dicoPlayers = players.dic
    debug("Done. " + clock.strClock())
    
    
    
    if CrawlMatches:
        debug("Fetching informations for all matches...")
        chrono.start( int(lengthTour) )
        for t in tournaments.tournaments:
            if matchCrawler.treatTournament( t ):
                chrono.tick()
                if chrono.i % 5 == 0: chrono.printRemaining()
            else:
                chrono.decTotal()
        debug("All tournaments: Done. " + clock.strClock())
    
    
    
    if MergeMatches:
        debug("Merging all matches...")
        matchMerger.startMerging( tournaments.tournaments )
        debug("Done. " + clock.strClock())
    
    
    if CrawlATPRanks:
        debug("Crawling all " + numberPlayers + " ranking histories...")
        chrono.start( int(numberPlayers) )
        for i in players.dic:
            if atpRank.addATPRank( players.dic[i] ):
                chrono.tick()
                if chrono.i % 20 == 0: chrono.printRemaining()
            else:
                chrono.decTotal()
        debug("Done. " + clock.strClock())
    
    
    if CleaningTournaments:
        debug("Cleaning tournaments...")
        tournaments.clean()
        debug("Done. " + clock.strClock())
    
    if CleaningPlayers:
        debug("Cleaning players...")
        players.clean()
        debug("Done. " + clock.strClock())
    
    if CleaningMatches:
        debug("Cleaning matches...")
        matchMerger.clean()
        debug("Done. " + clock.strClock())
    
    if AddRankings:
        debug("Computing rankings...")
        atpRankings.setNumberOfPlayers( players.ID )
        atpRankings.setTournaments = tournaments.tournaments
        atpRankings.startFeedingMatches()
        # do stuff here
        debug("Done. " + clock.strClock())
    
    return True



if debugMode:
    mainBody()
else:
    keepOn = True
    while keepOn:
        keepOn = False
        try :
            mainBody()
        except:
            printError("Network error expected: " + str( sys.exc_info()[0] ) )
            debug("Going to sleep for " + str(sleepingTime) + " seconds...")
            time.sleep( sleepingTime )
            debug("Waking up !")
            keepOn = True
        

debug("C'est fini !!!")







