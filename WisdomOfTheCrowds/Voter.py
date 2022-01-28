from abc import ABC, abstractmethod
import pandas as pd

class Voter(ABC):
    def voteRanked(self, dfNonNullCandidates:pd.DataFrame, nullCandidateScore, nullCandidateID):
        scores = list(self.predict(x=dfNonNullCandidates))
        scores.insert(0, nullCandidateScore)
        candidatesIDs = [nullCandidateID, *dfNonNullCandidates.index.values]
        scores = list(zip(candidatesIDs, scores))
        scores.sort(key=lambda x: x[1], reverse=True)
        ballot = [id for id, score in scores]
        return ballot

    @abstractmethod
    def predict(x):
        pass