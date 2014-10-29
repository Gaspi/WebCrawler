# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 09:16:48 2014
@authors: Gaspard, Thomas
"""

import urllib, re, unicodedata

from utils import *
from seasonCrawler import *


urlTE = "http://www.tennisexplorer.com/results/?type=atp-single&year={2}&month={1}&day={0}"




def getNotNoneTime(day=None, month=None, year=None):
    if not day:
        day = time.localtime().tm_mday
    if not month:
        month = time.localtime().tm_mon
    if not year:
        year = time.localtime().tm_year
    return (day, month, year)


def parseTennisExplorer( day=None, month=None, year=None):
    (day, month, year) = getNotNoneTime(day, month, year)
    dom = getDOM( urlTE.format(day,month, year) )
    lines = dom.find('table','result').find('tbody').find_all('tr')
    all_matches = []
    current_tour = []
    infos = None
    for day in dom.find_all('div','tbl'):
        date  = day.find('ul','tabs').find('span').contents[0].split(". ")
        lines = day.find_all('tr')
        infos = None
        current_tour = []
        for l in lines:
            cl = l.attrs['class'][-1]
            name = l.find('td', 't-name').contents[0]
            if cl == 'flags':
                tour_name = name.contents[-1]
                if 'href' in name.attrs:
                    url = "http://www.tennisexplorer.com" + name.attrs['href']
                    domtour = getDOM(url)
                    center = domtour.find('div', {'id':'center'})
                    full_name = center.find('h1').contents[0]
                    nature = re.findall('\((.*), (.*), (.*)\)', center.find('div').contents[0])[0]
                    convertNature(nature)
                    current_tour = [ tour_name, full_name, convertNature(nature) ]
                else:
                    current_tour = [tour_name, "???", convertNature(['$???','','']) ]
            elif cl == 'bott':
                rowspan = l.find_all('td', {'rowspan':"2"})
                t = rowspan[-1].find('a').attrs
                if 'href' in t:
                    url = "http://www.tennisexplorer.com" + t['href']
                else:
                    url = ""
                infos = [ rowspan[0].contents[0], name.contents[0], url]
            elif infos:
                all_matches.append( [current_tour[0], infos[1], name.contents[0]] +
                                    list(current_tour[2]) + date +
                                    [ current_tour[1], infos[0] ]  )
                infos = None
            else:
                print date
                print l
    return all_matches







def deltaDays(date1, date2):
    return (time.mktime( date1 ) - time.mktime( date2 )) / (3600 * 24)



def getRecentMatches(day=None, month=None, year=None):
    (day, month, year) = getNotNoneTime(day, month, year)
    timeNow = time.strptime( ".".join([day, month, year]) ,"%d.%m.%Y")
    
    tennisExpl = parseTennisExplorer(day, month, year)
    players = getAllPlayersFromDB("data/players.csv")
    ATPtourn1 = getAllTournamentsFromTY(1, year)
    ATPtourn2 = getAllTournamentsFromTY(2, year)
    ATPtourn4 = getAllTournamentsFromTY(3, year)
    allTourn = [ e for e in ATPtourn1 if 0 <= deltaDays(timeNow, time.strptime(c,"%d.%m.%Y")) < 20 ] + \
               [ e for e in ATPtourn2 if 0 <= deltaDays(timeNow, time.strptime(c,"%d.%m.%Y")) < 20 ] + \
               [ e for e in ATPtourn3 if 0 <= deltaDays(timeNow, time.strptime(c,"%d.%m.%Y")) < 20 ]
    return allTourn


def getRecentMatchesBis():

    lien = urllib.urlopen("http://www.tennisexplorer.com/matches/?type=atp-single")
    html = lien.read()
    
    expression = "\<tr id=\"(.*)\" class=.* onmouseover=\"md_over\(this\)\;\" onmouseout=\"md_out\(this\)\;\"\>"
    idi = re.findall(expression, html)
    #idi
    
    expression = "\<td class\=\"t\-name\"\>\<a href=\".*\"\>(.*)\<\/a\>.*\<\/td\>"
    joueur = re.findall(expression, html)
    #joueur
    
    expression = "\<td class\=\"t\-name\" colspan\=\"2\"\>.*\<\/span\>([^<]*).*\<\/td\>"
    compet = re.findall(expression, html)
    #compet
    
    expression = "\<li class\=\"set\".*\>[\s\t]*\<span class\=\"tab\"\>(.*)\<\/span\>[\s\t]*\<\/li\>"
    date = re.findall(expression, html)[0]
    
    expression ="\<td class\=\"first time\" rowspan\=\"2\"\>([^<]*).*"
    heure = re.findall(expression, html)
    #heure
    
    expression = "\<tr id=\"(.*)\" class=\"one fRow bott\" onmouseover=\"md_over\(this\)\;\" onmouseout=\"md_out\(this\)\;\"\>"
    debut = re.findall(expression, html)
    debut.append("END")
    
    nature = []
    print compet
    for i in xrange(len(compet)):
        lien = urllib.urlopen("http://www.tennisexplorer.com/"+compet[i].lower().replace(' ','-')+"/")
        html = lien.read()
        expression = "\<div class\=\"box boxBasic lGray\"\>\((.*), (.*), (.*)\<\/div\>\<div class\=\"box boxBasic lGray\"\>"
        y = re.findall(expression, html)
        print y
        if len(y)>0 :
            nature.append(y[0])
        else: 
            nature.append(('$0','',''))
        print nature
    
    info = [ convertNature(n) for n in nature ] + ["END"]
    
    matches = []
    i_comp = -1
    for i in xrange(len(joueur)/2):
        if (idi[2*i] == debut[i_comp+1]):
            i_comp += 1
        matches.append([compet[i_comp], info[i_comp][0], info[i_comp][1], info[i_comp][2], date, heure[i], joueur[2*i], joueur[2*i+1]])

    players = getAllPlayersFromDB("data/players.csv")
    
    res = []
    for match in matches:
        player1 = match[6].split()[-1]+" "+" ".join(match[6].split()[:-1]).lower().replace("-", " ")
        player2 = match[7].split()[-1]+" "+" ".join(match[7].split()[:-1]).lower().replace("-", " ")
        res.append( [player1, player2, match] )
        if player1 in players and player2 in players:
            print("|".join([match[0], players[player1], players[player2], match[1], match[2], match[3], match[4], match[5]]))
        else:
            print("|".join([match[0], player1, player2, match[1], match[2], match[3], match[4], match[5]]))
    return res




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
        print nature
        return (nature[0], "-1", "-1")


def printMatrix(matches):
    l = len(matches[0])
    lengths = [0] * l
    for m in matches:
        for i in range(l):
            if len(m[i]) > lengths[i]:
                lengths[i] = len(m[i])
    s = "%" + ("s  %".join( [str(e) for e in lengths])) + "s"
    for m in matches:
        print s % tuple(m)



def getAllPlayersFromDB(path):
    players = {}
    with open(path) as f:
        lines = f.readlines()
        for line in lines[1:]:
            els = line.split("|")
            i = els[0]
            player = els[3]
            players[player.split()[0][0] + ". " +
                    " ".join(player.split()[1:]).lower().replace("-", " ")] = i
    return players












# --------------------------------------------------------------
#                 Finding closest string
# --------------------------------------------------------------


def getWordsLower(line):
    cleanLine = unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').lower()
    return [ e[1] for e in re.findall('([^a-z]*)([a-z]*)([^a-z]*)', cleanLine) if len(e[1]) > 0 ]

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
        res += 1 / (0.5 + mini)
    return res

def closest(line, lines):
    res = None
    maxi = 0
    for l in lines:
        leven = similarityLeven(line, l)
        if leven > maxi:
            maxi = leven
            res = l
    return res





