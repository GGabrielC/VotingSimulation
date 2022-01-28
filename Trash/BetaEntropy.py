from VotingSystem.VotingSystems.MyVotingSystem.MyAbstractVotingSystem import MyAbstractVotingSystem
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.EntropyFilter import EntropyFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ONLY_NULL_CANDIDATE
from VotingSystem.VotingSystems.MyVotingSystem.MyVotingSystem import constructName


class BetaEntropy (MyAbstractVotingSystem):
    def __init__(self, alpha, beta, defaultOffset=-1):
        name = "BetaEntropy <\u03B1:{}, \u03B2:{}>".format(self.alpha, self.beta)
        super().__init__(EntropyFilter(),
                         [ThresholdFilter(alpha)],
                         [ThresholdFilter(beta, ONLY_NULL_CANDIDATE, defaultOffset=defaultOffset)],
                         name=name)
        self.alpha = alpha
        self.beta = beta