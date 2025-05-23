import pandas as pd
import talib
from datetime import datetime
import os

# ta_lib_factors.py
# 国债期货技术指标计算模块（基于 TA-Lib）
# 包含常用的动量类与量价类指标封装函数


class TALibFactors:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # === 动量类因子（Momentum Indicators） ===
    def add_adx(self, timeperiod=14):
        """平均趋向指数 ADX 及其方向性指标"""
        self.df[f"ADX_{timeperiod}"] = talib.ADX(self.df['high'], self.df['low'], self.df['close'], timeperiod)
        self.df[f"PLUS_DI_{timeperiod}"] = talib.PLUS_DI(self.df['high'], self.df['low'], self.df['close'], timeperiod)
        self.df[f"MINUS_DI_{timeperiod}"] = talib.MINUS_DI(self.df['high'], self.df['low'], self.df['close'], timeperiod)

    def add_cci(self, timeperiod=14):
        """顺势指标 CCI"""
        self.df[f"CCI_{timeperiod}"] = talib.CCI(self.df['high'], self.df['low'], self.df['close'], timeperiod)

    def add_mom(self, timeperiod=10):
        """动量指标 MOM"""
        self.df[f"MOM_{timeperiod}"] = talib.MOM(self.df['close'], timeperiod)

    def add_roc(self, timeperiod=10):
        """变动率 ROC"""
        self.df[f"ROC_{timeperiod}"] = talib.ROC(self.df['close'], timeperiod)

    def add_rsi(self, timeperiod=14):
        """相对强弱指数 RSI"""
        self.df[f"RSI_{timeperiod}"] = talib.RSI(self.df['close'], timeperiod)

    def add_willr(self, timeperiod=14):
        """威廉指标 WILLR"""
        self.df[f"WILLR_{timeperiod}"] = talib.WILLR(self.df['high'], self.df['low'], self.df['close'], timeperiod)

    def add_trix(self, timeperiod=15):
        """三重指数移动平均 TRIX"""
        self.df[f"TRIX_{timeperiod}"] = talib.TRIX(self.df['close'], timeperiod)

    def add_ppo(self, fastperiod=12, slowperiod=26, matype=0):
        """百分比价格振荡器 PPO"""
        self.df[f"PPO_{fastperiod}_{slowperiod}"] = talib.PPO(self.df['close'], fastperiod, slowperiod, matype)

    def add_stoch(self):
        """随机指标 KD (slow K/D)"""
        slowk, slowd = talib.STOCH(self.df['high'], self.df['low'], self.df['close'])
        self.df['STOCH_K'] = slowk
        self.df['STOCH_D'] = slowd

    # === 量价类因子（Volume Indicators） ===
    def add_obv(self):
        """能量潮指标 OBV"""
        self.df["OBV"] = talib.OBV(self.df['close'], self.df['volume'])

    def add_atr(self, timeperiod=14):
        """真实波幅 ATR"""
        self.df[f"ATR_{timeperiod}"] = talib.ATR(self.df['high'], self.df['low'], self.df['close'], timeperiod)

    def add_mfi(self, timeperiod=14):
        """资金流量指标 MFI"""
        self.df[f"MFI_{timeperiod}"] = talib.MFI(self.df['high'], self.df['low'], self.df['close'], self.df['volume'], timeperiod)

    def add_ad(self):
        """累积/派发线 AD"""
        self.df["AD"] = talib.AD(self.df['high'], self.df['low'], self.df['close'], self.df['volume'])

    def add_adosc(self, fastperiod=3, slowperiod=10):
        """震荡指标 ADOSC（Chaikin A/D Oscillator）"""
        self.df[f"ADOSC_{fastperiod}_{slowperiod}"] = talib.ADOSC(
            self.df['high'], self.df['low'], self.df['close'], self.df['volume'], fastperiod, slowperiod)

    # === 一键计算所有指标 ===
    def add_all(self):
        self.add_adx()
        self.add_cci()
        self.add_mom()
        self.add_roc()
        self.add_rsi()
        self.add_willr()
        self.add_trix()
        self.add_ppo()
        self.add_stoch()
        self.add_obv()
        self.add_atr()
        self.add_mfi()
        self.add_ad()
        self.add_adosc()
        return self.df
