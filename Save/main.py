# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 09:16:48 2014
@authors: Gaspard, Thomas, Arnaud
"""

from utils                  import *
from tournamentCrawler      import *
from matchCrawler           import *
from bdd                    import *
from searchCrawler          import *
from playerCrawler          import *
from tournamentInfoCrawler  import *
from seasonCrawler          import *
import time





debug("Initialisation...")
yearStart = 2013
yearEnd = 2013
tournamentTypes = [1,2, 4]
folder = 'C:\\Users\\Gaspard\\Dropbox2\\Dropbox\\PESTOCrawling'
try: os.stat(folder)
except: os.mkdir(folder)
tournaments_codes = folder + "tournamentCodes.csv"
tournaments_save  = folder + "tournaments.csv"
player_codes      = folder + "playerCodes.csv"
player_save       = folder + "players.csv"

chrono      = Chrono()
seasons     = Seasons()
tournaments = Tournaments()
players     = Players()
clock       = Clock()
clock.clock()
debug("Done. ")



if True:
    debug("Looking for all tournaments (types " + str(tournamentTypes) +
        ") from " + str(yearStart) + " to " + str(yearEnd) + "...")
    seasons.addTournamentsFromAllTY( tournamentTypes, yearStart, yearEnd )
    debug("Saving information...")
    seasons.saveCodes( tournaments_codes )
lengthTour = str( len(seasons.codes) )
debug("Done. " + clock.strClock())
debug("Found: " + lengthTour + " tournaments")
sys.exit()

# Should run in a few minutes
# TODO : decide the starting datas



if True:
    debug("Looking for all tournaments (types " + str(tournamentTypes) +
        ") from " + str(yearStart) + " to " + str(yearEnd) + "...")
    for t in tournamentTypes:
        tournaments.addTournamentsFromYears( t, yearStart, yearEnd )
    debug("Saving information...")
    tournaments.saveCodes( tournaments_codes )
    tournaments.saveTournaments(tournaments_save)
else:
    debug("Loading all tournaments (types " + str(tournamentTypes) +
        ") from " + str(yearStart) + " to " + str(yearEnd) + "...")
    tournaments.loadCodes(tournaments_codes)
    tournaments.loadTournaments(tournaments_save)


lengthTour = str( len(tournaments.codes) )
debug("Done. " + clock.strClock())
debug("Found: " + lengthTour + " tournaments")



if True:
    debug("Looking for all players in all the " + lengthTour + " tournaments.")
    chrono.start( int(lengthTour) )
    for tournament in tournaments.codes:
        players.addPlayersFromTournament(tournament['e'], tournament['y'] )
        chrono.tick()
        if chrono.i % 10 == 0:
            chrono.printRemaining()
            debug("Found: " + str(len(players.codes)) )
    players.saveCodes( player_codes )
else:
    debug("Loading all players in all the " + lengthTour + " tournaments.")
    players.loadCodes(player_codes)
debug("Done. " + clock.strClock())

numberOfPlayers =  str( len( players.codes ) )
debug("Found: " + numberOfPlayers + " players" )



if True:
    debug("Fetching informations for all " + numberOfPlayers + " players")
    players.fetchInfoPlayers()
    players.savePlayers( player_save )
else:
    debug("Loading informations for all " + numberOfPlayers + " players")
    players.loadPlayers(player_save)
debug("Done. " + clock.strClock())


if True:
    debug("Fetching informations for all matches...")
    tournaments.fetchAllMatches('BDD/matches.csv', players.dic)
else:
    pass
debug("Done. " + clock.strClock())











if False:
    tournament = getTournamentInfos("339", "2010")
    printObject( tournament )


if False:
    matchInfos = getMatchInfos('0339', '2010', '3', 'R485')
    printObject( matchInfos )


if False:
    matches = getMatchesOfTournament("339", "2010")
    printObject( matches )


if False:
    saveMatchesOfYear("BDD/bdd.csv", "2", "2014", 20, True)
#    mainCSV("bdd.csv", [ ["339", "2010"] ] )




if False:
    tournament = getTournamentInfos("339", "2010")
    printObject( tournament )


if False:
    matchInfos = getMatchInfos('0339', '2010', '3', 'R485')
    printObject( matchInfos )


if False:
    matches = getMatchesOfTournament("339", "2010")
    printObject( matches )


if False:
    saveMatchesOfYear("BDD/bdd.csv", "2", "2014", 20, True)
#    mainCSV("bdd.csv", [ ["339", "2010"] ] )



