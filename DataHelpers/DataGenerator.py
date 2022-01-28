import random
import pandas as pd

def weightedSum(input, weights):
    return(sum([c*i for i,c in zip(input, weights)]))

def generate(rows, collumns, outFile=None, inputs=None, weights=None):
    collumns -= 1
    if weights is None:
        weights = [round(random.uniform(5,10), 3) for _ in range(collumns)]
    if inputs is None:
        inputs = [[round(random.uniform(-10,10),3) for _ in range(collumns)] for _ in range(rows)]
    df = pd.DataFrame( [[*x,weightedSum(x, weights)] for x in inputs],
                       columns= [*(list(range(len(inputs[0])))), "y"])

    if outFile:
        df.to_csv(outFile, index=False)

    return df