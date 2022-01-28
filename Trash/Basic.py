from VotingSystem.VotingSystems.MyVotingSystem.MyAbstractVotingSystem import MyAbstractVotingSystem
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.FirstStageFilter import FirstStageFilter
from VotingSystem.VotingSystems.MyVotingSystem.MyVotingSystem import constructName


class Basic (MyAbstractVotingSystem):
    def __init__(self, alpha):
        name = constructName(alpha=alpha)
        super().__init__(FirstStageFilter(), [ ThresholdFilter(alpha) ],name=name)
        self.alpha = alpha