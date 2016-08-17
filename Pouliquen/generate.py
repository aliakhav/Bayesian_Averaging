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
    min1: minimum of phi1,
    range1: range of data for phi1,       
    min2: minimum of D_phi,
    range2:range of data for D_phi   
""" 
def LHS_TITAN(num_sample,min1,range1,min2,range2):  
   
    #number of random dimension
    randoms=2
    
    lhd = pylhs.lhs(randoms, num_sample)
    lhs=np.zeros((num_sample,randoms))
    lhs[:,0]=lhd[:,0]*range1+min1
    lhs[:,1]=lhd[:,1]*range2+min2
    
    fp = open(os.path.join(os.getcwd(),'titan/input_Pouliquen.py'),'r')
    simdata = fp.read()
    fp.close
    
    fpp = open(os.path.join(os.getcwd(),'titan/exec_script'),'r')
    simdatap = fpp.read()
    fpp.close
    
    
    phi1=1111
    phi3=2222
    phi2=3333
    
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
        rep_phi1="{:.3f}".format(lhs[i,0])
        rp_simdata = simdata.replace(str(phi1),rep_phi1)
        rep_phi3="{:.3f}".format(lhs[i,0]+1.0)
        rp_simdata = rp_simdata.replace(str(phi3),rep_phi3)
        rep_phi2="{:.3f}".format(lhs[i,1]+lhs[i,0])
        rp_simdata = rp_simdata.replace(str(phi2),rep_phi2)      
        fp = open(os.path.join(os.getcwd(),dircs_name+str(i)+'/input_Pouliquen.py'),'w')
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

    #writing the LHS design points to a .csv     
    np.savetxt('Design_Points.csv', lhs, delimiter=',')

LHS_TITAN(256,11.0,22.0,9.0,5.0)
