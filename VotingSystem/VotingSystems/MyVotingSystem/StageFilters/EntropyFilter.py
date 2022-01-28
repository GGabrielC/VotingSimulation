from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import StageFilter
from scipy.stats import entropy
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ALL_CANDIDATES
import pandas as pd

def minEntropy(dfStages:pd.DataFrame):
    return dfStages.idxmin()
def maxEntropy(dfStages:pd.DataFrame):
    return dfStages.idxmax()

class EntropyFilter(StageFilter):
    def __init__(self, lowest=True):
        namePrefix = 'Min' if lowest else 'Max'
        self.method = minEntropy if lowest else maxEntropy
        super().__init__(namePrefix+'Entropy', ALL_CANDIDATES)

    def run(self, dfStages:pd.DataFrame):
        if len(dfStages) == 0:
            return None
        return self.method(self.entropiesPerRow(dfStages)) # return self.method(dfStages/(1+dfStages.index.values[-1]))

    def entropiesPerRow(self, dfStages:pd.DataFrame):
        return dfStages.apply(lambda x: entropy(x, base=2), axis=1)

    # def entropiesPerRow(self, dfStages:pd.DataFrame):
        # dfStages_SumTo1 = dfStages.div (dfStages.sum(axis=1), axis=0)
        # return dfStages_SumTo1.apply(lambda x: entropy(x, base=2), axis=1)