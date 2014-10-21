# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 12:12:12 2014

@author: Gaspard
"""









player = L3[i]
    lien = urllib.urlopen("http://en.wikipedia.org/w/index.php?title="+player+"&action=edit")
    html = lien.read()
    y = re.findall("\#rEDIRECT \[\[(.*)\]\]", html)
    
    
    
    
    Data = pd.read_csv('players.csv')
Data


def name(ch):
    y =  ch[ch.rfind('/')+1:]
    return y.replace("-","_")

for i in xrange(len(Data['ID|Code|IDPlayer'])):
    Data['ID|Code|IDPlayer'][i] = name(Data['ID|Code|IDPlayer'][i])