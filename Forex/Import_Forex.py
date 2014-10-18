# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 14:30:14 2014

@author: thomasbraun
"""

import numpy as np
from datetime import date


data = np.genfromtxt("Forex_2000_2014_FINAL enhanced_for_PYTHON_2.txt",delimiter=",")

def forex(Y,M,D):
    ref=str(Y)+str(date(Y, M, D).isocalendar()[1])
    print ref
    for i in range(data.shape[0]):
            if int(data[i,0])==int(ref):
                return data[i,1] 
    

if __name__ == "__main__":
    print forex(2005, 5, 25)