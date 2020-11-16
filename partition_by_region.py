# partition global data set in subset according to value of column cod_ine that represent region code
# example for spain  and usa dataset, equal for all the other dataset

import pandas as pd
import numpy as np
import glob
from matplotlib import dates as d

# SPAIN
#global_path = "scenario1/global_spain.csv"
#partition_path = "scenario1/partitioned_spain"
#partition_col = 'cod_ine'

#ITALY 
global_path = "scenario1/global_italy.csv"
partition_path = "scenario1/partitioned_ita"
partition_col = 'codice_regione'


# USA
#global_path = "scenario1/global_usa.csv"
#partition_path = "scenario1/partitioned_usa"
#partition_col = 'state'


csv = pd.read_csv(global_path, sep=";", parse_dates = ["data"])
csv.fillna(0, inplace=True)
csv['data']=d.date2num(csv['data'])
csv.to_csv(global_path, sep=";", index=False)



data_category_range = csv[partition_col].unique()
data_category_range = data_category_range.tolist()

for i,value in enumerate(data_category_range):
    csv[csv[partition_col] == value].to_csv(str(partition_path)+r'/ita_region_'+str(value)+r'.csv',sep=";",index = False)

for file in glob.glob(str(partition_path)+"/*.csv"):
    csv = pd.read_csv(file, sep=";")
    csv.dropna(axis=0, how="any", inplace=True)
    csv.to_csv(file, sep=";", index=False)

