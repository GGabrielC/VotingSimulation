import pandas as pd
import numpy as np

class MyProcessedRankedBallots:
    def __init__(self, ballots, nullCandidate, source=None):
        self.source = source
        self.ballots = ballots
        self.nullCandidate = nullCandidate
        self.numberOfCandidates = len(self.ballots[0])
        self.numberOfVoters = len(self.ballots)
        self.candidates = self.ballots[0]

        self.dfStampCounts = self.findStampCounts()
        self.dfProcessedVoteCounts = self.findProcessedVoteCounts()
        self.dfScoreOfCandidates = self.findScoreOfCandidates()
        self.sortColumnsFromTables()

    def getTablesAsString(self):
        return "Stamp Counts Table:\n{}\n\nProcessed Vote Counts Table:\n{}\n\nScore(%) of Candidates Table:\n{}\n".format(
            self.dfStampCounts.to_string(),
            self.dfProcessedVoteCounts.to_string(),
            (100 * self.dfScoreOfCandidates).to_string()
        )

    def sortColumnsFromTables(self):
        stages = list(reversed(self.dfScoreOfCandidates.index.values.tolist()))
        self.dfScoreOfCandidates = self.dfScoreOfCandidates.sort_values(by=stages, axis=1, ascending=False)
        sortedCandidates = self.dfScoreOfCandidates.columns.values.tolist()
        self.dfProcessedVoteCounts = self.dfProcessedVoteCounts[sortedCandidates]
        self.dfStampCounts = self.dfStampCounts[sortedCandidates]

    def findStampCounts(self):
        data = np.zeros((self.numberOfCandidates,self.numberOfCandidates), dtype=int)
        dfStampCounts = pd.DataFrame(data, columns=self.candidates)
        dfStampCounts.index.name = 'Preference'
        dfStampCounts.columns.name = 'Candidates'
        for ballot in self.ballots:
            for preference in range(self.numberOfCandidates):
                candidate = ballot[preference]
                dfStampCounts[candidate][preference] += 1
        return dfStampCounts

    def findProcessedVoteCounts(self):
        dfProcessedVoteCounts = self.dfStampCounts.cumsum(axis=0)
        dfProcessedVoteCounts.index.name = 'Stage'
        return dfProcessedVoteCounts

    def findScoreOfCandidates(self):
        return self.dfProcessedVoteCounts / self.numberOfVoters