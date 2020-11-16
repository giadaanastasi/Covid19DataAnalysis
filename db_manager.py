# handle database manager functions for the algorithm
# example for spain dataset


from scenario2_utility import *


from sklearn.cluster import KMeans 
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as d
import glob, os
import numpy as np
import random as random
from datetime import date
from scipy.spatial.distance import cdist
import operator


#casos num_db 0
#hospital num_db 1
#tests    num_db 2
num_databases = 3
num_features = [7, 4, 5]

def receive_centers(csv_path,centers, num_db):
    dm = []
    result = []
    if num_db == 0:
        csv = pd.read_csv(csv_path, sep=";", index_col=False)
    else:
        csv = pd.read_csv(csv_path, sep=";")
    csv.fillna(0, inplace=True)
    csv.to_csv(csv_path, sep=";", index = False)
    distance = lambda u, v: ((u-v)**2).sum()
    
    for i in range(0, len(csv)):
        dm=[]
        for elem in centers[:][:][:][:]:
            dm.append(distance(np.array(csv.iloc[i,:]),elem[num_db][:]))
        result.append(dm)

    return result

def execution_phase(vector_q, num_db, csv_path, centers):
    count_vector = []
    index_column = []
    for j in range(len(vector_q)):
        index = 0
        for i in range(len(centers)): 
            equal = 0
            for k in range(num_databases): 
                if np.array_equal(vector_q[j][k], centers[i][k]) == True: 
                    equal +=1
            if equal == len(centers[i]):
                index = i
        index_column.append(index)
    csv = pd.read_csv(csv_path, sep=";")
    csv['index_col'] = index_column
    csv.to_csv(csv_path, sep=";", index = False)

    vector_s = []
    sum_features = lambda u, v: u+v
    for i in range(len(centers)):
        elem_s = []
        count_elem = 0
        for j in range(len(csv)):
            if (csv.iloc[j][csv.columns == 'index_col']==i).bool():
                if len(elem_s)==0:
                    elem_s = csv.iloc[j][csv.columns != 'index_col'].astype(float)
                else:
                    elem_s += np.around(np.array(csv.iloc[j][csv.columns !=  'index_col'].astype(float)), 3)
                count_elem +=1                                                                                                                                                          
        if len(elem_s)==0:
            elem_s = np.zeros(num_features[num_db])
            count_elem = 0
        vector_s.append(elem_s)
        count_vector.append(np.array(count_elem))
    
    vector_d = []
    distance = lambda u, v: ((u-v)**2).sum()
    for j in range(len(csv)):
        elem_d = []
        for elem in centers[:][:][:][:]:
            elem_d.append(distance(np.array(csv.iloc[j][csv.columns != 'index_col']), elem[num_db][:]))
        vector_d.append(elem_d)
    csv.drop(['index_col'], axis = 1, inplace = True)
    csv.to_csv(csv_path, sep=";", index = False)
    return vector_d, vector_s, count_vector