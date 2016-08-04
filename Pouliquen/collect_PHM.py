# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 18:46:23 2016

@author: aliakhav
"""

import os

def run_samples(i):
    path='LHS'+str(i)
    os.chdir(path)    
    os.system('cp pileheightrecord.-00001 ../Distance_Calc')
    os.chdir('../Distance_Calc')
    os.system('mv pileheightrecord.-00001 pileheightrecord'+str(i))
    os.chdir('..')    
    return

num_sample=256

for i in range(0,num_sample):
	run_samples(i)
