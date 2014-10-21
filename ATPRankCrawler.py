# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 10:50:14 2014

@author: Gaspard
"""

from playerCrawler import *



def intFromRank(r):
    if r[-1] == 'T':
        r = r[:-1]
    r = "".join(r.split(","))
    r = "".join(r.split("."))
    return int(r)

class ATPRank:
    
    def __init__(self, rankPath=''):
        self.rankPath = rankPath
    
    def addATPRank(self, dico):
        code = dico['IDPlayer']
        ID   = dico['ID']
        path = self.getPath(ID)
        if self.isTreated(path):
            return False
        else:
            url = urlOpen( url_players + code + '.aspx?t=rh' )
            dom = BeautifulSoup(url)
            trList = dom.find('table').find_all('tr')
            with open(path+'2', 'wb') as f:
                w = csv.DictWriter(f, [ 'Date', 'Rank' ] )
                for tr in trList[1:]:
                    tab = tr.find_all('td')
                    if len( tab[1].contents ) > 0:
                        w.writerow( {'Date' : tab[0].contents[0] ,
                                     'Rank' : intFromRank( tab[1].contents[0] ) }  )
            os.rename( path+"2", path )
            return True
    
    
    
    def getPath(self, ID):
        return self.rankPath + "p" + str(ID) + "p.csv"
    
    def isTreated(self, path):
        return os.path.isfile(path+".csv")
    
    


