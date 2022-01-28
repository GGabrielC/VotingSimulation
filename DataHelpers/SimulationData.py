import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from collections import Counter
from DataHelpers.SplittedData import SplittedData

def nominalToNumeric(df):
    lencoders = dict()
    for column in df:
        if df[column].dtype != 'float':
            le = preprocessing.LabelEncoder()
            lencoders[column] = le
            le.fit(df[column])
            df[column] = le.transform(df[column])

def balanceData(df,yName):
    c = Counter(df[yName])
    bestK, bestV = None, -1
    for k,v in c.items():
        if v > bestV:
            bestK, bestV = k, v
    for k,v in c.items():
        times = int(bestV/v)
        dfToAppend = df[df[yName]==k]
        for _ in range(times - 1):
            dfToAppend = dfToAppend.append(df[df[yName]==k])
        if times > 1:
            df = df.append(dfToAppend)
    return df

class SimulationData:
    @staticmethod
    def getData(filePaths, yName, test_size=0.3, delimiter=None, needsToBeBalanced=False):
        dfs = [pd.read_csv(filePath, delimiter=delimiter) for filePath in filePaths]
        df = pd.concat(dfs, axis=0, ignore_index=True)
        nominalToNumeric(df)
        if needsToBeBalanced:
            df = balanceData(df, yName)
        df = df.sample(frac=1)

        train, test = train_test_split(df, test_size=test_size)
        df_train_x, df_train_y = train.loc[:, train.columns != yName], train[[yName]]
        df_test_x, df_test_y = test.loc[:, test.columns != yName], test[[yName]]
        return SplittedData(df_train_x=df_train_x, df_train_y=df_train_y, df_test_x=df_test_x, df_test_y=df_test_y)

    @staticmethod
    def getDataInfo(dataSetName):
        needsToBeBalanced = None
        maxOutput = None
        delimiter = None
        bestWantedValMSE, worstWantedValMSE = {}, {}
        wantedMeanValMSE, wantedStDevValMSE = {}, {}

        if dataSetName == 'iris':
            yName, delimiter = 'petal-width', ','
            needsToBeBalanced = False
            fileNames = ['iris.data']
            worstWantedValMSE['petal-width'] = 0.5
            bestWantedValMSE['petal-width'] = 0.1

            wantedMeanValMSE['petal-width'] = 1
            wantedStDevValMSE['petal-width'] = 0.2
        elif dataSetName == 'wine':
            yName, delimiter, maxOutput = 'quality', ';', 10
            needsToBeBalanced = True
            worstWantedValMSE = 16
            fileNames = ['winequality-red.csv', 'winequality-white.csv']
        elif dataSetName == "mySynthetic":
            yName = 'y'
            fileNames = ["MySyntheticDataset.csv"]
            wantedMeanValMSE['y'] = 9500
            wantedStDevValMSE['y'] = 1000
        elif dataSetName == 'fish':
            yName, delimiter = 'Weight', ','
            needsToBeBalanced = False
            fileNames = ['Fish.data']
        elif dataSetName == 'house':
            yName = 'Y house price of unit area'
            fileNames = ['Real estate valuation data set.csv']
        elif dataSetName == 'student':
            yName, delimiter, maxOutput = 'G3', ';', 20
            fileNames = ['student-mat.csv']

        pathPrefixData = "Data"
        filePaths = [os.path.join(os.getcwd(), pathPrefixData, fileName) for fileName in fileNames]
        return {'dataSetName':dataSetName,
                'filePaths': filePaths, 'yName': yName, 'delimiter': delimiter,
                'maxOutput': maxOutput, 'needsToBeBalanced': needsToBeBalanced,
                "worstWantedValMSE": worstWantedValMSE, "bestWantedValMSE":bestWantedValMSE,
                "wantedMeanValMSE":wantedMeanValMSE, "wantedStDevValMSE":wantedStDevValMSE,
                }
