from VotingSystem.VotingSystem import VotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from statistics import variance
import pandas as pd

class MaxVarianceProportionalWeightedSumWins(VotingSystem):
    def __init__(self, alpha=0):
        self.alpha = alpha
        super().__init__(name="MaxVarianceProportionalWeightedSumWins<α={}>".format(self.alpha))

    def _runAlgorithm(self, processedBallots: MyProcessedRankedBallots) -> dict:
        dfStages = processedBallots.dfScoreOfCandidates
        ThresholdFilter(self.alpha)
        firstValidStageIndex = ThresholdFilter(self.alpha).run(dfStages)
        dfStages = dfStages[firstValidStageIndex:]
        weights = dfStages.apply(lambda x: variance(x), axis=1)
        winnersPerStage = dfStages.idxmax(axis=1)
        absoluteCandidateScore = {c:0 for c in processedBallots.candidates}
        point = 1+firstValidStageIndex
        for weight, winner in zip(weights, winnersPerStage):
            absoluteCandidateScore[winner] += weight*point
            point+=1
        winner = pd.Series(absoluteCandidateScore).idxmax()
        return {"winner": winner, "algorithm": self.name}
