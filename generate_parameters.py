# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:28:16 2023

@author: Elida
"""


import numpy as np
import random as rn
import generate_splines as sp
import os
from scipy.interpolate import interp1d
from dipy.tracking.streamline import length
import random as rn


#%%Generate a 3x3 random vector

def getRandomVect(mu, sigma):
         vect = np.zeros([3], dtype = 'float32')
         vect[0] = rn.gauss(mu, sigma)
         vect[1] = rn.gauss(mu, sigma)
         vect[2] = rn.gauss(mu, sigma)
         
         return vect
def generate_radio_list(r1_points, r1_center,r2_points, r2_center):
  
    radio1_list=[]
    radio2_list=[]
    for i in range(len(r1_points)):
        radio1 = np.linalg.norm(r1_points[i] - r1_center) 
        radio2 = np.linalg.norm(r2_points[i] - r2_center) 
        radio1_list.append(radio1)
        radio2_list.append(radio2)

    r2=int(np.mean(radio1_list))
    r4=int(np.mean(radio2_list))
      
    if r2 < r4:
        r3_range=[r2,r4]
    else:
        r3_range=[r4,r2]
        
    
    r3 = rn.randint(*r3_range)
    
    while r3 > r2 or r3 >r4:
        r3 = rn.randint(*r3_range)

   
    return [ r2, r3, r4]
def interpolate_fun(original_points,points):
            
    aux = np.linspace(0, 1, len(original_points))
    aux_interpolated = np.linspace(0, 1,points)
    
    
    
    interp_func = interp1d(aux, original_points, axis=0, kind='linear')
    points_interpolated = interp_func(aux_interpolated)
    points_interpolated =np.array([ i.astype(np.float32) for i in points_interpolated ])
    
    return points_interpolated
    


def generate_fiber_parameters(centroids, r1_points,r2_points, numb_fib_total_range):
    simulated_tractography = []
    par_list = []
    idx=1
    
    distance_list=[]
    for i in range(len(centroids)):
        kk=length(centroids[i][0])
        distance_list.append(kk)


    for i in range(len(centroids)):
        
        centroide=centroids[i][0]
        max_vert= max(len(r1_points[i]), len(r2_points[i]))
        
     
        while True:
            numb_fib_total = rn.randint(*numb_fib_total_range)
  
            if numb_fib_total  >= max_vert:
                break

        points_interpolated_r1=interpolate_fun(r1_points[i],numb_fib_total)
        points_interpolated_r2=interpolate_fun(r2_points[i],numb_fib_total)
        
        r1_center = np.mean(points_interpolated_r1,axis=0)
        r2_center = np.mean(points_interpolated_r2,axis=0)

        radio_list = generate_radio_list(points_interpolated_r1, r1_center, points_interpolated_r2, r2_center)
        par_list.append((numb_fib_total, radio_list))

        fiber_points = [ 3, 10,17]
        if distance_list[i]<=50:
            flag=True
        else:
            flag=False
        spline_all, d_list,new_d_list= sp.splines_simulator(fiber_points, radio_list, centroide, numb_fib_total,points_interpolated_r1, centroide[0],points_interpolated_r2, centroide[20],flag)
       
    

        simulated_tractography.append(spline_all)
      
        print('Completed simulated bundle', idx)
        idx+=1

    return simulated_tractography, par_list,d_list,new_d_list

def generate_noise(simulated_tractography,mu,sigma_range):
   sigma_list = np.linspace(sigma_range[0], sigma_range[1], len(simulated_tractography))
   numb_point=5
   simulated_tractography_random2=[]
   c=0
   for d in simulated_tractography:  
       aplastada=[]
       sigma=sigma_list[c]
       c+=1
       for d1 in d: 
            vect=getRandomVect(mu, sigma)
         
            random_numbers=np.linspace(-1, 0,5)
         
            resultado = np.array([i * vect for i in random_numbers])
            d1_copy = d1.copy()
            d1_copy[0:numb_point] += resultado
            d1_copy = d1_copy[::-1]
            d1_copy[0:numb_point] += resultado
            d1_copy = d1_copy[::-1]
            
            aplastada.append(d1_copy)
    
                    
    
       simulated_tractography_random2.append(aplastada)
   return simulated_tractography_random2  


def generate_labels(simulated_tractography):
    n = 0
    index_sim_tractography = []

    for i in simulated_tractography:
        index_list = np.arange(n, n + len(i))
        n = index_list[-1] + 1
        index_sim_tractography.append(index_list)
        
        


    with open('Results/labels.txt', 'w') as f:
        for index_list in index_sim_tractography:
            f.write(' '.join(map(str, index_list)) + '\n')



