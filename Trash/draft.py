from DataHelpers.SimulationData import SimulationData
from WisdomOfTheCrowds import Crowd
from WisdomOfTheCrowds.CrowdBuilder import buildCrowd

def draftSamplePredict(sData, crowd):
    y = crowd.predict(sData.df_test_x)
    #y = crowd.roundPredict(sData.df_test_x)
    print(y)
def draftSampleEvaluateMSE(sData, crowd, batch_size):
    ev = crowd.evaluate(df_test_y=sData.df_test_y, df_test_x=sData.df_test_x, batch_size=batch_size, metric="mean_squared_error")
    print(ev)
def draftSampleEvaluateCM(sData, crowd, batch_size):
    ev = crowd.evaluate(df_test_y=sData.df_test_y, df_test_x=sData.df_test_x, batch_size=batch_size, metric="confusion_matrix")
    print(ev)
def draftSampleEvaluateEmergentProperties(sData, crowd, batch_size):
    em = crowd.evaluateEmergentPropertiesWithMeanAndMedian(df_test_x=sData.df_test_x, df_test_y=sData.df_test_y, batch_size=batch_size)
    print(em)

def draft():
    batch_size, metric = 128, "confusion_matrix"
    dataInfo = SimulationData.getDataInfo('fish')
    params = {i: dataInfo[i] for i in dataInfo if i in ['filePaths', 'yName', 'delimiter', 'needsToBeBalanced']}
    sData = SimulationData.getData(**params, test_size=0.3)

    dfCrowd = buildCrowd(splittedData=sData, size=1, epochs=1, trainableLayerCountInterval=[33, 33],
                         filterOutSomeModels=True, maxOutput=dataInfo['maxOutput'])
    crowd = Crowd(dfCrowd)

    indivPreds = crowd.predictionIndividuals(x=sData.df_test_x, batch_size=128)
    results = crowd.evaluate(indivPreds=indivPreds, df_test_y=sData.df_test_y, batch_size=batch_size, metric=metric)
    #print(pd.DataFrame(results[metric]))
    print(results[metric])

    emergentProperties = crowd.evaluateEmergentPropertiesWithMeanAndMedian(
        df_test_x=sData.df_test_x, df_test_y=sData.df_test_y, batch_size=batch_size, indivPreds=indivPreds)
    print(emergentProperties)