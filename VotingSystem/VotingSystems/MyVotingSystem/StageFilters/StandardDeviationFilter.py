from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import StageFilter
from statistics import stdev
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ALL_CANDIDATES

def minVariance(dfStages):
    return dfStages.apply(lambda x: stdev(x), axis=1).idxmin()
def maxVariance(dfStages):
    return dfStages.apply(lambda x: stdev(x), axis=1).idxmax()

class StandardDeviationFilter(StageFilter):
    def __init__(self, highest=True):
        namePrefix = 'Max' if highest else 'Min'
        self.method = minVariance if highest else maxVariance
        super().__init__(namePrefix+'StDev', ALL_CANDIDATES)

    def run(self, dfStages):
        if len(dfStages) == 0:
            return None
        return self.method(dfStages)
