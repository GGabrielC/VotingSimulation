from VotingSystem.VotingSystems.MyVotingSystem.MyAbstractVotingSystem import MyAbstractVotingSystem
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.EntropyFilter import EntropyFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ONLY_NULL_CANDIDATE
from VotingSystem.VotingSystems.MyVotingSystem.MyVotingSystem import constructName


class BetaGammaEntropy (MyAbstractVotingSystem):
    def __init__(self, alpha, beta, gamma):
        name = "BetaGammaEntropy <\u03B1:{}, \u03B2:{}, \u03B3:{}>".format(alpha, beta, gamma)
        super().__init__(EntropyFilter(),
                         [ ThresholdFilter(alpha) ],
                         [ ThresholdFilter(beta, ONLY_NULL_CANDIDATE, defaultOffset=-1), ThresholdFilter(gamma) ],
                         name=name)
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma