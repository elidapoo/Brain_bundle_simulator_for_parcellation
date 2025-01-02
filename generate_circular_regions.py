# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:28:03 2022

@author: Elida
"""
import numpy as np
import math
from math import cos,sin
import random as rn
from scipy.interpolate import splprep, splev

#%%
def calculate_tangent(points, index):
    if index == 0:
        tangent = points[1] - points[0]
    elif index == len(points) - 1:
        tangent = points[-1] - points[-2]
    else:
        tangent = points[index + 1] - points[index - 1]
    return tangent / np.linalg.norm(tangent)

def generate_circle_points(center, normal, radius, num_points):
    # Crear un array de ángulos uniformemente distribuidos
    theta = np.random.uniform(0, 2 * np.pi, num_points)
    # Crear un array de radios distribuidos uniformemente
    radii = np.sqrt(np.random.uniform(0, 1, num_points)) * radius
    
    # Crear vectores ortogonales al normal
    if np.all(normal == [0, 0, 1]):
        v1 = np.array([1, 0, 0])
    else:
        v1 = np.cross(normal, [0, 0, 1])
    v1 = v1 / np.linalg.norm(v1)
    v2 = np.cross(normal, v1)
    
    # Generar los puntos dentro del círculo
    circle_points = [center + r * (v1 * np.cos(t) + v2 * np.sin(t)) for r, t in zip(radii, theta)]
    return np.array(circle_points)


#%%Generate the intermediate and the central circles.
def allpoints_generator(radio_list, centroide, point_list,r1_points,r1_center,r2_points):
    d_list = []

    idx=[3,10,17]
    for i in range(len(point_list)):
        p1 = point_list[i]
        
   
        center = p1
        tangent = calculate_tangent(centroide, idx[i])    
        circle_points = generate_circle_points(center, tangent, radio_list[i],len(r2_points))
        d = [np.array(i, dtype=np.float32) for i in circle_points]
       
        d_list.append(d)

    return  d_list

