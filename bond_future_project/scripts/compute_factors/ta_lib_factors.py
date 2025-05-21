import pandas as pd
import talib
from datetime import datetime
import os

class TALibFactors:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def add_adx(self, timeperiod=14):
        self.df[f"ADX_{timeperiod}"] = talib.ADX(self.df['high'], self.df['low'], self.df['close'], timeperiod)
        self.df[f"PLUS_DI_{timeperiod}"] = talib.PLUS_DI(self.df['high'], self.df['low'], self.df['close'], timeperiod)
        self.df[f"MINUS_DI_{timeperiod}"] = talib.MINUS_DI(self.df['high'], self.df['low'], self.df['close'], timeperiod)

    def add_cci(self, timeperiod=14):
        self.df[f"CCI_{timeperiod}"] = talib.CCI(self.df['high'], self.df['low'], self.df['close'], timeperiod)

    def add_mom(self, timeperiod=10):
        self.df[f"MOM_{timeperiod}"] = talib.MOM(self.df['close'], timeperiod)

    def add_roc(self, timeperiod=10):
        self.df[f"ROC_{timeperiod}"] = talib.ROC(self.df['close'], timeperiod)

    def add_rsi(self, timeperiod=14):
        self.df[f"RSI_{timeperiod}"] = talib.RSI(self.df['close'], timeperiod)

    def add_willr(self, timeperiod=14):
        self.df[f"WILLR_{timeperiod}"] = talib.WILLR(self.df['high'], self.df['low'], self.df['close'], timeperiod)

    def add_obv(self):
        self.df["OBV"] = talib.OBV(self.df['close'], self.df['volume'])

    def add_atr(self, timeperiod=14):
        self.df[f"ATR_{timeperiod}"] = talib.ATR(self.df['high'], self.df['low'], self.df['close'], timeperiod)

    def add_all(self):
        self.add_adx()
        self.add_cci()
        self.add_mom()
        self.add_roc()
        self.add_rsi()
        self.add_willr()
        self.add_obv()
        self.add_atr()
        return self.df
