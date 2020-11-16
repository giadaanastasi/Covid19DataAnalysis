# handle scenario 1
# example for spain dataset
 
from scenario1_utility import *


from sklearn.cluster import KMeans 
import pandas as pandas
from matplotlib import pyplot as plt
from matplotlib import dates as d
import glob, os
import numpy as np
from random import sample
from scipy.spatial import distance as dist
import time
from datetime import datetime

global_path = "scenario1/global_spain.csv"
partitioned_path = "scenario1/partitioned_spain"



def main():
    initial_centers = []

    csv = pd.read_csv(global_path, sep=";")
    csv.fillna(0, inplace = True)
    csv.to_csv(global_path, sep=";", index=False)

    centers = np.array(csv.sample(NUM_CLUSTERS))
    initial_centers = centers
    vector_q = []
    count_members = []
    sum_members = []
    for file in glob.glob(partitioned_path+"/*.csv"):
        vector_q.append(mapper(file, centers))
        result=combiner(file, centers)
        #print(result[1])
        #reduce function
        if len(count_members)==0:
            count_members = np.array(result[0]).astype(float)
            sum_members = np.array(result[1]).astype(float)
        else: 
            count_members += np.array(result[0]).astype(float)
            sum_members += np.array(result[1]).astype(float)
        
    centers = []
    for i in range(len(sum_members)):
        new_center = []
        for j in range(len(sum_members[i])):
            new_center.append(sum_members[i][j]/count_members[i])
        centers.append(new_center)
    
    iterations = 1
    while True: 
        count_members = []
        sum_members = []
        new_vector_q = []
        for file in glob.glob(partitioned_path+"/*.csv"):
            new_vector_q.append(mapper(file, centers))
            result=combiner(file, centers)
            #reduce function
            
            if len(count_members)==0:
                count_members = np.array(result[0]).astype(float)
                sum_members = np.array(result[1]).astype(float)
            else: 
                count_members += np.array(result[0]).astype(float)
                sum_members += np.array(result[1]).astype(float)

        new_centers = []

        for i in range(len(sum_members)):
            new_center = []
            for j in range(len(sum_members[i])):
                new_center.append(sum_members[i][j]/count_members[i])
            new_centers.append(new_center)

        #print(len(vector_q))
        #print(len(new_vector_q))

        if compare_vectors(vector_q, new_vector_q):
            break

        iterations +=1
        centers = new_centers
        vector_q = new_vector_q

    print("Terminated in "+str(iterations)+" iterations")   
    return count_members, centers, initial_centers


if __name__ == "__main__":

    NUM_ITERATIONS = 10
    NUM_CLUSTERS = 10
    count_vector = []
    new_centroids = []
    clusters = []

    #for i in range(NUM_ITERATIONS):
    start_time = datetime.now()
    result = main()
    end_time = datetime.now()
    count_vector = result[0]
        #print("Test n°: "+str(i)+' Duration: {}'.format(end_time - start_time))
    
    print("Final clusters partitioned: "+str(count_vector)) 

    new_centroids = result[1]
    
    start_time = datetime.now()
    centers = result[2]

        
    csv = pd.read_csv(global_path, sep=";")
    csv.fillna(0, inplace=True)
    
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
    
    centers = []
    for i in range(len(sum_members)):
        new_center = []
        for j in range(len(sum_members[i])):
            new_center.append(sum_members[i][j]/count_elem[i])
        centers.append(new_center)
    
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
        

        if compare_vectors(vector_q, new_vector_q):
            break

        centers = new_centers
        vector_q = new_vector_q
        iterations +=1

    end_time = datetime.now()
    print("Iterations: "+str(iterations)+' Duration: {}'.format(end_time - start_time))

    print("Final clusters global: "+str(count_elem))
