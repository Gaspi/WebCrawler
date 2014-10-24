# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 12:12:12 2014

@author: Gaspard
"""




class Wikipedia:
    
    def __init__(self, fs):
        self.cleanPlayerPath = fs.cleanPlayerPath
        self.players = []
    
    def isTreated(self, dico):
        return 'Name' in dico
    
    
    def addNamePlayer(self, code):
        if self.isTreated(dico):
            return False
        else:
            # Fill here
            dico['Name'] = ''
            return True
    
    def save(self):
        with open(self.playersPath, 'wb') as csvfile:
            w = getWriter(csvfile, players_fields)
            w.writerows( sorted(self.dic.values(), key=lambda k: k['ID']) )
    def load(self):
        with open(self.playersPath, 'rb') as csvfile:
            for p in getReader( csvfile ):
                p['ID'] = int( p['ID'] )
                if p['ID'] >= self.ID:
                    self.ID = p['ID'] + 1
                self.dic[ p['IDPlayer'] ] = p
        
    
    def clean(self, cleanFunction=defaultPlayerCleanFunction):
        with open( self.cleanPlayerPath , 'wb') as f:
            w = getWriter(f, players_fields)
            with open( self.playersPath, 'rb' ) as f2:
                for e in csv.DictReader(f2, restval='?', delimiter='|'):
                    w.writerow( cleanFunction(e) )
    
    


#Code de Omar


    
    