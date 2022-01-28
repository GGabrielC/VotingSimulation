from VotingSystem.VotingSystem import VotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from statistics import stdev
import pandas as pd

class MaxStandardDeviationWeightedSumWins(VotingSystem):
    def __init__(self, alpha=0):
        self.alpha = alpha
        super().__init__(name="MaxStandardDeviationWeightedSumWins<α={}>".format(self.alpha))

    def _runAlgorithm(self, processedBallots: MyProcessedRankedBallots) -> dict:
        dfStages = processedBallots.dfScoreOfCandidates
        ThresholdFilter(self.alpha)
        firstValidStageIndex = ThresholdFilter(self.alpha).run(dfStages)
        dfStages = dfStages[firstValidStageIndex:]
        weights = dfStages.apply(lambda x: stdev(x), axis=1)
        winnersPerStage = dfStages.idxmax(axis=1)
        absoluteCandidateScore = {c:0 for c in processedBallots.candidates}
        point = 1
        for weight, winner in zip(weights, winnersPerStage):
            absoluteCandidateScore[winner] += weight*point
        winner = pd.Series(absoluteCandidateScore).idxmax()
        return {"winner": winner, "algorithm": self.name}
