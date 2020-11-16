#utility function for scenario 2


from db_manager import *


from sklearn.cluster import KMeans 
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as d
import glob, os
import numpy as np
import random as random
import math 
import sys

# parameters for spain dataset
NUM_CLUSTERS = 5
num_features = [7, 4, 5] 
num_istances = 3648
num_databases = 3 


def start_server():
    centroids = []
    csvfile = pd.read_csv("spain_scenario2/global_scenario2_spain.csv", sep=";")
    csvfile.fillna(0, inplace=True)
    sample = csvfile.sample(NUM_CLUSTERS)
    list_numbers = np.around(np.array(sample),3)
    centers = []
    for elem in list_numbers:
        centers.append(np.split(elem, [7,11,16])[0:3])
    return centers

def compare_vectors(vector1, vector2):
    false = 0 
    for i in range(len(vector1)): 
        for j in range(len(vector1[i])):
            if np.array_equal(vector1[i][j],vector2[i][j])==False: 
                false += 1
    if false == 0:  
        return True
    else: 
        return False

def send_centers(centroids):
    i = 0
    result = []
    for file in glob.glob("spain_scenario2/partitioned/spain_*.csv"):
        partial = receive_centers(file, centroids, i)
        i += 1
        result.append(partial)
    k=0
    centroids_sum = []
    for elem in result[0]:
        partial = 0
        elem_sum = []
        for i in range(len(elem)):
            sum =0
            for j in range(len(result)):
                sum += result[j][k][i]
            sum = math.sqrt(sum)
            elem_sum.append(sum)
        centroids_sum.append(elem_sum)
        k += 1
    return centroids_sum


def assign_centers(centroids, centroids_sum):
    vector_q = []
    for elem in centroids_sum: 
        minDis = sys.float_info.max
        index = 0
        for i in range(len(elem)): 
            if elem[i] < minDis:
                index = i
                minDis = elem[i]
        vector_q.append(centroids[index])
    return vector_q

def server_execution_phase(vector_q,centroids):
    vector_d = []
    vector_s = []
    count_vector = []
    i=0
    for file in glob.glob("spain_scenario2/partitioned/spain_*.csv"):
        result = execution_phase(vector_q, i, file, centroids)
        new_elem = result[0]
        vector_d.append(new_elem)
        new_elem = result[1]
        vector_s.append(new_elem)
        new_elem = result[2]
        count_vector.append(new_elem)
        i += 1

    new_centroids = []
    for i in range(NUM_CLUSTERS): 
        new_centroid = []
        for db in range(num_databases): 
            new_centroid.append(np.around((vector_s[db][i]/ count_vector[db][i]), 3)) 
        new_centroids.append(new_centroid)

    temp_q = []
    for i in range(num_istances):
        elem_sum = [] 
        for j in range(num_databases): 
            if len(elem_sum) == 0 : 
                elem_sum = (np.array(vector_d[j][i])).astype(float)
            else: 
                elem_sum += (np.array(vector_d[j][i])).astype(float)
        temp_q.append(elem_sum)
    

    new_vector_q = []
    for elem in temp_q: 
        minDis = sys.float_info.max
        index = 0
        for i in range(len(elem)): 
            if elem[i] < minDis:
                index = i
                minDis = elem[i]
        new_vector_q.append(new_centroids[index])

    return new_centroids, new_vector_q, count_vector[0]


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

def compare_vectors_global(vector1, vector2):
    false = 0 
    for i in range(len(vector1)): 
            if np.array_equal(vector1[i],vector2[i])==False: 
                false += 1
    if false == 0:  
        return True
    else: 
        return False