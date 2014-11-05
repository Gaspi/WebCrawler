# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 09:16:48 2014
@authors: Gaspard, Thomas
"""

import re, unicodedata

from utils import *
from seasonCrawler import *
from FileSystem import *


urlTE = "http://www.tennisexplorer.com/results/?type=atp-single&year={2}&month={1}&day={0}"
urlTE = "http://www.tennisexplorer.com/matches/"


infoReader = InfoReader('localnewpath.txt')

fs = FileSystem(infoReader)  # reads 4 lines
Year                = infoReader.readInt()
Month               = infoReader.readInt()
Day                 = infoReader.readInt()
sleepingTime        = infoReader.readInt()
CleaningMatches     = infoReader.readBool()
AddRankings         = infoReader.readBool()
debugMode           = infoReader.readBool()
refreshTime         = infoReader.readInt()


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






class RecentMatches:

    def __init__(self):
        debug('Initializing...')
        self.all_matches = []
        self.all_tournaments = []
        self.timeNow = time.strptime( ".".join([str(e) for e in getNotNoneTime()]) ,"%d.%m.%Y")
        self.allTourn = getAllTournaments( self.timeNow )
        self.players = PlayerRecognizer( fs.cleanPlayerPath )
        self.allowNoLink     = False
        self.filterFutures   = True
        self.filterChallenger= False
        self.id_tour = -1
        debug('Done.')
        
    
    def cleanRecentMatches(self):
        debug('Cleaning matches...')
        chrono = Chrono()
        chrono.start(len(self.all_matches))
        for m in self.all_matches:
            closestName, _, _ = closest( m[-2], self.allTourn.keys() )
            t = self.allTourn[closestName]
            m.append(closestName)
            m.append( str(t['TournamentCategory']) )
            m.append( str(t['Indoor']) )
            m.append(     t['StartDate'] )
            m.append( str(t['TournamentType']) )
            name0 = m[0]
            name1 = m[1]
            m[0] = self.players.recognize(name0)
            m[1] = self.players.recognize(name1)
            m.append( name0 )
            m.append( name1 )
            chrono.tick()
            if chrono.needPrint(): chrono.printRemaining()
        self.matches      = self.all_matches
        self.unrecognized = sorted( [e for e in self.players.recognitions if e[6] == "True" ] , key=lambda k:k[2])
        self.recognized   = sorted( [e for e in self.players.recognitions if e[6] == "False" ], key=lambda k:k[2])
        self.others       = sorted( [e for e in self.players.recognitions if e[6] not in[ "True","False"] ] , key=lambda k:k[2])
#        if self.unrecognized:
#            raise self
#        if self.others:
#            raise self
    
    
    
    def parseTennisExplorer(self, day=None, month=None, year=None):
        (day, month, year) = getNotNoneTime(day, month, year)
        dom = getDOM( urlTE.format(day,month, year) )
        lines = dom.find('table','result').find('tbody').find_all('tr')
        
        current_tour = []
        infos = None
        for day in dom.find_all('div','tbl'):
            date  = day.find('ul','tabs').find('span').contents[0].split(". ")
            lines = day.find_all('tr')
            infos = None
            filtering = False
            current_tour = []
            debug("Fetching matches for " + ".".join(date) )
            chrono = Chrono()
            chrono.start(len(lines))
            for l in lines:
                cl = l.attrs['class'][-1]
                name = l.find('td', 't-name').contents[0]
                
                if cl == 'flags':
                    tour_name = name.contents[-1]
                    if self.filterFutures and re.findall('futures', tour_name.lower()):
                        filtering = True
                        print "Starting filtering (Futures): " + tour_name
                    elif self.filterChallenger and re.findall('challenger', tour_name.lower()):
                        filtering = True
                        print "Starting filtering (Challenger): " + tour_name
                    else:
                        print tour_name
                        filtering = False
                    if 'href' in name.attrs:
                        url = "http://www.tennisexplorer.com" + name.attrs['href']
                        domtour = getDOM(url)
                        center = domtour.find('div', {'id':'center'})
                        full_name = center.find('h1').contents[0]
                        country = re.findall( '\((.*)\)', full_name)
                        country = country[0] if country else ''
                        nature = re.findall('\((.*), (.*), (.*)\)', center.find('div').contents[0])[0]
                        cn = convertNature(nature)
                        self.id_tour += 1
                        current_tour = [ tour_name, full_name, cn, 'T' ]
                        prize = int( "".join( [e[1] for e in re.findall('([^0-9]*)([0-9]*)',cn[0]) ]) )
                        current_tour = {'IDTournament'       : self.id_tour,
                                        'Tournament'         : tour_name,
                                        'full_name'          : full_name,
                                        'has_link'           : True,
                                        'Indoor'             : int(cn[1] == 'Indoor'),
                                        'TournamentType'     : 1,   # Field du site [1,2,4]
                                        'TournamentCategory' : 0,   # Field de Sylvain
                                        'Surface'            : cn[2],
                                        'Country'            : country,
                                        'TournamentPrize'    : prize,
                                        'TournamentCurrency' : 'D',
                                        'TournamentPrizeUSD' : prize,
                                        'Draw'               : 0,
                                        'TournamentStart'    : '',
                                        'TournamentEnd'      : '',
                                        'e':0, 'y':0 }
                        self.all_tournaments.append(current_tour)
                    else:
                        filtering = True
                        current_tour = [ tour_name, tour_name + " [NoLink]", convertNature(['$???','','']), 'F' ]
                elif not filtering:
                    if cl == 'bott':
                        rowspan = l.find_all('td', {'rowspan':"2"})
                        t = rowspan[-1].find('a').attrs
                        if 'href' in t:
                            url = "http://www.tennisexplorer.com" + t['href']
                        else:
                            raise Exception("A match has not link !")
                        fullName = followLinkPlayer( name)
    #                   fullName = name.contents[0]
                        infos = [ rowspan[0].contents[0], fullName, url]
                    elif infos:
    #                   fullName = name.contents[0]
                        fullName = followLinkPlayer( name )
                        if self.allowNoLink or current_tour['has_link']:
                            self.all_matches.append( [ infos[1], fullName,
                                                      current_tour['TournamentPrize'],
                                                      current_tour['Indoor'],
                                                      current_tour['Surface']
                                                    ] + date +
                                                [infos[0],
                                                 current_tour['Tournament'],
                                                 current_tour['full_name'],
                                                 current_tour['has_link'] ]  )
                        infos = None
                    else:
                        print date
                        print l
                chrono.tick()
                if chrono.needPrint(): chrono.printRemaining()



    def saveTournaments(self):
        with open(fs.cleanTournamentsPath, "wb") as f:
            w = getWriter(f, tournaments_infos_fields_clean)
            for t in self.all_tournaments:
                del t['has_link'], t['full_name']
                w.writerow( t )
                
    def saveMatchesAux(self, filePath):
        with open(fs.cleanMatchesPath + "id", "wb") as f:
            w = getWriter(f, match_field_names_clean + new_match_fields)
            w.writerows( self.all_matches )
    
    def saveMatches(self):
        with open(fs.cleanMatchesPath + "id", "wb") as f:
            w = csv.writer(f, delimiter='|')
            w.writerows( self.all_matches )


# temporary debug function
def main():
    global rm
    rm = RecentMatches()
    rm.parseTennisExplorer()
    rm.cleanRecentMatches()
    rm.saveTournaments()
    rm.saveMatches()




def convertNature(nature):
    if nature[1] == "indoors":
        return (nature[0], "Indoor", "Hard")
    elif nature[1] == "clay":
        return (nature[0], "Outdoor", "Clay")
    elif nature[1] == "hard":
        return (nature[0], "Outdoor", "Hard")
    elif nature[1] == "clay":
        return (nature[0], "Outdoor", "Grass")
    else:
#        debug(nature)
        return (nature[0], "-1", "-1")



class PlayerRecognizer:
    def __init__(self, path):
        self.players = {}
        self.recognitions = []
        with open(path) as f:
            for line in f.readlines()[1:]:
                els = line.strip('\n').split("|")
                player = " ".join([ els[3], els[11], els[4] + els[5] + els[6] ])
                self.players[ cleanLine(player) ] = els[0]
    def recognize(self,name):
        (closestName, score, delta) = closest(name, self.players.keys() )
        aux = name.split()
        caux = closestName.split()
        refuse = score < 7
        self.recognitions.append( (" ".join(aux[:-1]), " ".join(caux[:-1]), score, score * len(name), aux[-1] == caux[-1], delta, str(refuse)) )
        if refuse:
            return -1
        else:
            return self.players[closestName]
    

def getAllPlayersFromDB(path):
    players = {}
    with open(path) as f:
        for line in f.readlines()[1:]:
            els = line.strip('\n').split("|")
            player = els[3] + " " + els[11]
            players[ player ] = els[0]
    return players



def cleanCountry(name):
    if   name == 'USA'   : return 'United States'
    elif name == 'Russia': return 'Russian Federation'
    elif name == 'RSA'   : return 'South Africa'
    else                 : return name


def getAllTournaments(t):
    ATPtourn1 = getAllTournamentsFromTY(1, t.tm_year)
    ATPtourn2 = getAllTournamentsFromTY(2, t.tm_year)
    ATPtourn4 = getAllTournamentsFromTY(4, t.tm_year)
    alltour=[ e for e in ATPtourn1 if 0 <= deltaDays(t, time.strptime(e['StartDate'],"%d.%m.%Y")) < 20 ] + \
            [ e for e in ATPtourn2 if 0 <= deltaDays(t, time.strptime(e['StartDate'],"%d.%m.%Y")) < 20 ] + \
            [ e for e in ATPtourn4 if 0 <= deltaDays(t, time.strptime(e['StartDate'],"%d.%m.%Y")) < 20 ]
    res = dict()
    for t in alltour:
        res[ t['Name'] ] = t
    return res



def followLinkPlayer(name):
    if 'href' in name.attrs:
        url = "http://www.tennisexplorer.com" + name.attrs['href']
        domplayer = getDOM(url)
        fullname = domplayer.find('table', 'plDetail').find('h3').contents[0]
        country = ''
        birth = ''
        for d in domplayer.find_all('div', 'date'):
            c = d.contents[0].split(': ')
            if c[0] == 'Country':
                country = cleanCountry(c[1])
            elif c[0] == 'Born':
                birth = ''.join(c[1].split('. '))
        return  fullname + ' ' + country + ' ' + birth
    else:
        raise Exception("A player has not link !")





# --------------------------------------------------------------
#                 Finding closest string
# --------------------------------------------------------------
err = None
def cleanLine(line):
    try:
        return unicodedata.normalize('NFKD', unicode(line.decode('UTF-8'))).encode('UTF-8', 'ignore').lower()
    except:
        global err
        err = [line, cleanLine]
        raise Exception( "err=" + str(err) )
        

def getWordsLower(line):
    return [ e[1] for e in re.findall('([^a-z0-9]*)([a-z0-9]*)([^a-z0-9]*)', cleanLine(line)) if len(e[1]) > 0 ]

def levenshtein(s1, s2):
    if len(s1) < len(s2): return levenshtein(s2, s1)
    if len(s2) == 0:      return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def similarityLeven(line1, line2):
    l1 = getWordsLower(line1)
    l2 = getWordsLower(line2)
    res = 0
    for w1 in l1:
        mini = inf
        for w2 in l2:
            leven = levenshtein(w1,w2)
            if leven < mini:
                mini = leven
        if w1.isdigit():
            res += 2 if w1 == w2 else 0 # 1 / (0.5 + mini)
        else:
            res += 1 / (0.4 + mini)
#        res += len(w1) / (0.5 + mini)
    return res

def closest(line, lines):
    res = None
    maxi = 0
    delta = 0
    for l in lines:
        leven = similarityLeven(line, l)
        if leven > maxi:
            delta = leven - maxi
            maxi = leven
            res = l
    return (res, maxi, delta)








#
#
#
#
#from tournamentCrawler      import *
#from matchCrawler           import *
#from bdd                    import *
#from playerCrawler          import *
#from tournamentInfoCrawler  import *
#from matchMerger            import *
#from ATPRankCrawler         import *
#from ATPRankings            import *
#from FileSystem             import *
#
#infoReader = InfoReader('localnewpath.txt')
#
#fs = FileSystem(infoReader)  # reads 4 lines
#Year                = infoReader.readInt()
#Month               = infoReader.readInt()
#Day                 = infoReader.readInt()
#sleepingTime        = infoReader.readInt()
#CleaningMatches     = infoReader.readBool()
#AddRankings         = infoReader.readBool()
#debugMode           = infoReader.readBool()
#refreshTime         = infoReader.readInt()
#
#print "Initialisation: Done."
#
#
#def mainBody():
#    
#    debug("Initialisation...")
#    clock       = Clock()
#    clock.clock()
#    
#    tournaments = Tournaments( fs )
#    players     = Players(     fs )
#    matchCrawler= Matches(     fs )
#    atpRankings = ATPRankings( fs )
#
#    chrono      = Chrono()
#    chrono.periodTime = refreshTime * 0.001
#    clock.done()
#    
#
##    debug("Loading all tournaments (types " + str(tournamentTypes) +
##              ") from " + str(yearStart) + " to " + str(yearEnd) + "...")
##    seasons.loadCodes()
##    
##    lengthTour = str( len(seasons.codes) )
##    clock.done()
##    debug("Found: " + lengthTour + " tournaments")
#    
#    
#    
#    debug("Loading...")
#    tournaments.load()
#    
#    clock.done()
#    numberPlayers = len(tournaments.playerCodes)
#    debug("Found: " + str(numberPlayers) + " players" )
#    
#    
#    debug("Loading players...")
#    players.load()
#    
#    matchCrawler.dicoPlayers = players.dic
#    clock.done()
#    
##    atpRankings.playersNb = players.ID
#    atpRankings.playersNb = numberPlayers
#    atpRankings.tournaments = tournaments.tournaments
#    atpRankings.loadPlayedTournaments()
#    
#    debug("Computing played tournaments...")
#    atpRankings.startFeedingMatches()
#    atpRankings.savePlayedTournaments()
#    clock.done()
#    
#    debug("Computing rankings...")
#    atpRankings.startComputingRanks()
#    clock.done()
#    
#    debug("Cleaning rankings...")
#    atpRankings.clean()
#    clock.done()
#    
#    return True
#
#
#clock = Clock()
#clock.clock()
#
#with open(fs.debugOut, 'a') as debugout:
#    setDebugFileOut(debugout)
#    if debugMode:
#        mainBody()
#    else:
#        keepOn = True
#        while keepOn:
#            keepOn = False
#            try :
#                mainBody()
#            except:
#                err = sys.exc_info()
#                printError("Error !!!  " + str( err[0] ) )
#                printError("Detail:   "  + str( err[1] ) )
#                printError("Network error expected.")
#                debug("Going to sleep for " + str(sleepingTime) + " seconds...")
#                time.sleep( sleepingTime )
#                debug("Waking up !")
#                keepOn = True
#    debug("C'est fini !!!")
#    debug("Duration: " + clock.strClock())
#    debugPrintTime("End time:")
#


