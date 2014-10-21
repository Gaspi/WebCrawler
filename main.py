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


yearStart = 2000
yearEnd = 2014
tournamentTypes = [1,2,4]

#folder = 'C:\\Users\\Gaspard\\Dropbox2\\Dropbox\\WebCrawling 2.0\\WebCrawler\\2000to2014\\'
#matches_folder    = folder + "tournaments\\"
folder = '/cal/homes/tbraun/Documents/Webmining/WebCrawler/2000to2014/'
matches_folder    = folder + "tournaments/"
CrawlingSeasons     = True
CrawlingTournaments = True
CrawlPlayers        = True
CrawlMatches        = True
MergeMatches        = True
CleaningTournaments = True
CleaningPlayers     = True
CleaningMatches     = True
sleepingTime = 30

tournaments_codes = folder + "tournamentCodes.csv"
tournaments_save  = folder + "tournaments.csv"
player_codes      = folder + "playerCodes.csv"
player_save       = folder + "players.csv"
treated_path      = folder + "treated.csv"
matches_path      = folder + "matches.csv"

try:    os.stat( folder)
except: os.mkdir(folder)
try:    os.stat( matches_folder)
except: os.mkdir(matches_folder)

debug("Done.")




def mainBody():
    
    debug("Initialisation...")
    
    seasons     = Seasons(    tournaments_codes )
    tournaments = Tournaments(tournaments_save, player_codes)
    players     = Players(    player_save       )
    matchCrawler= Matches(    matches_folder    )
    matchMerger = MatchMerger(matches_folder, matches_path  )
    
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
        i = 0
        for code in seasons.codes:
            chrono.tick()
            tournaments.addTournamentFromCode(code)
            i += 1
            if i % 20 == 0:
                debug("Tournaments " + str(i) + " / " + lengthTour +
                      " treated. Players found: " + str(len(tournaments.playerCodes)) +
                      "  Remaining: " + str( chrono.remaining() ) )
        tournaments.save()
    
    debug("Done. " + clock.strClock())
    numberPlayers = str( len(tournaments.playerCodes) )
    debug("Found: " + numberPlayers + " players" )
    
    
    if players.canLoad():
        debug("Loading...")
        players.load()
    
    if CrawlPlayers:
        debug("Looking for all " + numberPlayers + " players...")
    
        chrono.start( int(numberPlayers) )
        i = 0
        for code in tournaments.playerCodes:
            chrono.tick()
            players.addInfoPlayer(code)
            i += 1
            if i % 20 == 0: chrono.printRemaining()
        players.save()
    matchCrawler.dicoPlayers = players.dic
    debug("Done. " + clock.strClock())
    
    
    if CrawlMatches:
        debug("Fetching informations for all matches...")
        chrono.start( int(lengthTour) )
        for t in tournaments.tournaments:
            matchCrawler.treatTournament( t )
            chrono.tick()
            if chrono.i % 5 == 0:
                chrono.printRemaining()
            
        debug("All tournaments: Done. " + clock.strClock())
    
    
    
    if MergeMatches:
        debug("Merging all matches...")
        matchMerger.startMerging( tournaments.tournaments )
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
    
    return True



keepOn = True
while keepOn:
    keepOn = False
    try :
        mainBody()
    except:
        printError("Network error expected: " + str( sys.exc_info()[0] ) )
        time.sleep( sleepingTime )
        debug("Waking up !")
        keepOn = True
        

debug("C'est fini !!!")





