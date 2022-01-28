from VotingSystem.VotingSystem import VotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots
from pyrankvote import Candidate, Ballot, instant_runoff_voting

class InstantRunoffVoting(VotingSystem):
    def __init__(self):
        super().__init__(name="InstantRunoffVoting")

    def _runAlgorithm(self, processedBallots: MyProcessedRankedBallots) -> dict:
        candidates = [Candidate(c) for c in processedBallots.candidates]
        ballots = [Ballot(ranked_candidates=[Candidate(c) for c in b]) for b in processedBallots.ballots]
        election_result = instant_runoff_voting(candidates, ballots)
        winner = election_result.get_winners()[0].name
        return {"winner":winner}