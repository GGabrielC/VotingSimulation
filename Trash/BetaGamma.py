from VotingSystem.VotingSystems.MyVotingSystem.MyAbstractVotingSystem import MyAbstractVotingSystem
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.LastStageFilter import LastStageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ONLY_NULL_CANDIDATE
from VotingSystem.VotingSystems.MyVotingSystem.MyVotingSystem import constructName


class BetaGamma (MyAbstractVotingSystem):
    def __init__(self, alpha, beta, gamma):
        name = "BetaGamma <\u03B1:{}, \u03B2:{}, \u03B3:{}>".format(alpha, beta, gamma)
        super().__init__(LastStageFilter(),
                         [ ThresholdFilter(alpha) ],
                         [ ThresholdFilter(beta, ONLY_NULL_CANDIDATE, defaultOffset=-1), ThresholdFilter(gamma) ],
                         name=name)
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma