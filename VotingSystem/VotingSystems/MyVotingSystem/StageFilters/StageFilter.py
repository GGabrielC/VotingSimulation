from abc import ABC, abstractmethod

ALL_CANDIDATES = object()
ONLY_NULL_CANDIDATE = object()
NULL_CANDIDATE_PLACEHOLDER = None

class StageFilter(ABC):
    def __init__(self, name, defaultCandidates=ALL_CANDIDATES, defaultOffset=0):
        self.name = name
        if not (defaultCandidates is ALL_CANDIDATES or defaultCandidates is ONLY_NULL_CANDIDATE):
            raise Exception("Only ONLY_NULL_CANDIDATE and ALL_CANDIDATES accepted !")
        self.defaultCandidates = defaultCandidates
        self.nullCandidate = NULL_CANDIDATE_PLACEHOLDER
        self.defaultOffset = defaultOffset

    @abstractmethod
    def run(self, dfStages):
        pass