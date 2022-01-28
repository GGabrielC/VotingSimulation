from VotingSystem.VotingSystem import VotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots

class FirstPastThePost(VotingSystem):
    def __init__(self):
        super().__init__(name="FirstPastThePost (but without tactical voting)")

    def _runAlgorithm(self, processedBallots: MyProcessedRankedBallots) -> dict:
        return {"winner": processedBallots.dfProcessedVoteCounts.iloc[0].idxmax()}