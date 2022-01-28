import pandas as pd

class SplittedData:
    df_train_x = None
    df_train_y = None
    df_test_x = None
    df_test_y = None

    def __init__(self, df_train_x=None, df_train_y=None, df_test_x=None, df_test_y=None):
        self.df_train_x = df_train_x
        self.df_train_y = df_train_y
        self.df_test_x = df_test_x
        self.df_test_y = df_test_y

    def asDict(self):
        return {"df_train_x":self.df_train_x, "df_train_y":self.df_train_y, "df_test_x":self.df_test_x, "df_test_y":self.df_test_y}
    def train(self):
        return {"df_train_x":self.df_train_x, "df_train_y":self.df_train_y}
    def test(self):
        return {"df_test_x":self.df_test_x, "df_test_y":self.df_test_y}

    def dfTrain(self):
        return pd.concat([self.df_train_x, self.df_train_y], axis=1, join="inner")
    def dfTest(self):
        return pd.concat([self.df_test_x, self.df_test_y], axis=1, join="inner")

    def allX(self):
        return pd.concat([self.df_train_x, self.df_test_x])
    def allY(self):
        return pd.concat([self.df_train_y, self.df_test_y])
