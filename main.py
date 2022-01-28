from VotingSimulations.RealisticVotingSimulation import RealisticVotingSimulation
from VotingSystem.VotingSystems.MyVotingSystem.MyVotingSystem import MyVotingSystem
from VotingSystem.VotingSystems.PreferentialBlockVoting import PreferentialBlockVoting
from VotingSystem.VotingSystems.InstantRunoffVoting import InstantRunoffVoting
from VotingSystem.VotingSystems.SingleTransferableVote import SingleTransferableVote
from VotingSystem.VotingSystems.FirstPastThePost import FirstPastThePost
from VotingSystem.VotingSystems.MaxVarianceWeightedSumWins import MaxVarianceWeightedSumWins
from VotingSystem.VotingSystems.MinEntropyWeightedSumWins import MinEntropyWeightedSumWins
from VotingSystem.VotingSystems.MinEntropyWeightedSumWins2 import MinEntropyWeightedSumWins2
from VotingSystem.VotingSystems.MaxStandardDeviationWeightedSumWins import MaxStandardDeviationWeightedSumWins
from VotingSystem.VotingSystems.MaxStandardDeviationProportionalWeightedSumWins import MaxStandardDeviationProportionalWeightedSumWins
from VotingSystem.VotingSystems.MinEntropyProportionalWeightedSumWins2 import MinEntropyProportionalWeightedSumWins2
from VotingSystem.VotingSystems.MinEntropyProportionalWeightedSumWins import MinEntropyProportionalWeightedSumWins
from VotingSystem.VotingSystems.MaxVarianceProportionalWeightedSumWins import MaxVarianceProportionalWeightedSumWins
from DataHelpers import DataGenerator
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import os.path

def getVotingSystems():
    pass
def createSyntheticDataset():
    pass
def getOutputFiles():
    pass

def main():
    outDataFrame, outDetails = getOutputFiles()
    crowdBuildMethod = "standardDistribution" # "standardDistribution" "thresholdValMSE" None
    rvs = RealisticVotingSimulation(datasetName="mySynthetic", numVoters=750, numCandidates=20, epochs=166,
                                    trainableLayerCount=1, columnBlindness=5, crowdBuildMethod=crowdBuildMethod,
                                    outsDetails=[outDetails])
    results = rvs.run(getVotingSystems(), numElections=750)

    with open(outDetails, 'a', encoding="utf-8") as file:
        strResults = "========= SIMULATION RESULTS ========\n{}\n".format(results.to_string())
        print(strResults)
        print(strResults, file=file)
        results.to_csv(outDataFrame, encoding="utf-8")
        print("File outputs:", outDataFrame, outDetails)

def getOutputFiles():
    i=1
    outTemplate = "Results/Results{}.{}"
    while True:
        outDataFrame, outDetails = outTemplate.format(i, "csv"), outTemplate.format(i, "txt")
        if not(os.path.isfile(outDataFrame) or os.path.isfile(outDetails)):
            print("To be used:", outDataFrame, outDetails)
            return outDataFrame, outDetails
        i+=1

def createSyntheticDataset():
    DataGenerator.generate(3000, 11, 'Data/MySyntheticDataset.csv')
    df = pd.read_csv('Data/MySyntheticDataset.csv')
    s = df.loc[:, "y"]
    ax = s.hist(bins=20)
    fig = ax.get_figure()
    fig.savefig('Data/figure.pdf')
    s.hist()
    plt.savefig('Data/figure.pdf')

def getVotingSystems():
    alphaPool = [0.5, 0.66, 0.8]
    betaPool = [None, 0.33]
    gammaPool = [None, 0.66, 0.8]
    winStagePickers = ["first", "last", "min_entropy", "max_entropy", "min_variance", "max_variance", "max_stdev"]
    pool = [alphaPool, betaPool, gammaPool, winStagePickers]
    votingSystems = [
        InstantRunoffVoting(),
        SingleTransferableVote(),
        PreferentialBlockVoting(),
        FirstPastThePost(),

        *[MyVotingSystem(a, b, g, p) for a, b, g, p in itertools.product(*pool) if g is None or a < g],

        MinEntropyWeightedSumWins(alpha=0),
        MinEntropyWeightedSumWins(alpha=0.5),
        MinEntropyWeightedSumWins2(alpha=0),
        MinEntropyWeightedSumWins2(alpha=0.5),
        MaxVarianceWeightedSumWins(alpha=0),
        MaxVarianceWeightedSumWins(alpha=0.5),
        MaxStandardDeviationWeightedSumWins(alpha=0),
        MaxStandardDeviationWeightedSumWins(alpha=0.5),

        MinEntropyProportionalWeightedSumWins(alpha=0),
        MinEntropyProportionalWeightedSumWins(alpha=0.5),
        MinEntropyProportionalWeightedSumWins2(alpha=0),
        MinEntropyProportionalWeightedSumWins2(alpha=0.5),
        MaxVarianceProportionalWeightedSumWins(alpha=0),
        MaxVarianceProportionalWeightedSumWins(alpha=0.5),
        MaxStandardDeviationProportionalWeightedSumWins(alpha=0),
        MaxStandardDeviationProportionalWeightedSumWins(alpha=0.5),
    ]
    return votingSystems

if __name__ == "__main__":
    #createSyntheticDataset()
    #RandomVotingSimulation().run()
    main()