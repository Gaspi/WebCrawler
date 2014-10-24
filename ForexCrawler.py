# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 14:28:49 2014
@author: Thomas, Gaspard
"""

from bs4 import BeautifulSoup
import urllib
from datetime import date

start_year='2000'
start_month='1'
end_year='2014'
end_month='10'

url_forex_start = 'http://www.oanda.com/currency/average?amount=1&start_month='+start_month+'&start_year='+start_year+'&end_month='+end_month+'&end_year='+end_year+'&base=USD&avg_type=Week&Submit=1&exchange='
url_forex_end   = '&interbank=0&format=CSV'

url_EUR = urllib.urlopen( url_forex_start + 'EUR' + url_forex_end ) # cas €/$
url_AUD = urllib.urlopen( url_forex_start + 'AUD' + url_forex_end ) # cas A$/$
url_GBP = urllib.urlopen( url_forex_start + 'GBP' + url_forex_end ) # cas £/$


dom     = {'EUR':BeautifulSoup(url_EUR),'AUD':BeautifulSoup(url_AUD), 'GBP':BeautifulSoup(url_GBP) }
tableau = {'EUR': dom['EUR'].find_all('pre')[1].contents[0] ,'AUD': dom['AUD'].find_all('pre')[1].contents[0]   ,'GBP': dom['GBP'].find_all('pre')[1].contents[0] }
aux     = {'EUR':tableau['EUR'].split('\n') ,'AUD': tableau['AUD'].split('\n') ,'GBP':tableau['GBP'].split('\n')}


calendar={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}



def codeOfDate(Y,M,D):
    return date(Y, M, D).isocalendar()[0] * 100 + date(Y, M, D).isocalendar()[1]



def createForexDico():
    res = dict()
    for i in range(0,len(aux['EUR'])):
        if len(aux['EUR'][i]) <> 0 and aux['EUR'][i][0] == 'W':        
            j_EUR=aux['EUR'][i].split(',')
            j_AUD=aux['AUD'][i].split(',')
            j_GBP=aux['GBP'][i].split(',')
            mean={'EUR':(float(j_EUR[2])+float(j_EUR[3]))/2,
                  'AUD':(float(j_AUD[2])+float(j_AUD[3]))/2,
                  'GBP':(float(j_GBP[2])+float(j_GBP[3]))/2,
                  'USD':1.0  }
            D = int(j_EUR[1][0:2])
            M = calendar[j_EUR[1][3:6]]
            Y = int(j_EUR[1][7:11])
            res[ codeOfDate(Y,M,D) ] = mean
    return res

forex_dico = createForexDico()

def forex(Y,M,D,currency): #currency is either 'EUR', 'AUD' or 'GBP' or 'USD'
    return forex_dico[ codeOfDate(Y,M,D) ][ convertToCurrency(currency) ]

def forexDate(date,currency):
    d = date.split('.')
    return forex( int(d[2]), int(d[1]), int(d[0]), convertToCurrency(currency) )
    

# conversion functions:
currencies = ['EUR', 'AUD', 'GBP', 'USD']
currencyLetter_Char = {
                '\xe2\x82\xac'  :'E',
                '$'             :'D',
                '\xc2\xa3'      :'P',
                '\xc3\x87'      :'E',
                '\xc3\xba'      :'P',
                'A$'            :'A'   }

currencyName_Letter = { 'E':'EUR' , 'D':'USD' , 'P':'GBP' , 'A':'AUD'}

def convertToCurrency(c):
    if c in currencies:
        return c
    elif c in currencyName_Letter:
        return convertToCurrency( currencyName_Letter[c] )
    elif c in currencyLetter_Char:
        return convertToCurrency( currencyLetter_Char[c] )
    else:
        raise Exception("Wrong currency symbol: " + str(c))






