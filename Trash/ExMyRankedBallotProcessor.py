
class MyProcessedRankedBallots:
    def __init__(self, ballots, nullCandidateID):
        self.ballots = ballots
        self.nullCandidateID = nullCandidateID
        self.numberOfCandidates = len(self.ballots[0])
        self.numberOfVoters = len(self.ballots)

        self.candidateCodes = list(range(self.numberOfCandidates))
        self.candidateIDs = self.candidateCodes if set(self.candidateCodes) == set(self.ballots[0]) else self.ballots[0]
        self.candidateMappingsCodeToId = {cCode: cid for cCode, cid in zip(self.candidateCodes, self.candidateIDs)}
        self.candidateMappingsIdToCode = {v: k for k, v in self.candidateMappingsCodeToId.items()}

        self.ballots = [[self.candidateMappingsIdToCode[id] for id in ballot] for ballot in ballots]
        self.nullCandidateCode = self.candidateMappingsIdToCode[self.nullCandidateID]

        self.stampCounts = self.findStampCounts()
        self.processedVoteCounts = self.findProcessedVoteCounts()
        self.scoreOfCandidates = self.findScoreOfCandidates()

    def findStampCounts(self):
        stampCounts = [[0] * self.numberOfCandidates for i in range(self.numberOfCandidates)]
        for ballot in self.ballots:
            for preference in range(self.numberOfCandidates):
                candidate = ballot[preference]
                stampCounts[preference][candidate] += 1
        return stampCounts

    def findProcessedVoteCounts(self):
        processedVoteCounts = [row[:] for row in self.stampCounts]
        prevStage = processedVoteCounts[0]
        for stage in processedVoteCounts[1:]:
            for i in range(len(stage)):
                stage[i] += prevStage[i]
            prevStage = stage
        return processedVoteCounts

    def findScoreOfCandidates(self):
        scoreOfCandidates = [stage[:] for stage in self.processedVoteCounts]
        for i in range(len(scoreOfCandidates)):
            for j in range(len(scoreOfCandidates[0])):
                scoreOfCandidates[i][j] = (100 * scoreOfCandidates[i][j]) / self.numberOfVoters
        return scoreOfCandidates