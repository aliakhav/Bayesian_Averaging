# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 19:39:11 2016

@author: aliakhav
"""

import numpy as np
import os
import shutil as st
import pyDOE as pylhs

"""  
    num_sample: number of samples
    min1: minimum of phi_int,
    range1: range of data for phi_int,       
    min2: minimum of phi_bed,
    range2:range of data for phi_bed   
""" 
def LHS_TITAN(num_sample,min1,range1,min2,range2):  
   
    #number of random dimension
    randoms=2
    
    lhd = pylhs.lhs(randoms, num_sample)
    lhs=np.zeros((num_sample,randoms))
    lhs[:,0]=lhd[:,0]*range1+min1
    lhs[:,1]=lhd[:,1]*range2+min2
    
    fp = open(os.path.join(os.getcwd(),'titan/input_Coulomb.py'),'r')
    simdata = fp.read()
    fp.close
    
    fpp = open(os.path.join(os.getcwd(),'titan/exec_script'),'r')
    simdatap = fpp.read()
    fpp.close
    
    
    internal=1111
    bed=2222    
    
    jubnumber=55555
    
    dircs_name='LHS'
    
    #delete the folders if they are already exist
    for i in range(0,num_sample): 
        dirname=os.path.join(os.getcwd(),dircs_name+str(i))
        if (os.path.isdir(dirname)):
            st.rmtree(os.path.join(os.getcwd(),dircs_name+str(i))) 
    
    #creates the folder for simulation
    for i in range(0,num_sample): 
        st.copytree('titan',os.path.join(os.getcwd(),dircs_name+str(i))) 
    
    #replace the sample value with initial value in the list of input    
    for i in range(0,num_sample):        
        print lhs[i,:]
        rep_internal="{:.2f}".format(lhs[i,0])
        rp_simdata = simdata.replace(str(internal),rep_internal)
        rep_bed="{:.2f}".format(lhs[i,1])
        rp_simdata = rp_simdata.replace(str(bed),rep_bed)
        fp = open(os.path.join(os.getcwd(),dircs_name+str(i)+'/input_Coulomb.py'),'w')
        fp.write(rp_simdata)
        fp.flush()
        fp.close
#        print i
    #modifying the job name in the slurm scripts for each sample    
    for i in range(0,num_sample):        
        rep_jubnumber="{:.0f}".format(i)
        rp_simdatap = simdatap.replace(str(jubnumber),rep_jubnumber)   
        fpp = open(os.path.join(os.getcwd(),dircs_name+str(i)+'/exec_script'),'w')
        fpp.write(rp_simdatap)
        fpp.flush()
        fpp.close      

LHS_TITAN(256,35.0,4.0,20.0,7.0)
