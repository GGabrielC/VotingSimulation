import random
from VotingSystem.VotingSystems.MyVotingSystem.MyAbstractVotingSystem import MyAbstractVotingSystem as MRVS
from VotingSystem.VotingSystems.MyVotingSystem.MyVotingSystem import MyVotingSystem
from VotingSystem.Helper.MyRankedBallotProcessor import MyProcessedRankedBallots

def getRandomBallot(candidates):
    rawBallot = candidates[:]
    random.shuffle(rawBallot)
    return tuple(rawBallot)

class RandomVotingSimulation:
    def __init__(self, numberOfVoters=16, numberOfCandidates=8, alpha=0.5, beta=0.3333, gamma=0.6666):
        self.setHyperparameters(numberOfVoters=numberOfVoters, numberOfCandidates=numberOfCandidates,
                                alpha=alpha, beta=beta, gamma=gamma)
        self.countSimulationAttempts = 0

    def simulate(self):
        self.countSimulationAttempts += 1
        candidates = list(range(self.numberOfCandidates))
        ballots = [getRandomBallot(candidates) for i in range(self.numberOfVoters)]
        self.prb = MyProcessedRankedBallots(ballots=ballots, nullCandidate=0)

        self.vsBasic = MyVotingSystem(self.alpha)
        self.vsBeta = MyVotingSystem(self.alpha, self.beta)
        self.vsBetaG = MyVotingSystem(self.alpha, self.beta, self.gamma)
        self.vsBetaGE = MyVotingSystem(self.alpha, self.beta, self.gamma, "MinEntropy")

        self.resultsBasic = self.vsBasic.run(self.prb)
        self.resultsBeta = self.vsBeta.run(self.prb)
        self.resultsBetaGamma = self.vsBetaG.run(self.prb)
        self.resultsBetaGammaEntropy = self.vsBetaGE.run(self.prb)

        self.algorithmsResults = [self.resultsBasic, self.resultsBeta, self.resultsBetaGamma, self.resultsBetaGammaEntropy]

    def run(self):
        while (not self.getSatisfactionOfGeneratedBallots()):
            self.simulate()
            if self.countSimulationAttempts%50 == 0:
                print("Simulation Attempts made:", self.countSimulationAttempts, set(r['winner'] for r in self.algorithmsResults))
        MRVS.displayDetailsAssumingSameTables(self.prb, self.algorithmsResults)

    def getSatisfactionOfGeneratedBallots(self):
        if self.countSimulationAttempts == 0:
            return False

        # winners = set(r['winner'] for r in self.algorithmsResults)
        # if len(winners) != len(self.algorithmsResults):
        #     return False

        # for r in self.algorithmsResults:
        #      if r['winner'] == self.prb.nullCandidate:
        #          return False

        return True

    def setHyperparameters(self, numberOfVoters=16, numberOfCandidates=8, alpha=0.5, beta=0.3333, gamma=0.6666):
        self.numberOfVoters = numberOfVoters
        self.numberOfCandidates = numberOfCandidates
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
