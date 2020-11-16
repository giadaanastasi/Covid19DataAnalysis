# used to clean files
# used to convert string in usa dataset in integers 

from sklearn.cluster import KMeans 
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as d
import glob, os
import numpy as np
import random as random
import math 
#from random import sample
from scipy.spatial import distance as dist



states = ['AK', 'AL', 'AR', 'AS',	'AZ',	'CA',	'CO',	'CT',	'DC',	'DE',	'FL',	'GA',	'GU',	'HI',	'IA',	
'ID',	'IL',	'IN',	'KS',	'KY',	'LA',	'MA',	'MD',	'ME',	'MI',	'MN',	'MO',	'MP',	'MS',	
'MT',	'NC',	'ND',	'NE',	'NH',	'NJ',	'NM',	'NV',	'NY',	'OH',	'OK',	'OR',	'PA',	'PR',	'RI',	'SC',	'SD',	
'TN'	,'TX','UT',	'VA',	'VI',	'VT',	'WA',	'WI',	'WV',	'WY']

csv= pd.read_csv("global_usa.csv", sep=";")
new_states = []
for i in range(len(csv)): 
    for j in range(len(states)):
        if (csv.iloc[i][csv.columns == 'state']==states[j]).bool():
            new_states.append(j+1)

csv.drop(['state'],axis=1, inplace=True)
csv['state']=new_states
csv.fillna(0, inplace=True)
csv.to_csv("global_usa.csv", sep=";", index = False)