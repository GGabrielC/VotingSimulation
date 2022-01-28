# import pandas as pd
# import numpy as np
# import random
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, Activation, Lambda
#
# def addScalarLayer(model, scalar, sampleInput):
#     model.add(Dense(1, use_bias=False))
#     model.predict(sampleInput, batch_size=1)
#     model.layers[-1].set_weights(np.array([[[scalar]]]))
#     model.layers[-1].trainable = False
#
# def constructLayers(model, trainableLayerCount, sampleInput, maxOutput):
#     maxOutput = None
#     model.add(Dropout(0.11))
#     for i in range(trainableLayerCount):
#         model.add(Dense(sampleInput.shape[1], activation='relu'))
#         model.add(Dropout(0.11))
#
#     lastLayerActivation = 'relu' # if maxOutput is None else 'sigmoid'
#     model.add(Dense(1, activation=lastLayerActivation))
#     if not (maxOutput is None):
#         addScalarLayer(model=model, scalar=maxOutput+0.1, sampleInput=sampleInput)
#     else:
#         model.predict(sampleInput, batch_size=1)
#
# def buildModel(trainableLayerCount, metric, sampleInput, maxOutput):
#     loss = None
#     if metric == 'mean_squared_error':
#         loss = 'mean_squared_error'
#     elif metric == 'sparse_categorical_crossentropy':
#         loss = 'accuracy'
#
#     model = Sequential()
#     constructLayers(model, trainableLayerCount, sampleInput, maxOutput)
#     model.compile(optimizer='adam', loss=loss, metrics=[metric])
#     return model
#
# def takeLastEpochResults(results):
#     r = dict()
#     for k, v in results.items():
#         r[k] = v[-1]
#     return r
#
# def getFEParameters(columnsIdxs, testAtEachEpoch, batch_size, verbose, epochs, sData, fit=False, eval=False):
#     for columnsIdx in columnsIdxs:
#         trainData = {'x': sData.df_train_x.iloc[:, columnsIdx], 'y': sData.df_train_y}
#         testData = {'x': sData.df_test_x.iloc[:, columnsIdx], 'y': sData.df_test_y}
#         validation_data = (testData['x'], testData['y']) if testAtEachEpoch else None
#
#         commonParams = {'batch_size': batch_size, 'verbose': verbose}
#         fitParams = {**commonParams, **trainData, 'epochs': epochs, 'validation_data': validation_data}
#         evalParams = {**commonParams, **testData}
#         if fit and eval:
#             yield fitParams,evalParams
#         elif fit:
#             yield fitParams
#         elif eval:
#             yield evalParams
#         else:
#             raise Exception("Sorry bro/sis, can't have both fit=False eval=False !")
#
# def generateModelCollumnsIdxPair(count_models, collumnCount, df_train_x, trainableLayerCountInterval, metric, maxOutput):
#     models, columnsIdxs = [], []
#     for _ in range(count_models):
#         columnsIdx = random.sample(range(0, len(df_train_x.columns)), collumnCount)
#         sampleInput = df_train_x.iloc[0:1, columnsIdx].to_numpy()
#         trainableLayerCount = random.randint(trainableLayerCountInterval[0], trainableLayerCountInterval[1])
#         parameters = [trainableLayerCount, metric, sampleInput, maxOutput]
#         models.append(buildModel(*parameters))
#         columnsIdxs.append(columnsIdx)
#     return models, columnsIdxs
#
# def convertResultsEval(sampleModel, resultsEvalModels):
#     metrics = sampleModel.metrics_names
#     resultsEvalModels = [{metric: result[metrics.index(metric)] for metric in metrics} for result in resultsEvalModels]
#     [[r.update({"val_" + k: r.pop(k)}) for k in [i for i in r.keys()]] for r in resultsEvalModels]
#     return resultsEvalModels
#
# def combineResults(sampleModel, resultsFitModels, resultsEvalModels):
#     resultsEvalModels = convertResultsEval(sampleModel, resultsEvalModels)
#     results = [{**(takeLastEpochResults(rFit.history)), **rEval} for rFit, rEval in zip(resultsFitModels, resultsEvalModels)]
#     return results
#
# def getFitnessResults(models, paremetersFit, parametersEval, testAtEachEpoch):
#     resultsFitModels = [model.fit(**params) for model,params in zip(models,paremetersFit)]
#     if testAtEachEpoch:
#         resultsFitModels = [modelResult.history for modelResult in resultsFitModels]
#         # TODO maybe plot median progress of models's stats ?
#         results = [takeLastEpochResults(modelResult) for modelResult in resultsFitModels]
#     else:
#         resultsEvalModels = [model.evaluate(**params) for model,params in zip(models,parametersEval)]
#         results = combineResults(models[0], resultsFitModels, resultsEvalModels)
#     return results
#
# def buildCrowd(splittedData, size=100, epochs=1, maxOutput = None, maxIndividualMSE=None, minimumVisibleCollumns=None, trainableLayerCountInterval=[10,10], waveCount=1):
#     metric = "mean_squared_error"
#     verbose = 1
#     batch_size = 256
#     testAtEachEpoch = True
#     minimumVisibleCollumns = len(splittedData.df_train_x.columns) if minimumVisibleCollumns is None else minimumVisibleCollumns
#
#     dfCrowd = None
#     for collumnCount in range(minimumVisibleCollumns, minimumVisibleCollumns + waveCount):
#         print("collumnCount============", collumnCount)
#         count_models = size  # ** (waveCount - i)
#         models, columnsIdxs = generateModelCollumnsIdxPair(count_models, collumnCount, splittedData.df_train_x,
#                                                            trainableLayerCountInterval, metric, maxOutput)
#
#         parameters = [columnsIdxs, testAtEachEpoch, batch_size, verbose, epochs, splittedData]
#         paremetersFit, parametersEval = getFEParameters(fit=True, *parameters), getFEParameters(eval=True, *parameters)
#         results = getFitnessResults(models, paremetersFit, parametersEval, testAtEachEpoch)
#
#         df_r = pd.DataFrame(results).round(decimals=2)
#         df_r.insert(0, "Input_Columns", columnsIdxs)
#         df_r.insert(0, "Model", models)
#
#         if dfCrowd is None:
#             dfCrowd = df_r
#         else:
#             dfCrowd = pd.concat([dfCrowd, df_r], axis=0, ignore_index=True)
#     if maxIndividualMSE != None:
#         dfCrowd = dfCrowd.drop(dfCrowd[dfCrowd.val_mean_squared_error > maxIndividualMSE].index)
#     return dfCrowd
#
# #def predictionIndividuals(self, x, batch_size=128):
#     #return [m.predict(x.iloc[:, ci], batch_size=batch_size, verbose=0) for m, ci in zip(self.models(), self.collumnsIdxs())]
#
# #def collumnsIdxs(self):
# #   for index, model in self.dfCrowd.iterrows():
# #       yield model['Input_Columns']
#
# # def getFEParameters(columnsIdxs, testAtEachEpoch, batch_size, verbose, epochs, sData, fit=False, eval=False):
# #     for columnsIdx in columnsIdxs:
# #         trainData = {'x': sData.df_train_x.iloc[:, columnsIdx], 'y': sData.df_train_y}
# #         testData = {'x': sData.df_test_x.iloc[:, columnsIdx], 'y': sData.df_test_y}
# #         validation_data = (testData['x'], testData['y']) if testAtEachEpoch else None #test no iloc ?
# #
# #         commonParams = {'batch_size': batch_size, 'verbose': verbose}
# #         fitParams = {**commonParams, **trainData, 'epochs': epochs, 'validation_data': validation_data}
# #         evalParams = {**commonParams, **testData}
# #         if fit and eval:
# #             yield fitParams,evalParams
# #         elif fit:
# #             yield fitParams
# #         elif eval:
# #             yield evalParams
# #         else:
# #             raise Exception("Sorry bro/sis, can't have both fit=False eval=False !")