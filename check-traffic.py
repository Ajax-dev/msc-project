import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import joblib
import pandas as pd


# filename = 'models/finalised_model_svm.sav'
filename = 'models/finalised_model_rf.sav'
# filename = 'models/finalised_model_knn.sav'
classifier = joblib.load(filename)
dt_current = pd.read_csv('data/realtime.csv')
result = classifier.predict(dt_current)

with open('.result', 'w') as f:
    print("\033[38;5;208mINSPECTING\033[0;0m")
    f.write(str(result[0]))
