# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 10:03:34 2023

@author: Elida
"""

import numpy as np
import random as rn
import math
from geomdl import fitting
import generate_circular_regions as gtm


#%%Generate  splines with 21 points
def Approximate_funtion(points, degree):
    
    degree =degree# cubic curve
    
    
    # Do global curve approximation
    curve = fitting.interpolate_curve(points, degree,ctrlpts_size=5)
    
 
    curve.delta = 0.048

    curve_points = curve.evalpts
    return curve_points


#%%

# Función de emparejamiento de puntos
def match_points(point_sets):
    matched_points = []
    used_indices = {i: [] for i in range(len(point_sets))}
    
    # Selección del primer punto en el primer conjunto
    for i in range(len(point_sets[0])):
        current_points = []
        
        # Añade el punto actual al conjunto de emparejados
        current_point = point_sets[0][i]
        current_points.append(current_point)

        # Emparejamiento con los otros conjuntos
        for j in range(1, len(point_sets)):
            min_dist = float('inf')
            selected_point = None
            selected_index = None

            # Encuentra el punto más cercano en el siguiente conjunto
            for k, point in enumerate(point_sets[j]):
                if k not in used_indices[j]:
                    dist = np.linalg.norm(current_point - point)
                    if dist < min_dist:
                        min_dist = dist
                        selected_point = point
                        selected_index = k
            
            # Añadir el punto emparejado a la lista de puntos actuales
            current_points.append(selected_point)
            used_indices[j].append(selected_index)
        
        # Añadir el conjunto de puntos emparejados a la lista global
        matched_points.append(current_points)

    # Convertir la lista de listas en un array numpy
    matched_points = np.array(matched_points)
    
    return matched_points

#%%
def splines_simulator(fiber_points,radio_list,centroide,numb_fib_total,r1_points, r1_center,r2_points, r2_center,flag):
    point_list=centroide[fiber_points] #centroide[[0,5,10,15,20]]

    d_list=gtm.allpoints_generator(radio_list,centroide, point_list,r1_points,r1_center,r2_points)  ### 8 puntos de los puntos [3,10,17]              
   

    d_list.insert(0, [r1_points[i] for i in range(r1_points.shape[0])])
    

    d_list.append([r2_points[i] for i in range(r2_points.shape[0])])
    
  
    new_d_list=d_list.copy()
    sig_points=[0,3,10,17,20]
    
    point_list=list(point_list)
    point_list.insert(0,r1_center)
    point_list.append(r2_center)
    new_d_list=[np.array(i) for i in new_d_list]
  
    matched_points=match_points(new_d_list)
    spline_all=[]
    
    for mp in matched_points:
        mp=list(mp)
        
        if flag==True:
            spline= Approximate_funtion(mp,2) #fibras cortas
        else:
    
            spline= Approximate_funtion(mp,4)  #fibras largas
    
        spline_all.append(np.array(spline).astype('float32'))
        
    return spline_all,d_list,new_d_list

