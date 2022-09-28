import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
import joblib

import pandas as pd
import numpy as np


filename = 'models/finalised_model_svm.sav'
classifier = joblib.load(filename)
dt_current = pd.read_csv('data/realtime.csv')
result = classifier.predict(dt_current)

with open('.result', 'w') as f:
    print("\033[38;5;208mINSPECTING\033[0;0m")
    f.write(str(result[0]))
