from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import StageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ALL_CANDIDATES

class FirstStageFilter(StageFilter):
    def __init__(self):
        super().__init__("First",ALL_CANDIDATES)

    def run(self, dfStages):
        if len(dfStages) == 0:
            return None
        return dfStages.index.to_list()[0]