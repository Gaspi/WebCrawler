# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 10:50:14 2014

@author: Gaspard
"""






class ATPRank:
    
    def __init__(self, playerPath=''):
        self.dic = dict()
        self.ID  = 0
        self.playersPath = playerPath
        self.i = 0
        self.savePeriod = 20
    
    def isTreated(self, code):
        for t in self.dic:
            if self.dic[t]['Code'] == code:
                return True
        return False

    def addInfoPlayer(self, code):
        if not self.isTreated(code):
            url = urlOpen( url_players + code + '.aspx' )
            dom = BeautifulSoup(url)
            aux = infoFromDOM(dom)
            playerURL = playersFromURL(url)
            aux.update( {
                "ID"        : self.ID,
                "Code"      : code,
                "IDPlayer"  : playerURL  } )
            self.dic[playerURL] = aux
            self.ID += 1
            self.saveMaybe()
    
    def save(self):
        with open(self.playersPath, 'wb') as csvfile:
            w = getWriter(csvfile, players_fields)
            w.writerows( sorted(self.dic.values(), key=lambda k: k['ID']) )
    def load(self):
        with open(self.playersPath, 'rb') as csvfile:
            self.dic = dict()
            self.ID = 0
            for p in getReader( csvfile ):
                p['ID'] = int( p['ID'] )
                if p['ID'] >= self.ID:
                    self.ID = p['ID'] + 1
                self.dic[ p['IDPlayer'] ] = p
    
    
    def saveMaybe(self):
        self.i += 1
        if self.i % self.savePeriod == 0:
            debug("Saving")
            self.save()
    
    def canLoad(self):
        return os.path.isfile(self.playersPath)