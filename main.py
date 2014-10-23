# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 09:16:48 2014
@authors: Gaspard, Thomas
"""

import sys
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
from FileSystem             import *

infoReader = InfoReader('localurl.txt')

fs = FileSystem(infoReader)  # reads 4 lines

folder              = fs.folder
matches_folder      = fs.matches_folder
ranksFolder         = fs.ranksFolder
cleanFolder         = fs.cleanFolder

yearStart           = infoReader.readInt()
yearEnd             = infoReader.readInt()
tournamentTypes     = infoReader.readIntList()
sleepingTime        = infoReader.readInt()
CrawlingSeasons     = infoReader.readBool()
CrawlingTournaments = infoReader.readBool()
CrawlPlayers        = infoReader.readBool()
CrawlATPRanks       = infoReader.readBool()
CrawlMatches        = infoReader.readBool()
MergeMatches        = infoReader.readBool()
CleaningTournaments = infoReader.readBool()
CleaningPlayers     = infoReader.readBool()
CleaningMatches     = infoReader.readBool()
AddRankings         = infoReader.readBool()
debugMode           = infoReader.readBool()
refreshTime         = infoReader.readInt()

tournaments_codes = fs.tournaments_codes 
tournaments_save  = fs.tournaments_save
player_codes      = fs.player_codes
player_save       = fs.player_save
treated_path      = fs.treated_path
matches_path      = fs.matches_path
rankingsSave      = fs.rankingsSave

cleanPlayerPath     = fs.cleanPlayerPath
cleanTournamentsPath= fs.cleanTournamentsPath
cleanMatchesPath    = fs.cleanMatchesPath

debug("Done.")


def mainBody():
    
    debug("Initialisation...")
    clock       = Clock()
    clock.clock()
    
    seasons     = Seasons(    tournaments_codes )
    tournaments = Tournaments(tournaments_save, player_codes, cleanTournamentsPath)
    players     = Players(    player_save, cleanPlayerPath  )
    matchCrawler= Matches(    matches_folder    )
    matchMerger = MatchMerger(matches_folder, matches_path,cleanMatchesPath)
    atpRank     = ATPRank( ranksFolder )
    atpRankings = ATPRankings( ranksFolder, matches_path, rankingsSave, cleanMatchesPath )

    chrono      = Chrono()
    chrono.periodTime = refreshTime
    clock.done()
    
    
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
    clock.done()
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
            if chrono.needPrint():
                printLine("Tournaments " + str(chrono.i) + " / " + lengthTour +
                      " treated. Players found: " + str(len(tournaments.playerCodes)) +
                      " Remaining: " + chrono.remaining() )
#                chrono.printRemaining()
        tournaments.save()
        print
    
    clock.done()
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
                if chrono.needPrint(): chrono.printRemaining()
            else:
                chrono.decTotal()
        players.save()
    matchCrawler.dicoPlayers = players.dic
    clock.done()
    
    
    
    if CrawlMatches:
        debug("Fetching informations for all matches...")
        chrono.start( int(lengthTour) )
        for t in tournaments.tournaments:
            if matchCrawler.treatTournament( t ):
                chrono.tick()
                if chrono.needPrint(): chrono.printRemaining()
            else:
                chrono.decTotal()
        debug("All tournaments: Done. " + clock.strClock())
    
    
    
    if MergeMatches:
        debug("Merging all tournaments...")
        matchMerger.startMerging( tournaments.tournaments )
        clock.done()
    
    if CrawlATPRanks:
        debug("Crawling all " + numberPlayers + " ranking histories...")
        chrono.start( int(numberPlayers) )
        for i in players.dic:
            if atpRank.addATPRank( players.dic[i] ):
                chrono.tick()
                if chrono.needPrint(): chrono.printRemaining()
            else:
                chrono.decTotal()
        clock.done()
    
    
    if CleaningTournaments:
        debug("Cleaning tournaments...")
        tournaments.clean()
        clock.done()
    
    if CleaningPlayers:
        debug("Cleaning players...")
        players.clean()
        clock.done()
    
    if CleaningMatches:
        debug("Cleaning matches...")
        chrono.start(0)
        matchMerger.clean( chrono )
        clock.done()
    
    atpRankings.playersNb = players.ID
    atpRankings.tournaments = tournaments.tournaments
    atpRankings.loadPlayedTournaments()
    if AddRankings:
        debug("Computing played tournaments...")
        atpRankings.startFeedingMatches()
        atpRankings.savePlayedTournaments()
        clock.done()
        
        debug("Computing rankings...")
        atpRankings.startComputingRanks()
        clock.done()
        
        debug("Cleaning rankings...")
        atpRankings.clean()
        clock.done()
    
    return True


clock       = Clock()
clock.clock()

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
debug("Duration: " + clock.strClock())






