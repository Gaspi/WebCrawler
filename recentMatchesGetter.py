import urllib
import re
from urllib2 import Request, urlopen, URLError, HTTPError

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
for i in xrange(len(compet)):
    lien = urllib.urlopen("http://www.tennisexplorer.com/"+compet[i].lower().replace(' ','-')+"/")
    html = lien.read()
    expression = "\<div class\=\"box boxBasic lGray\"\>\((.*), (.*), (.*)\<\/div\>\<div class\=\"box boxBasic lGray\"\>"
    y = re.findall(expression, html)
    if len(y)>0 :
        nature.append(y[0])
    else: 
        nature.append(('$0','',''))

info = []
for i in xrange(len(nature)):
    if nature[i][1] == "indoors":
        info.append((nature[i][0], "Indoor", "Hard"))
    elif nature[i][1] == "clay":
        info.append((nature[i][0], "Outdoor", "Clay"))
    elif nature[i][1] == "hard":
        info.append((nature[i][0], "Outdoor", "Hard"))
    elif nature[i][1] == "clay":
        info.append((nature[i][0], "Outdoor", "Grass"))
    else: 
        info.append((nature[i][0], "-1", "-1"))

info.append("END")

matches = []
i_comp = -1
for i in xrange(len(joueur)/2):
    if (idi[2*i] == debut[i_comp+1]):
        i_comp += 1
    matches.append([compet[i_comp], info[i_comp][0], info[i_comp][1], info[i_comp][2], date, heure[i], joueur[2*i], joueur[2*i+1]])

players = {}
f = open("data/players.csv")
lines = f.readlines()
for line in lines[1:]:
    els = line.split("|")
    i = els[0]
    player = els[3]
    players[player.split()[0][0]+". "+" ".join(player.split()[1:]).lower()] = i

for match in matches:
    player1 = match[6].split()[-1]+" "+" ".join(match[6].split()[:-1]).lower()
    player2 = match[7].split()[-1]+" "+" ".join(match[7].split()[:-1]).lower()
    if player1 in players and player2 in players:
        print("|".join([match[0], players[player1], players[player2], match[1], match[2], match[3], match[4], match[5]]))

