from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import StageFilter
from statistics import variance
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ALL_CANDIDATES

def minVariance(dfStages):
    return dfStages.apply(lambda x: variance(x), axis=1).idxmin()
def maxVariance(dfStages):
    return dfStages.apply(lambda x: variance(x), axis=1).idxmax()

class VarianceFilter(StageFilter):
    def __init__(self, highest=True):
        namePrefix = 'Max' if highest else 'Min'
        self.method = minVariance if highest else maxVariance
        super().__init__(namePrefix+'Variance', ALL_CANDIDATES) #\u03C3\u00b2

    def run(self, dfStages):
        if len(dfStages) == 0:
            return None
        return self.method(dfStages)
