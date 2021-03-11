import random

def prettyPrintRow(row, collumnLength, rowName="r"):
    getPrefix = lambda item: " " * (collumnLength-len(str(item)))
    output = getPrefix(rowName) + rowName
    for i in row:
        output+= getPrefix(i) + str(i)
    print(output)

def prettyPrintTable(table, name="Table", rowName="", itemSuffix=""):
    print(name)
    table = [row[:] for row in table]
    highestNumber = max([i for row in table for i in row])
    collumnLength = len(str(highestNumber))+2+len(itemSuffix)
    
    prettyPrintRow(range(len(table[0])), collumnLength, rowName="")
    if itemSuffix=="%":
        table = [list(map( lambda i: "{:.2f}".format(i), row)) for row in table]
    table = [list(map( lambda i: str(i)+itemSuffix, row)) for row in table]
    [prettyPrintRow(row, collumnLength, rowName+str(i)) for row,i in zip(table, range(len(table)))]
    print()

def getRandomBallot(candidates):
    rawBallot = candidates[:]
    random.shuffle(rawBallot)
    return tuple(rawBallot)

def getStampCounts(ballots, candidates):
    stampCounts = [[0] * len(candidates) for i in range(len(candidates))]
    for ballot in ballots:
        for preference in range(len(candidates)):
            candidate = ballot[preference]
            stampCounts[ preference][candidate] += 1 
    return stampCounts
    
def getProcessedVoteCounts(stampCounts):
    processedVoteCounts = [row[:] for row in stampCounts]
    prevStage = processedVoteCounts[0]
    for stage in processedVoteCounts[1:]:
        for i in range(len(stage)):
            stage[i] += prevStage[i]
        prevStage = stage
    return processedVoteCounts
    
def getScoreOfCandidates(processedVoteCounts, numberOfVoters ):
    scoreOfCandidates = [stage[:] for stage in processedVoteCounts]
    for i in range(len(scoreOfCandidates)):
        for j in range(len(scoreOfCandidates[0])):
            scoreOfCandidates[i][j] = (100*scoreOfCandidates[i][j]) / numberOfVoters
    return scoreOfCandidates
    
def getWinnerByBasic(scoreOfCandidates, alpha):
    threshold = 100*alpha
    
    stageNum = -1
    for stage in scoreOfCandidates:
        stageNum += 1
        maxScore = max(stage)
        if maxScore <= threshold:
            continue
        timesPresent = stage.count(maxScore)
        if timesPresent == 1:
            return {
                'algorithm': 'basic',
                'winner': stage.index(maxScore),
                'score': maxScore, 
                'stage': stageNum,}
        
def getWinnerByBetaGamma(scoreOfCandidates, alpha, beta, gamma):
    # we assume: 0 < beta < alpha < gamma < 1
    # we assume: NULLCandidate to be candidate 0
    # we assume: no two candidates have equal score
    # we assume: no threshold will be passed at first stage
    NULLCandidate = 0
    thresholdA = 100* alpha
    thresholdB = 100* beta
    thresholdG = 100* gamma
    
    lastStageByBeta = next(filter(lambda stage: stage[NULLCandidate]>thresholdB, scoreOfCandidates))
    lastStageByBetaIndex = -1 +scoreOfCandidates.index(lastStageByBeta)
    bestScoreByBeta = max(scoreOfCandidates[lastStageByBetaIndex])
    
    lastStageByGamma = next(filter(lambda stage: max(stage)>thresholdG, scoreOfCandidates))
    lastStageByGammaIndex = scoreOfCandidates.index(lastStageByGamma)
    bestScoreByGamma = max(lastStageByGamma)
    
    firstStageByAlpha = next(filter(lambda stage: max(stage)>thresholdA, scoreOfCandidates))
    firstStageByAlphaIndex = scoreOfCandidates.index(firstStageByAlpha)
    firstBestScoreByAlpha = max(firstStageByAlpha)
    
    lastStageIndex = min(lastStageByBetaIndex, lastStageByGammaIndex)
    lastStage = scoreOfCandidates[lastStageIndex]
    lastStageMaxScore = max(lastStage)
    lastStageCandidate = lastStage.index(lastStageMaxScore)
    
    winner = lastStageCandidate if lastStageMaxScore > thresholdA else NULLCandidate
    return {
        'algorithm': "BetaGamma",
        'NULLCandidate': NULLCandidate,
        'winner': winner,
        'bestCandidate':  lastStageCandidate,
        'bestScore':      lastStageMaxScore, 
        'bestScoreStage': lastStageIndex,
        'lastStageByBeta': lastStageByBetaIndex,
        'bestScoreByBeta': bestScoreByBeta,
        'lastStageByGamma': lastStageByGammaIndex,
        'bestScoreByGamma': bestScoreByGamma,
        'firstStageByAlpha': firstStageByAlphaIndex,
        'bestScoreByAlpha':  firstBestScoreByAlpha,}
    
