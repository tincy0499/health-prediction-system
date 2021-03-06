from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
import pandas as pd
import pickle
import json
import os

class LoadData:
    def __init__(self):
        import pymongo
        xs = 'pickles/x_scaler.pkl'
        ys = 'pickles/y_scaler.pkl'
        with open(xs, 'rb') as pickle_file:
            self.X_scaler = pickle.load(pickle_file)
        with open(ys, 'rb') as pickle_file:
            self.Y_scaler = pickle.load(pickle_file)

        mng_client = pymongo.MongoClient(
            "mongodb+srv://admin:admin@cluster0.vwurs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = mng_client.diabetes_data
        self.cursor = db.Diabetes_US.find({})

    def next(self, batchsize=None):
        res = []
        counter = 0
        for r in self.cursor:
            res.append(r)
            counter += 1
            if batchsize and counter == batchsize:
                break
        df = pd.DataFrame(res).drop('_id', axis=1)

        X_training = df.drop('Outcome', axis=1).values
        Y_training = df[['Outcome']].values

        X_scaled = self.X_scaler.transform(X_training)
        Y_scaled = self.Y_scaler.transform(Y_training)

        return X_scaled, Y_scaled

def load_data(scale=True):
    datafile = "../diabetes.csv"

    df = shuffle(pd.read_csv(datafile ,dtype=float))

    training_data = df.sample(frac=0.9)
    X_training = training_data.drop('Outcome', axis=1).values
    Y_training = training_data[['Outcome']].values

    testing_data = df.drop(training_data.index)
    X_testing = testing_data.drop('Outcome', axis=1).values
    Y_testing = testing_data[['Outcome']].values

    if not True:
        return (X_training, Y_training), (X_testing, Y_testing)

    print(len(df.index))
    print(len(training_data.index))
    print(len(testing_data.index))
    print(df.columns)

    X_scaler = MinMaxScaler(feature_range=(0, 1))
    Y_scaler = MinMaxScaler(feature_range=(0, 1))
    X_scaled_training = X_scaler.fit_transform(X_training)
    Y_scaled_training = Y_scaler.fit_transform(Y_training)

    X_scaled_testing = X_scaler.transform(X_testing)
    Y_scaled_testing = Y_scaler.transform(Y_testing)
    # print(X_scaled_training)

    xs = 'pickles/x_scaler.pkl'
    ys = 'pickles/y_scaler.pkl'
    with open(xs, 'wb') as pickle_file:
        pickle.dump(X_scaler, pickle_file)
    with open(ys, 'wb') as pickle_file:
        pickle.dump(Y_scaler, pickle_file)

    return (X_scaled_training,Y_scaled_training), (X_scaled_testing, Y_scaled_testing)

if __name__ == '__main__':
    # import_content('../diabetes.csv')
    load_data()


