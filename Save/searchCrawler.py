# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:28:49 2014
@author: Gaspard, Thomas, Arnaud
"""

import urllib
import re
from tournamentCrawler import *
from bdd import *



def searchTournaments(t, y):
    url = 'http://www.atpworldtour.com/Scores/Archive-Event-Calendar.aspx?t='+str(t)+'&y='+str(y)
    content = urllib.urlopen(url).read()
    tournaments = re.findall('aspx\?e=([0-9]+)\&y\=([0-9]+)"\>', content)
    return tournaments


def searchAllTournaments(t, start=2014, end=2000):
    for i in range(start,end,-1):
        pass



def saveMatchesOfYear(filename, t, y, limit = 10, verbose=False):
    tournaments = searchTournaments(t,y)
    with open(filename, 'wb') as f:
        w = getMatchWriter(f)
        for t in tournaments[0:limit]:
            if verbose:
                debug( t[0] + " / " + t[1] )
            matches = getMatchesOfTournament( t[0], t[1] )
            writeTournament(w, matches)
    debug("Done.")




