from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import random
import numpy as np
from keras.callbacks import Callback
from WisdomOfTheCrowds.Voter import Voter

def takeLastEpochResults(results):
    r = dict()
    for k, v in results.items():
        r[k] = v[-1]
    return r

def convertResultsEval(sampleModel, resultsEvalModels):
    metrics = sampleModel.metrics_names
    resultsEvalModels = [{metric: result[metrics.index(metric)] for metric in metrics} for result in resultsEvalModels]
    [[r.update({"val_" + k: r.pop(k)}) for k in [i for i in r.keys()]] for r in resultsEvalModels]
    return resultsEvalModels

def combineResults(sampleModel, resultsFitModels, resultsEvalModels):
    resultsEvalModels = convertResultsEval(sampleModel, resultsEvalModels)
    results = [{**(takeLastEpochResults(rFit.history)), **rEval} for rFit, rEval in zip(resultsFitModels, resultsEvalModels)]
    return results

class StopAtLossValue(Callback):
    def __init__(self, threshold, monitor='loss'):
        super().__init__()
        self.monitor = monitor
        self.threshold = threshold

    def on_epoch_end(self, batch, logs={}):
        if logs.get(self.monitor) <= self.threshold:
             self.model.stop_training = True

class StopAtStagnation(Callback):
    def __init__(self, relativeMinimumImprovement=0.0015, monitor='loss', countLastIterations=5):
        super().__init__()
        self.monitor = monitor
        self.relativeMinimumImprovement = relativeMinimumImprovement
        self.countLastIterations = countLastIterations
        self.counter = 0
        self.previousScore = None

    def on_epoch_end(self, batch, logs={}):
        score = logs.get(self.monitor)
        if self.previousScore is None:
            self.previousScore = score
        else:
            maximumAcceptedScore = self.previousScore-self.previousScore*self.relativeMinimumImprovement
            self.counter += 1 if maximumAcceptedScore < score else 0
        if self.counter == self.countLastIterations:
            self.model.stop_training = True
            print("Stagnation Detected !")

class CrowdMember(Sequential, Voter):
    def __init__(self, trainableLayerCount, metric, maxOutput, paremetersFit, parametersEval,
                 testAtEachEpoch, columnBlindness=0, callbacks=None):
        super().__init__()
        sampleInput = paremetersFit["x"].iloc[0:1,]
        self.callbacks = [*callbacks, StopAtStagnation(monitor="val_mean_squared_error")]
        self.setTopology(trainableLayerCount, metric, sampleInput, maxOutput, columnBlindness)
        self.train(paremetersFit=paremetersFit, parametersEval=parametersEval, testAtEachEpoch=testAtEachEpoch)

    def setTopology(self, trainableLayerCount, metric, sampleInput, maxOutput, columnBlindness):
        loss = None
        if metric == 'mean_squared_error':
            loss = 'mean_squared_error'
        elif metric == 'sparse_categorical_crossentropy':
            loss = 'accuracy'

        if type(columnBlindness) is list:
            left, right = columnBlindness[0], columnBlindness[1]
            if right < 1:
                columnBlindness = random.uniform(left, right)
            else:
                columnBlindness = random.randint(left, right)
        if columnBlindness < 1:
            countVisibleColumns = max(1, int((1 - columnBlindness) * (sampleInput.shape[1])))
        elif columnBlindness >= 1:
            countVisibleColumns = max(1, sampleInput.shape[1] - columnBlindness)
        self._visibleColumns = list(sorted(random.sample(range(0, sampleInput.shape[1]), countVisibleColumns)))
        self.constructLayers(trainableLayerCount, sampleInput, maxOutput)
        self.compile(optimizer='adam', loss=loss, metrics=[metric])

    def fit(self, *args, **kwargs):
        kwargs['x'] = kwargs['x'].iloc[:,self._visibleColumns].to_numpy()
        if 'y' in kwargs.keys() and kwargs['y'] is not None:
            kwargs['y'] = kwargs['y'].to_numpy()
        if 'validation_data' in kwargs.keys() and kwargs['validation_data'] is not None:
            x_val = kwargs['validation_data'][0].iloc[:,self._visibleColumns].to_numpy()
            y_val = kwargs['validation_data'][1].to_numpy()
            kwargs['validation_data'] = (x_val, y_val)
        return super().fit(*args,**kwargs)

    def predict(self, x, *args, **kwargs):
        if x is None :
            print(x)
        x = x.iloc[:,self._visibleColumns].to_numpy()
        return super().predict(x,*args,**kwargs)

    def evaluate(self, *args, **kwargs):
        if type(kwargs['x']) is not np.ndarray:
            kwargs['x'] = kwargs['x'].iloc[:,self._visibleColumns].to_numpy()
        if 'y' in kwargs.keys() and kwargs['y'] is not None and type(kwargs['y']) is not np.ndarray:
            kwargs['y'] = kwargs['y'].to_numpy()
        return super().evaluate(*args, **kwargs)

    def train(self, paremetersFit, parametersEval, testAtEachEpoch):
        resultsFit = self.fit(callbacks=self.callbacks, **paremetersFit)
        if testAtEachEpoch:
            modelResult = resultsFit.history
            results = takeLastEpochResults(modelResult)
        else:
            resultsEval = self.evaluate(**parametersEval)
            results = combineResults(self, resultsFit, resultsEval)
        self.trainResults = results
        return self.trainResults

    def constructLayers(self, trainableLayerCount, sampleInput, maxOutput):
        #self.add(Dropout(0.11))
        for i in range(trainableLayerCount):
            self.add(Dense(sampleInput.iloc[:,self._visibleColumns].shape[1], activation='relu'))
            #self.add(Dropout(0.11))
        lastLayerActivation = 'linear'
        self.add(Dense(1, activation=lastLayerActivation))
