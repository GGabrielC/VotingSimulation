from VotingSystem.VotingSystems.MyVotingSystem.MyAbstractVotingSystem import MyAbstractVotingSystem
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.EntropyFilter import EntropyFilter
from VotingSystem.VotingSystems.MyVotingSystem.MyVotingSystem import constructName


class BasicEntropy (MyAbstractVotingSystem):
    def __init__(self, alpha):
        name = constructName(alpha, )
        super().__init__(EntropyFilter(), [ThresholdFilter(alpha)], name=name)
        self.alpha = alpha
