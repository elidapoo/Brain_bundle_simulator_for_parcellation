'''
Cristobal  @ 05-02-2022 18:05 / BrainVISA VM
'''

import numpy as np
import os
from soma import aims, aimsalgo
import random
import time


path_labels='/home/elida/Downloads/GeoSP-master/output_atlas/Llabels.txt'

final_path= path_labels
with open(path_labels, 'r') as archivo:
      contenido = archivo.readlines()
numeros_enteros = []
for linea in contenido:
    numero = int(linea.strip())
    numeros_enteros.append(numero)
    
    

    
    
    
path_mesh = '/home/elida/Downloads/GeoSP-master/input_data/lh_tal.obj'

mesh = aims.read(path_mesh)
vert = np.array(mesh.vertex())
parcelation = numeros_enteros


if 'Llabels' in os.path.basename(path_labels):
      output_file =final_path+'Lparcelation.gii'
elif 'Rlabels' in os.path.basename(path_labels):
      output_file = final_path+'Rparcelation.gii'


print(len(parcelation))
path_parce='/home/elida/Downloads/label/lh.r.aparc.annot.gii'
parce = np.array(aims.read(path_parce))

print(len(parce[0]))


c=0
new_parcelation = np.full_like(parce[0], -1, dtype=int)  # Llena el array con -1

# Asignar valores a new_parcelation
c = 0
for i, valor in enumerate(parce[0]):
    if valor != -1:
        new_parcelation[i] = parcelation[i]
    c += 1

print(np.min(parce))
print(np.max(parce))
print(c)


ws = aims.Writer()
texOut = aims.TimeTexture_FLOAT(1,len(vert))
for j in range(0,len(vert)):
 	texOut[0][j] = new_parcelation[j]
ws.write(texOut,output_file)
