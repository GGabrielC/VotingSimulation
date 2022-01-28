from abc import ABC, abstractmethod
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots

class VotingSystem(ABC):
    def __init__(self, name):
        self.name = name

    def run(self, processedBallots=None, ballots=None, nullCandidateID=None):
        if processedBallots is None:
            processedBallots = MyProcessedRankedBallots(ballots, nullCandidateID)
        self.processedBallots = processedBallots
        results = self._runAlgorithm(processedBallots)
        results = {
            **results,
            'algorithm': self.name,
        }
        return results

    @abstractmethod
    def _runAlgorithm(self, processedBallots:MyProcessedRankedBallots) -> dict:
        pass

