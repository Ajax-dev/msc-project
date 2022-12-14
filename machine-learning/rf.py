from datetime import datetime
from random import random

import pandas as pd
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

class RandomForest():

    def __init__(self):
        start = datetime.now()
        print("Opening dataset.\n")
        self.dataset = pd.read_csv('../train/dataset-small.csv')
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
        classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=0)
        model = classifier.fit(X_train, y_train)

        # Testing classification
        y_pred = model.predict(X_test)

        print("-----------Fitting complete--------------")
        # Create a vonfusion matrix, accuracy score and then report
        print("     Confusion Matrix        ")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)

        ### Printing heatmap - seaborn
        x_labels = ["Actual Normal", "Actual DDoS"]
        y_labels = ["Predicted Normal", "Predicted DDoS"]
        sn.heatmap(cm, linewidths=1,annot=True, fmt='g', xticklabels=x_labels, yticklabels=y_labels)

        print("     Accuracy Score        ")
        acc = accuracy_score(y_test, y_pred)
        print("Success = {0:.2f}%" .format(acc*100))
        failure = 1.0 - acc
        print("Fail = {0:.2f}%" .format(failure*100))

        print("     Classification Report        ")
        cr = classification_report(y_test,y_pred)
        print(cr)

        # Save the model
        filename = '../models/finalised_model_rf.sav'
        joblib.dump(classifier, filename)
        
def main():
    start = datetime.now()

    rf = RandomForest()
    rf.training()

    end = datetime.now()
    print("Total time to train: ", (end.microsecond-start.microsecond), " microseconds")

if __name__ == "__main__":
    main()