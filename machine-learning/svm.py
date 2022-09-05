from datetime import datetime
from random import random

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler as SC
from sklearn.svm import SVC 
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

class SVM():

    def __init__(self):
        start = datetime.now()
        print("Opening dataset.\n")
        self.dataset = pd.read_csv('train/dataset-small.csv')
        end = datetime.now()
        print("Dataset read time: ", (end.microsecond-start.microsecond), " microseconds")

    def training(self):
        print("Training initialised")

        # Making X the features and y the label
        X = self.dataset.drop('Class', axis=1)
        y = self.dataset['Class']

        # Train test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Now fitting the SVM with the training set
        classifier = SVC(kernel='linear', random_state=0)
        model = classifier.fit(X_train, y_train)

        # Testing classification
        y_pred = model.predict(X_test)

        print("-----------Fitting complete--------------")
        # Create a vonfusion matrix, accuracy score and then report
        print("     Confusion Matrix        ")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)

        print("     Accuracy Score        ")
        acc = accuracy_score(y_test, y_pred)
        print("Success = {0:.2f}%" .format(acc*100))
        failure = 1.0 - acc
        print("Fail = {0:.2f}%" .format(failure*100))

        print("     Confusion Report        ")
        cr = classification_report(y_test,y_pred)
        print(cr)

        # Save the model
        filename = 'models/finalised_model_svm.sav'
        joblib.dump(classifier, filename)
        
def main():
    start = datetime.now()

    svm = SVM()
    svm.training()

    end = datetime.now()
    print("Total time to train: ", (end.microsecond-start.microsecond), " microseconds")

if __name__ == "__main__":
    main()