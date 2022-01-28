from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import StageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ALL_CANDIDATES

class SecondLastStageFilter(StageFilter):
    def __init__(self, offset=0):
        super().__init__("Last", ALL_CANDIDATES, offset)

    def run(self, dfStages):
        if len(dfStages) == 0:
            return None
        return dfStages.index.to_list()[-2]