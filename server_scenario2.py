# server file for scenario 2
# handle server operations
# handle iterations and convergence of the algorithm



from scenario2_utility import *
from db_manager import *


from sklearn.cluster import KMeans 
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as d
import glob, os
import numpy as np
import random as random
import sys
import math 
from scipy.spatial import distance as dist
import time
from datetime import datetime


def main(): 
    centroids = start_server()
    initial_centroids = centroids
    centroids_sum = send_centers(centroids)
    vector_q = assign_centers(centroids, centroids_sum)
    result = server_execution_phase(vector_q, centroids)
    new_vector_q = result[1]
    new_centroids = result[0]
    

    iteration = 1
    count_vector = []

    while True: 
        print("iteration: "+str(iteration))
        if compare_vectors(vector_q, new_vector_q):
            break

        iteration +=1
        centroids = new_centroids
        vector_q = new_vector_q
        result = server_execution_phase(vector_q,centroids)
        new_vector_q = result[1]
        new_centroids = result[0]
        count_vector = result[2]

    print("Ended in "+str(iteration)+" iterations")
    return count_vector, new_centroids, initial_centroids
 

if __name__ == "__main__":
    NUM_ITERATIONS = 10
    NUM_CLUSTERS = 5
    count_vector = []
    new_centroids = []
    clusters = []

    

    #for i in range(NUM_ITERATIONS):
    start_time = datetime.now()
    result = main()
    end_time = datetime.now()
    count_vector = result[0]
    print(' Duration: {}'.format(end_time - start_time))

    print("Final clusters partitioned: "+str(count_vector)) 

    centers = []
    centers = create_centroids_vector(result[2])
    
        
    csv = pd.read_csv("spain_scenario2/global_scenario2_spain.csv", sep=";")
    csv.fillna(0, inplace=True)
    result=[]
    result = assign_elem_to_clusters(csv, centers)
    clusters = result[0]
    vector_q = result[1]
    count_elem = []
    sum_members = []

    for i in range(NUM_CLUSTERS):
        count = 0
        sum_elem = []
        for j in range(len(clusters)):
            if clusters[j]==i:
                count += 1
                if len(sum_elem)==0:
                    sum_elem = np.array(csv.iloc[j][:]).astype(float)
                else: 
                    sum_elem += np.array(csv.iloc[j][:]).astype(float)
        count_elem.append(count)
        sum_members.append(sum_elem)
    
    iterations = 1
    while True:
        result = assign_elem_to_clusters(csv, centers)
        clusters = result[0]
        new_vector_q = result[1]
        count_elem = []
        sum_members = []
        for i in range(NUM_CLUSTERS):
            count = 0
            sum_elem = []
            for j in range(len(clusters)):
                if clusters[j]==i:
                    count += 1
                    if len(sum_elem)==0:
                        sum_elem = np.array(csv.iloc[j][:]).astype(float)
                    else: 
                        sum_elem += np.array(csv.iloc[j][:]).astype(float)
            count_elem.append(count)
            sum_members.append(sum_elem)

        new_centers = []
        for i in range(len(sum_members)):
            new_center = []
            for j in range(len(sum_members[i])):
                new_center.append(sum_members[i][j]/count_elem[i])
            new_centers.append(new_center)
        

        if compare_vectors_global(vector_q, new_vector_q):
            break

        centers = new_centers
        vector_q = new_vector_q
        iterations +=1

    end_time = datetime.now()
    print("Iterations: "+str(iterations)+' Duration: {}'.format(end_time - start_time))

    print("Final clusters global: "+str(count_elem))
