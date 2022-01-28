from VotingSystem.VotingSystem import VotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.EntropyFilter import EntropyFilter
import pandas as pd
from scipy.stats import entropy

class MinEntropyProportionalWeightedSumWins2(VotingSystem):
    def __init__(self, alpha=0):
        self.alpha = alpha
        super().__init__(name="MinEntropyProportionalWeightedSumWins2<α={}>".format(self.alpha))

    def _runAlgorithm(self, processedBallots: MyProcessedRankedBallots) -> dict:
        maxEntropy = entropy([1/len(processedBallots.candidates)])
        dfStages = processedBallots.dfScoreOfCandidates
        ThresholdFilter(self.alpha)
        firstValidStageIndex = ThresholdFilter(self.alpha).run(dfStages)
        dfStages = dfStages[firstValidStageIndex:]
        weights = EntropyFilter().entropiesPerRow(dfStages)
        winnersPerStage = dfStages.idxmin(axis=1)
        absoluteCandidateScore = {c: 0 for c in processedBallots.candidates}
        point = 1+firstValidStageIndex
        for weight, winner in zip(weights, winnersPerStage):
            absoluteCandidateScore[winner] += (maxEntropy-weight) * point
            point+=1
        winner = pd.Series(absoluteCandidateScore).idxmax()
        return {"winner": winner, "algorithm": self.name}
