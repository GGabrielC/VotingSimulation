from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import StageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ALL_CANDIDATES

class ThresholdFilter(StageFilter):
    def __init__(self, threshold, defaultCandidates=ALL_CANDIDATES, defaultOffset=0):
        super().__init__("Threshold", defaultCandidates, defaultOffset)
        self.threshold = threshold

    def run(self, dfStages, candidates=None, offset=None):
        if len(dfStages) == 0:
            return None
        if candidates is None:
            candidates = dfStages.columns.to_list() if self.defaultCandidates is ALL_CANDIDATES else [self.nullCandidate]
        offset = self.defaultOffset if offset is None else offset
        return offset + dfStages[dfStages[candidates].apply(lambda r: (r>self.threshold).any(), axis=1)].index.to_list()[0]
