# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 14:52:57 2023

@author: Elida
"""

import os
import visual_tools as vs
import BTools as bt
import numpy as np
import generate_parameters as gp
import time
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import pickle
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import interp1d
inicio = time.time()

def main(r1_points,r2_points,centroids):
    
    todasp = r1_points + r2_points

    longitudes = [len(arreglo) for arreglo in todasp]
    
  
    longitud_minima = min(longitudes)
    longitud_maxima = max(longitudes)
 
    mu = 0
    sigma_range = [1,1.5]  #
    numb_fib_total_range=[longitud_minima ,longitud_maxima +1]



    if not os.path.exists("Results"):
        os.makedirs("Results")

    if sigma_range == 0 or sigma_range == [0]:
        simulated_tractography_disperse, par_list, d_list, new_d_list = gp.generate_fiber_parameters(centroids, r1_points,  r2_points , numb_fib_total_range)
        gp.generate_labels(simulated_tractography_disperse)
        with open('Results/parametros.txt', 'w') as f:
            f.write('radios: ' + ', '.join(map(str, par_list)))
        return simulated_tractography_disperse
    else:
        simulated_tractography, par_list, d_list, new_d_list = gp.generate_fiber_parameters(centroids,r1_points,  r2_points ,  numb_fib_total_range)
        with open('Results/parametros.txt', 'w') as f:
            f.write('radios: ' + ', '.join(map(str, par_list)))
        simulated_tractography_disperse = gp.generate_noise(simulated_tractography, mu, sigma_range)
        gp.generate_labels(simulated_tractography_disperse)
        
        return simulated_tractography_disperse



if __name__ == "__main__":

        with open('Example/p1_list.pickle' , "rb") as file:
          r1_points=pickle.load(file)
          
        with open('Example/p2_list.pickle' ,'rb') as f:
            r2_points= pickle.load(f)
            
        centroids, _ = bt.read_bundle_severalbundles('Example/centroids.bundles')     
        simulated_tractography = main(r1_points, r2_points,centroids)
        bt.write_bundle_severalbundles('Results/simulated_data.bundles',   simulated_tractography)
    
    
            
    


    
