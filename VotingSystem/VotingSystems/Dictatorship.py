from VotingSystem.VotingSystem import VotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots
from WisdomOfTheCrowds import CrowdMember

class Dictatorship(VotingSystem):
    def __init__(self, dictator:CrowdMember, name="Dictator Hitler"):
        self.dictator = dictator
        super().__init__(name=name)

    def _runAlgorithm(self, processedBallots: MyProcessedRankedBallots) -> dict:
        ballot = self.dictator.voteRanked(**processedBallots.source)
        return {"winner": ballot[0], "algorithm": self.name}