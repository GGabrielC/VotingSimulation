from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.SecondLastStageFilter import SecondLastStageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.FirstStageFilter import FirstStageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystem import VotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots
import pandas as pd

class MyAbstractVotingSystem(VotingSystem):
    def __init__(self, winStagePicker, firstStageFilters=[], lastStageFilters=[], name="MyCustom"):
        self.winStagePicker = winStagePicker
        self.firstStageFilters = [FirstStageFilter(), *firstStageFilters]
        self.lastStageFilters = [SecondLastStageFilter(), *lastStageFilters]
        super().__init__(name)

    def _runAlgorithm(self, processedBallots:MyProcessedRankedBallots) -> dict:
        self._updateNullCandidateFilters(processedBallots.nullCandidate)
        allStages = processedBallots.dfScoreOfCandidates

        winner, winStage = processedBallots.nullCandidate, self._getNullCandidateWinStage(processedBallots)
        validStages = self._findValidStages(allStages)
        if len(validStages):
            winStage = self.winStagePicker.run(validStages)
            if type(winStage) is not int:
                print("woops")
            winner = allStages.iloc[winStage].idxmax()

        return { "winStage": winStage,
                 "winner": winner,
                 "validStages": validStages.index.values.tolist()}

    def _getNullCandidateWinStage(self, processedBallots):
        nullWinStages = []
        for sf in [self.winStagePicker, *self.firstStageFilters, *self.lastStageFilters]:
            if type(sf) is ThresholdFilter:
                allStages = processedBallots.dfScoreOfCandidates
                nullCandidate = processedBallots.nullCandidate
                nullWinStage = sf.run(allStages, candidates=[nullCandidate], offset=0)
                nullWinStages.append(nullWinStage)
        return min(nullWinStages)

    def _findValidStages(self, scoreOfCandidates):
        firstValidStageIndex = max([sf.run(scoreOfCandidates) for sf in self.firstStageFilters])
        lastValidStageIndex = min([sf.run(scoreOfCandidates) for sf in self.lastStageFilters])
        return scoreOfCandidates[firstValidStageIndex: 1+lastValidStageIndex]

    def _updateNullCandidateFilters(self, nullCandidate):
        for sf in [self.winStagePicker, *self.firstStageFilters, *self.lastStageFilters]:
            sf.nullCandidate = nullCandidate