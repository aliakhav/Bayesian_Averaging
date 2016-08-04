# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 17:00:17 2016

@author: aliakhav
"""

import os

def run_samples(i):
    path='LHS'+str(i)
    os.chdir(path)    
    os.system('sbatch exec_script')
    os.chdir('..')
    return

num_sample=256

for i in range(0,num_sample):
	run_samples(i)
