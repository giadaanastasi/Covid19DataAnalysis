# used to clean partitioned files if occur some error during execution

import pandas as pd
import numpy as np
import glob, os

for file in glob.glob("scenario1/partitioned_spain/*.csv"):
    csv = pd.read_csv(file, sep=";")
    csv.drop(['cluster_predict'], axis=1, inplace=True)
    csv.to_csv(file, sep=";", index=False)