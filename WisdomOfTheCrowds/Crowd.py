import numpy as np
import tensorflow.keras
import sklearn
from WisdomOfTheCrowds.Voter import Voter

def handleResults(y, df_test_y, metric="mean_squared_error"):
    if metric == "mean_squared_error":
        metric = tensorflow.keras.losses.MeanSquaredError()
        mse = metric(df_test_y.to_numpy(), y).numpy()
        return mse
    elif metric == "confusion_matrix":
        matrix = sklearn.metrics.confusion_matrix(df_test_y.to_numpy(), np.round(y))
        return matrix
    custom = metric(df_test_y, y).numpy()
    return custom

class Crowd(list, Voter):
    def __init__(self, name=None, metricPredict=np.mean, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crowd = self
        self.name = name
        self.metricPredict = metricPredict

    def getBestMemberByValMSE(self):
        best = self[0]
        for m in self:
            if m.trainResults["val_mean_squared_error"] < best.trainResults["val_mean_squared_error"]:
                best = m
        return best

    def predictionIndividuals(self, x, batch_size=128):
        return [individual.predict(x, batch_size=batch_size, verbose=0) for individual in self]

    def predict(self, x=None, metric=None, batch_size=128, indivPreds=None):
        if indivPreds is None:
            indivPreds = self.predictionIndividuals(x, batch_size=batch_size)
        if metric is None:
            metric = self.metricPredict
        y = [metric(i) for i in zip(*indivPreds)]
        return np.array(y)

    def roundPredict(self, x=None, metric=np.mean, batch_size=128, indivPreds=None):
        return np.round(self.predict(x=x, metric=metric, batch_size=batch_size, indivPreds=indivPreds))

    def evaluate(self, df_test_y, df_test_x=None, batch_size=128, metricPredict=np.mean,
                 metricEval="mean_squared_error", y=None, indivPreds=None):
        if y is None:
            if indivPreds is None:
                y = self.predict(x=df_test_x, metric=metricPredict, batch_size=batch_size)
            else:
                y = self.predict(indivPreds=indivPreds, metric=metricPredict, batch_size=batch_size)
        return handleResults(y, df_test_y, metricEval)

    def voteRankedIndividuals(self, nonNullCandidates, nullCandidateScore, nullCandidateID):
        ballots = [m.voteRanked(nonNullCandidates, nullCandidateScore, nullCandidateID) for m in self]
        return ballots

    # @staticmethod
    # def errorFunc(a, b):
    #     return ((a - b) ** 2) ** (1 / 2)
    #
    # def evaluateEmergentPropertiesWithMeanAndMedian(self, df_test_x, df_test_y, batch_size=128, indivPreds=None):
    #     if indivPreds is None:
    #         indivPreds = self.predictionIndividuals(x=df_test_x, batch_size=batch_size)
    #     y_median = self.predict(metric=np.median, batch_size=128, indivPreds=indivPreds)
    #     y_mean = self.predict(metric=np.mean, batch_size=128, indivPreds=indivPreds)
    #     indivPreds = zip(*indivPreds)
    #
    #     medianScore, meanScore = 0.0, 0.0
    #     for y, ty, ymedian, ymean in zip(indivPreds, df_test_y.iloc[:,0], y_median, y_mean):
    #         medianErr = self.errorFunc(ymedian, ty)
    #         meanErr = self.errorFunc(ymean, ty)
    #         errors = [self.errorFunc(ey, ty) for ey in y]
    #         bestIndividualErr = min(errors)
    #
    #         if bestIndividualErr > medianErr: medianScore+=1
    #         if bestIndividualErr > meanErr: meanScore+=1
    #     return {"emergence_median_win_rate":medianScore/len(df_test_y), "emergence_mean_win_rate":meanScore/len(df_test_y)}
