from WisdomOfTheCrowds.CrowdBuilder import CrowdBuilder
from DataHelpers.SimulationData import SimulationData
import pandas as pd
import numpy as np
from collections import defaultdict
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots
from VotingSystem.VotingSystems.Dictatorship import Dictatorship
from VotingSystem.VotingSystems.CrowdMetric import CrowdMetric
from math import sqrt
import matplotlib.pyplot as plt

class PerformanceKeeper():
    def __init__(self):
        self.__info = defaultdict(int)
        self.settled = False

    def add(self, results, evalVS):
        if self.settled:
            raise Exception("Settled!")
        self.__info[results["algorithm"], "rateTrueWinners"] += evalVS["winnerIsBest"]
        self.__info[results["algorithm"], "meanWinnerRank"] += evalVS["winnerRank"]
        self.__info[results["algorithm"], "rateWinner<NULL"] += evalVS["rateWinner<NULL"]

    def settle(self, toDivideWith):
        self.settled = True
        for key in self.__info:
            self.__info[key] /= toDivideWith

    def toDataFrame(self):
        if not self.settled:
            raise Exception("Not settled yet!")
        algorithms = list(set(k[0] for k in self.__info.keys()))
        colNames = list(set(k[1] for k in self.__info.keys()))
        data = [[self.__info[a,c] for c in colNames] for a in algorithms]
        df = pd.DataFrame(data=data, columns=colNames, index=algorithms)
        orderedColumns = ["meanWinnerRank", "rateTrueWinners", "rateWinner<NULL"]
        df = df[orderedColumns]
        df = df.sort_values(by=orderedColumns, ascending=[True,False,True])
        df.index.name = "Algorithms"
        df.columns.name = "Metrics"
        return df

    def __str__(self):
        return self.toDataFrame().to_string()

