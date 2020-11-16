# utility functions for scenario 1



from sklearn.cluster import KMeans 
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as date
from sklearn.model_selection import train_test_split
import glob, os
import numpy as np
import sys
import math 


# spain dataset
num_features = 7

# ita dataset
#num_features = 4

# spain dataset
#num_features = 11


def compare_vectors(vector1, vector2):
    false = 0 
    for i in range(len(vector1)): 
            if np.array_equal(vector1[i],vector2[i])==False: 
                false += 1
    if false == 0:  
        return True
    else: 
        return False

 
def mapper(file, centers): 
    csv = pd.read_csv(file,sep=";")

    distance = lambda u, v: math.sqrt(((u-v)**2).sum())
    distance_vector = []
    clusters = []
    for i in range(len(csv)): 
        minDis = sys.float_info.max
        index = 0
        for j in range(len(centers)):
            dist = distance(np.array(csv.iloc[i][:]), centers[j])
            if dist < minDis: 
                index = j
                minDis = dist
        clusters.append(index)
        distance_vector.append(minDis)
    csv['cluster_predict'] = clusters
    
    csv.to_csv(file, sep=";", index=False)
    return distance_vector

def combiner(file, centers):
    sum_members = []
    count_members = []

    csv = pd.read_csv(file, sep=";")
    
    for i in range(len(centers)):
        current_count = 0
        current_sum = []
        for j in range(len(csv)): 
            if (csv.iloc[j][csv.columns == 'cluster_predict']==i).bool():
                if len(current_sum)==0:
                    current_sum = np.around(np.array(csv.iloc[j][csv.columns != 'cluster_predict'].astype(float)), 3)
                else: 
                    current_sum += np.around(np.array(csv.iloc[j][csv.columns != 'cluster_predict'].astype(float)), 3)
                current_count +=1
        if len(current_sum)==0: 
            current_sum = np.zeros(num_features)
        count_members.append(current_count)
        sum_members.append(current_sum)

    csv.drop(['cluster_predict'], axis=1, inplace=True)
    csv.to_csv(file, sep=";", index=False)
    return count_members, sum_members

def assign_elem_to_clusters(csv, new_centroids): 
    dist = []
    clusters = []
    vector_dis =[]
    distance = lambda u, v: math.sqrt(((u-v)**2).sum())
    for i in range(len(csv)):
        minDis = sys.float_info.max
        index = 0
        for j in range(len(new_centroids)):
            dist = distance(np.array(csv.iloc[i][:]), new_centroids[j])
            if dist < minDis: 
                index = j
                minDis = dist
        clusters.append(index)
        vector_dis.append(minDis)
    return clusters, vector_dis

def create_centroids_vector(old_vector): 
    new_centroids = []
    temp = []
    for elem in old_vector: 
        for j in range(len(elem)):
            temp.append(np.array(elem[j]))
    i = 0
    new_center = []
    for elem in temp:
        if i == 3: 
            new_centroids.append(new_center)
            i=0
            new_center = []
        for j in range(len(elem)):
            new_center.append(elem[j])
        i += 1
    new_centroids.append(new_center)

    return new_centroids