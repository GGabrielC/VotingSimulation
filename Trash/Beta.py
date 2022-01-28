from VotingSystem.VotingSystems.MyVotingSystem.MyAbstractVotingSystem import MyAbstractVotingSystem
from VotingSystem.VotingSystems.MyVotingSystem.MyVotingSystem import constructName
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.FirstStageFilter import FirstStageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ONLY_NULL_CANDIDATE

class Beta (MyAbstractVotingSystem):
    def __init__(self, alpha, beta):
        name = constructName(alpha=alpha, beta=beta)
        super().__init__(FirstStageFilter(),
                         [ ThresholdFilter(alpha) ],
                         [ ThresholdFilter(beta, ONLY_NULL_CANDIDATE, defaultOffset=-1)],
                         name=name)
        self.alpha = alpha
        self.beta = beta