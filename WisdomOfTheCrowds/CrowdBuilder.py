import numpy as np
from WisdomOfTheCrowds.CrowdMember import CrowdMember
from WisdomOfTheCrowds.CrowdMember import StopAtLossValue
from WisdomOfTheCrowds.Crowd import Crowd

class CrowdBuilder():
    def __init__(self, epochs=1, batch_size = 64, verbose = 1,
                   maxOutput = None, trainableLayerCount=10,
                   metric ="mean_squared_error", testAtEachEpoch = True,
                   columnBlindness=0, method=None):
        self.method = method
        self.epochs = epochs
        self.batch_size = batch_size
        self.verbose = verbose
        self.maxOutput = maxOutput
        self.trainableLayerCount = trainableLayerCount
        self.metric = metric
        self.testAtEachEpoch = testAtEachEpoch
        self.columnBlindness = columnBlindness

    def buildCrowd(self, splittedData, size=100):
        paremetersFit, parametersEval = self.getFEParameters(splittedData, fit=True, eval=True)
        crowd = self.generateModels(size, paremetersFit, parametersEval)
        params = {"df_test_y":splittedData.df_test_y, "df_test_x":splittedData.df_test_x}
        crowdVal_mean = crowd.evaluate(**params, metricPredict=np.mean)
        crowdVal_median = crowd.evaluate(**params, metricPredict=np.median)
        return crowd, (crowdVal_mean, crowdVal_median)

    def generateModelsAfterLimitsValMSE(self, count_models, paremetersFit, parametersEval, bestMSE=None, worstMSE=None):
        models = Crowd()
        callbacks=[]
        if bestMSE is not None:
            callbacks.append(StopAtLossValue(threshold=bestMSE, monitor='val_mean_squared_error'))
        while (len(models) < count_models):
            print("Currently they are {}/{} models!".format(len(models), count_models))
            member = CrowdMember(self.trainableLayerCount, self.metric, self.maxOutput,
                                 paremetersFit, parametersEval, testAtEachEpoch=True,
                                 columnBlindness=self.columnBlindness, callbacks=callbacks)
            memberIsNotGoodEnough = worstMSE != None and member.trainResults["val_mean_squared_error"] > worstMSE
            if not memberIsNotGoodEnough:
                models.append(member); print("Model Added!")
            else:
                print("Model not Added! worstMSE={} MSE={}".format(worstMSE, member.trainResults["val_mean_squared_error"]))
        return models

    def generateModelsAfterStandardDistribution(self, count_models, paremetersFit, parametersEval, mean, stDev):
        models = Crowd()
        countTrainings, expectedValMSE = 0, -1
        trigger = triggerMoment = 5

        while (len(models) < count_models):
            print("Currently they are {}/{} models!".format(len(models), count_models))
            if trigger == triggerMoment:
                trigger = expectedValMSE = 0
                while expectedValMSE <= 0:
                    expectedValMSE = np.random.normal(loc=mean, scale=stDev)
            print("expectedValMSE={}".format(expectedValMSE))
            callbacks = [StopAtLossValue(threshold=expectedValMSE, monitor='val_mean_squared_error'),]
            member = CrowdMember(self.trainableLayerCount, self.metric, self.maxOutput,
                                 paremetersFit, parametersEval, testAtEachEpoch=True,
                                 columnBlindness=self.columnBlindness, callbacks=callbacks)
            error, maxError = member.trainResults["val_mean_squared_error"]-expectedValMSE, 0.05*stDev
            if error < maxError:
                trigger, expectedValMSE = triggerMoment, -1
                models.append(member); print("Model Added!")
            else:
                trigger += 1; print("Model not Added!  error={} maxError={}".format(error, maxError))
            countTrainings+=1; print("countTrainings={}".format(countTrainings))
        return models

    def generateModels(self, count_models, paremetersFit, parametersEval):
        if self.method is None:
            return self.generateModelsAfterLimitsValMSE(count_models, paremetersFit, parametersEval)
        elif self.method["name"] == "thresholdValMSE":
            return self.generateModelsAfterLimitsValMSE(count_models, paremetersFit, parametersEval,
                                                        self.method["bestMSE"],  self.method["worstMSE"])
        elif self.method["name"] == "standardDistribution":
            return self.generateModelsAfterStandardDistribution(count_models, paremetersFit, parametersEval,
                                                        self.method["mean"],  self.method["standardDeviation"])
        else:
            return self.method["function"](count_models, paremetersFit, parametersEval, self, **self.method["params"])

    def getFEParameters(self, sData, fit=False, eval=False):
        trainData = {'x': sData.df_train_x, 'y': sData.df_train_y}
        testData = {'x': sData.df_test_x, 'y': sData.df_test_y}
        validation_data = (testData['x'], testData['y']) if self.testAtEachEpoch else None

        commonParams = {'batch_size': self.batch_size, 'verbose': self.verbose}
        fitParams = {**commonParams, **trainData, 'epochs': self.epochs, 'validation_data': validation_data}
        evalParams = {**commonParams, **testData}
        if fit and eval:
            return fitParams, evalParams
        elif fit:
            return fitParams
        elif eval:
            return evalParams
        else:
            return Exception("Sorry bro/sis, can't have both fit=False eval=False !")