def displayInfo(infoToShow, hyperParameters, results):
    infoToShowTemplate = "".join(map( lambda i: i+": {"+i+"}\n", infoToShow))
    dataToDisplay = hyperParameters.copy()
    dataToDisplay.update(results)
    print(infoToShowTemplate.format(**dataToDisplay))

def getSatisfactionOfGeneratedBallots(resultsBasic, resultsBetaGamma, scoreOfCandidates):
    criticalStages = set([
        resultsBetaGamma['firstStageByAlpha'],
        resultsBetaGamma['lastStageByBeta'],
        resultsBetaGamma['lastStageByGamma'],])
    #if len(criticalStages) != 3):
    #    return False
    #if resultsBetaGamma['winner'] == resultsBetaGamma['NULLCandidate']:
    #    return False
    #if 0 != scoreOfCandidates[0][resultsBetaGamma['winner']]:
    #    return False
    bestStage = scoreOfCandidates[resultsBetaGamma['bestScoreStage']]
    if bestStage.count(max(bestStage))>1:
        return False
    bestStage = scoreOfCandidates[resultsBasic['stage']]
    if bestStage.count(max(bestStage))>1:
        return False
        
    return True

def main():
    numberOfVoters = 16
    numberOfCandidates = 8
    alpha = 0.5
    beta = 0.3333
    gamma = 0.6666
    
    hyperParameters = {
        'numberOfVoters': numberOfVoters,
        'numberOfCandidates' : numberOfCandidates,
        'alpha' : alpha, 'beta' : beta, 'gamma' : gamma,}
    
    satisfiedWithGeneratedBallots = False
    while (not satisfiedWithGeneratedBallots):
        candidates = list(range(numberOfCandidates))
        ballots = [getRandomBallot(candidates) for i in range(numberOfVoters)]
        
        stampCounts = getStampCounts(ballots, candidates)
        processedVoteCounts = getProcessedVoteCounts(stampCounts)
        scoreOfCandidates = getScoreOfCandidates(processedVoteCounts, numberOfVoters)
        
        resultsBasic = getWinnerByBasic(scoreOfCandidates, alpha)
        resultsBetaGamma = getWinnerByBetaGamma(scoreOfCandidates, alpha, beta, gamma)
        
        satisfiedWithGeneratedBallots = getSatisfactionOfGeneratedBallots(
            resultsBasic, resultsBetaGamma, scoreOfCandidates)
        if(satisfiedWithGeneratedBallots):
            prettyPrintTable(stampCounts, name="Stamp Counts Table:")
            prettyPrintTable(processedVoteCounts, name="Processed Vote Counts Table:")
            prettyPrintTable(scoreOfCandidates, name="Score of Candidates Table:", itemSuffix="%")
            displayInfo(
                infoToShow = ["algorithm", "winner", "stage", "score", "alpha"],
                results = resultsBasic, hyperParameters = hyperParameters)
            displayInfo( infoToShow = ['algorithm', 'NULLCandidate', 'winner',
                'bestCandidate', 'bestScore', 'bestScoreStage',
                'lastStageByBeta', 'bestScoreByBeta',
                'lastStageByGamma', 'bestScoreByGamma',
                'firstStageByAlpha', 'bestScoreByAlpha',
                'alpha', 'beta', 'gamma',],
                results = resultsBetaGamma, hyperParameters = hyperParameters)

if __name__ == "__main__":
    main()

