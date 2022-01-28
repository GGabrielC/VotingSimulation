from VotingSystem.VotingSystem import VotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots
from WisdomOfTheCrowds import Crowd
import numpy as np

class CrowdMetric(VotingSystem):
    def __init__(self, crowd:Crowd, metric=np.mean, metricName="Custom"):
        self.crowd = crowd
        self.metric = metric
        if metric is np.mean:
            metricName = "Mean"
        if metric is np.median:
            metricName = "Median"
        super().__init__(name="crowd-{}".format(metricName))

    def _runAlgorithm(self, processedBallots: MyProcessedRankedBallots) -> dict:
        ballot = self.crowd.voteRanked(**processedBallots.source)
        return {"winner": ballot[0], "algorithm": self.name}