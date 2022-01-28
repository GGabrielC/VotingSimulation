from VotingSystem.VotingSystems.MyVotingSystem.MyAbstractVotingSystem import MyAbstractVotingSystem
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.ThresholdFilter import ThresholdFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.LastStageFilter import LastStageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.FirstStageFilter import FirstStageFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.EntropyFilter import EntropyFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.VarianceFilter import VarianceFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StandardDeviationFilter import StandardDeviationFilter
from VotingSystem.VotingSystems.MyVotingSystem.StageFilters.StageFilter import ONLY_NULL_CANDIDATE

OFFSET_FOR_BETA = -1

class MyVotingSystem (MyAbstractVotingSystem):
    def __init__(self, alpha=0.5, beta=None, gamma=None, winStagePicker=None):
        winStagePicker = inferWinStagePicker(gamma, winStagePicker)
        firstStageFilters = [ ThresholdFilter(alpha) ]
        lastStageFilters = constructLastStageFilters(beta, gamma, defaultOffsetForBeta=OFFSET_FOR_BETA)
        name = constructName(alpha, beta, gamma, winStagePicker)
        super().__init__(winStagePicker, firstStageFilters, lastStageFilters, name)

def constructLastStageFilters(beta, gamma, defaultOffsetForBeta):
    lastStageFilters = []
    if beta is not None:
        lastStageFilters.append(ThresholdFilter(beta, ONLY_NULL_CANDIDATE, defaultOffset=defaultOffsetForBeta))
    if gamma is not None:
        lastStageFilters.append(ThresholdFilter(gamma))
    return lastStageFilters

def inferWinStagePicker(gamma, winStagePicker):
    winStagePicker = inferWinStagePickerFromString(winStagePicker) if type(winStagePicker) is str else winStagePicker
    if winStagePicker is None:
        winStagePicker = LastStageFilter() if gamma is not None else FirstStageFilter()
    return winStagePicker

def inferWinStagePickerFromString(winStagePicker):
    if winStagePicker is "first":
        return FirstStageFilter()
    elif winStagePicker is "last":
        return LastStageFilter()
    elif winStagePicker is "min_entropy" or winStagePicker is "entropy":
        return EntropyFilter()
    elif winStagePicker is "max_entropy":
        return EntropyFilter(lowest=False)
    elif winStagePicker is "min_variance":
        return VarianceFilter(highest=False)
    elif winStagePicker is "max_variance":
        return VarianceFilter()
    elif winStagePicker is "min_stdev":
        return StandardDeviationFilter(highest=False)
    elif winStagePicker is "max_stdev":
        return StandardDeviationFilter()
    return None

def constructName(alpha, beta, gamma, winStagePicker, hideNonExistent=False):
    name = "MyVoteSys <α={alpha:.2f}"
    if hideNonExistent:
        if beta is not None:
            name += ", β={beta:.2f}"
            if gamma is not None:
                name += ", γ={gamma:.2f}"
        elif gamma is not None:
            name += ", γ={gamma:.2f}"
    else:
        placeholder = -1
        if beta is None:
            beta = placeholder
        if gamma is None:
            gamma = placeholder
        name += ", β={beta:.2f}"
        name += ", γ={gamma:.2f}"
    name += ", {winStagePicker}>"
    name = name.format(**{'alpha': alpha, 'beta': beta, 'gamma': gamma,
                        'winStagePicker': winStagePicker.name})
    name = name.replace("-1.00", "____")
    return name