class RealisticVotingSimulation:
    def __init__(self, datasetName, numVoters=7, numCandidates=7, epochs=1,
                 trainableLayerCount=11, columnBlindness=0, crowdBuildMethod=None, outsDetails=None,
                 addCrowdAndBestVoterAsVotingSystems=True, nullCandidateQuantileScore=0.5):
        self.numCandidates = numCandidates
        self.numVoters = numVoters
        self.epochs = epochs
        self.trainableLayerCount = trainableLayerCount
        self.columnBlindness = columnBlindness
        self.setData(datasetName)
        self.setCrowdBuildMethod(crowdBuildMethod)
        self.electionCount = 0
        outsDetails = [None] if outsDetails is None else outsDetails
        self.outsDetails = {None, *outsDetails}
        self.addCrowdAndBestVoterAsVotingSystems = addCrowdAndBestVoterAsVotingSystems
        self.nullCandidateQuantileScore = nullCandidateQuantileScore

    def _putSimulationResultsToDataFrame(self):
        strValMSE = 'val_Mean²Err'
        dfSimulationResults = self._performances.toDataFrame()
        if self.addCrowdAndBestVoterAsVotingSystems:
            dfSimulationResults.loc[self.dictatorship.name, strValMSE] = self.bestVoter.trainResults['val_mean_squared_error']
            dfSimulationResults.loc[self.crowdMean.name, strValMSE] = self.crowdValMSE_mean
            dfSimulationResults.loc[self.crowdMedian.name, strValMSE] = self.crowdValMSE_median
        return dfSimulationResults

    def run(self, votingSystems, numElections=1):
        self.numeElectionsToBeMade = numElections
        self._setVoters(self.numVoters)
        if self.addCrowdAndBestVoterAsVotingSystems:
            self._addCrowdAndBestVoterAsVotingSystems(votingSystems)
        self._performances = PerformanceKeeper()
        self._anyMyVotingSystem = self._lastInstanceResultsVSs = None

        print("Running Elections !")
        for _ in range(numElections):
            self._runElection(votingSystems)
        print("Elections Ended !")
        self._printStuff()
        self._performances.settle(toDivideWith=numElections)
        return self._putSimulationResultsToDataFrame()

    def _runElection(self, votingSystems):
        self._setElectionContext()
        for vs in votingSystems:
            resultsVS = vs.run(self.processedBallots)
            self._lastInstanceResultsVSs.append(resultsVS)
            evalVS = self._evaluateElectionResults(resultsVS, self._dfCandidates, self._bestCandidate)
            self._performances.add(resultsVS, evalVS)

    def _evaluateElectionResults(self, resultsVotingSystem, dfCandidates, bestCandidate):
        winnerID = resultsVotingSystem["winner"]
        winner = dfCandidates[dfCandidates.index == winnerID].iloc[0, :]
        winnerIsBest = bestCandidate.equals(winner)
        candidates = [(index, row[self.yName]) for index, row in dfCandidates.iterrows()]
        candidates.sort(key=lambda x: x[1], reverse=True)
        winnerRank = [1 + i for i in range(len(candidates)) if candidates[i][0] == winnerID][0]
        winnerIsWorseThanNull = winner[self.yName] < self.nullCandidateScore
        return {"winnerIsBest": winnerIsBest, "winnerRank": winnerRank, "rateWinner<NULL": winnerIsWorseThanNull}

    def _setElectionContext(self):
        self.electionCount += 1
        if self.electionCount%5 == 0 or self.electionCount==1:
            print("Starting {}th/{} election".format(self.electionCount, self.numeElectionsToBeMade))
        self._lastInstanceResultsVSs = []
        self._setCandidates()
        params = [self._dfNonNullCandidatesInput, self.nullCandidateScore, self.nullCandidateIdx]
        self._ballots = self.voters.voteRankedIndividuals(*params)
        bestCandidateScore = self._dfCandidates[self.yName].max()
        self._bestCandidate = self._dfCandidates[self._dfCandidates[self.yName] == bestCandidateScore].iloc[0, :]
        source = {"dfNonNullCandidates": self._dfNonNullCandidatesInput,
                    "nullCandidateScore": self.nullCandidateScore,
                    "nullCandidateID": self.nullCandidateIdx}
        self.processedBallots = MyProcessedRankedBallots(self._ballots, nullCandidate=self.nullCandidateIdx, source=source)

    def _addCrowdAndBestVoterAsVotingSystems(self, votingSystems):
        self.dictatorship = Dictatorship(self.bestVoter, name="bestVoter (Dictatorship)")
        self.crowdMean = CrowdMetric(self.voters, np.mean)
        self.crowdMedian = CrowdMetric(self.voters, np.median)
        votingSystems.extend([self.dictatorship, self.crowdMean, self.crowdMedian])

    def _printStuff(self):
        for outDetails in self.outsDetails:
            file = outDetails if outDetails is None else open(outDetails, 'a', encoding="utf-8")
            dfLastInstanceResults = pd.DataFrame(self._lastInstanceResultsVSs).set_index("algorithm")
            plt.close()
            plt.hist([round(m.trainResults["val_mean_squared_error"],2) for m in self.voters])
            plt.savefig("VotersMeanSquaredErr")
            plt.close()
            plt.hist([round(sqrt(m.trainResults["val_mean_squared_error"]), 2) for m in self.voters])
            plt.savefig("VotersMeanErr")
            print("\n===== Last Election voting process ======\n", file=file)
            print(self.processedBallots.getTablesAsString(), file=file)
            print(dfLastInstanceResults.to_string(),"\n", file=file)
            print("Last Election Candidates:\n{}\n".format(
                self._dfCandidates[[self.yName]].sort_values(by=[self.yName]).to_string()), file=file)
            print("Voters Validation Mean Squared Error:\n{}\n".format(
                [round(m.trainResults["val_mean_squared_error"],2) for m in self.voters]), file=file)
            print("Voters Validation Mean Error:\n{}\n".format(
                [round(sqrt(m.trainResults["val_mean_squared_error"]), 2) for m in self.voters]), file=file)
            [print(k,":",v, file=file) for k,v in self.getHyperparameters().items()]
            print("", file=file)
            if file is not None:
                file.close()

    def setNullCandidate(self):
        q = self.nullCandidateQuantileScore
        self.nullCandidateIdx = "NullCandidate"
        self.nullCandidateScore = pd.Series(list(set(self.sData.allY().iloc[:, 0].tolist()))).quantile(q)
        self.nullCandidate = pd.Series(data={self.yName: self.nullCandidateScore},
                                       index=[self.yName], name=self.nullCandidateIdx)

    def _setCandidates(self):
        self.setNullCandidate()
        self._dfNonNullCandidatesInput = self.sData.df_test_x.sample(n=self.numCandidates-1)
        _dfNonNullCandidates = self.sData.dfTest().loc[self._dfNonNullCandidatesInput.index]
        self._dfCandidates = _dfNonNullCandidates.append(self.nullCandidate)
        self._dfCandidates.index.name = "Candidates"

    def setData(self, datasetName):
        self.dataInfo = SimulationData.getDataInfo(datasetName)
        params = {i: self.dataInfo[i] for i in self.dataInfo if i in ['filePaths', 'yName', 'delimiter', 'needsToBeBalanced']}
        self.sData = SimulationData.getData(**params, test_size=0.3)
        self.yName = self.dataInfo["yName"]

    def _setVoters(self, numVoters):
        crowdBuilder = CrowdBuilder(epochs=self.epochs, trainableLayerCount=self.trainableLayerCount,
                                    method=self.crowdBuildMethod, maxOutput=self.dataInfo['maxOutput'],
                                    columnBlindness=self.columnBlindness,)
        self.voters, (self.crowdValMSE_mean, self.crowdValMSE_median) = \
                        crowdBuilder.buildCrowd(splittedData=self.sData, size=numVoters)
        self.numVoters = len(self.voters)
        self.bestVoter = self.voters.getBestMemberByValMSE()

    def setCrowdBuildMethod(self, method):
        if method == "thresholdValMSE":
            self.crowdBuildMethod = {"name":method,   "bestMSE":self.dataInfo["bestWantedValMSE"][self.yName],
                                            "worstMSE":self.dataInfo["worstWantedValMSE"][self.yName],}
        elif method == "standardDistribution":
            self.crowdBuildMethod = {"name":method,   "mean":self.dataInfo["wantedMeanValMSE"][self.yName],
                                            "standardDeviation":self.dataInfo["wantedStDevValMSE"][self.yName],}
        elif method is None:
            self.crowdBuildMethod = None

    def getHyperparameters(self):
        return {
            "numCandiates": self.numCandidates,
            "numVoters": self.numVoters,
            "numElections": self.numeElectionsToBeMade,
            "columnBlindness": self.columnBlindness,
            "epochs": self.epochs,
            "trainableLayerCount": self.trainableLayerCount,
            "crowdBuildMethod": self.crowdBuildMethod,
            "dataSetName": self.dataInfo["dataSetName"],
            "predictedFeature": self.yName,
        }