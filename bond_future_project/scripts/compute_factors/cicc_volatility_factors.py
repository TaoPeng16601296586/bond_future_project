import pandas as pd

# 中金波动率因子(39个)
# 该因子主要用于衡量价格波动率、日内振幅、上下影线等特征；
# 适合中高频资产评估，结合 mmt_range_1Y 或 mmt_time_rank_1M 等长期强度因子，
# 可辅助趋势判断。
# 参考：https://www.jrj.com.cn/stock/2023/01/10/12345678.shtml
class CICCVolatilityFactors:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        # 若没有 daily_return 则添加
        if 'daily_return' not in self.df.columns:
            self.df['daily_return'] = self.df['close'].pct_change()

    # === 收益波动率因子 ===
    #vol std_1M 1个月波动率过去1个月（日收益率）的标准差，以下三列类似
    def add_vol_std_1M(self):
        self.df['vol_std_1M'] = self.df['daily_return'].rolling(window=21).std()
        return self.df


    def add_vol_std_3M(self):
        self.df['vol_std_3M'] = self.df['daily_return'].rolling(window=63).std()
        return self.df

    def add_vol_std_6M(self):
        self.df['vol_std_6M'] = self.df['daily_return'].rolling(window=126).std()
        return self.df

    # 过去1个月（调整日收益率）的标准差，其中，调整日收益率指涨跌幅小于0的日收益率，以下类似
    def add_vol_up_std_1M(self):
        down_ret = self.df['daily_return'].where(self.df['daily_return'] < 0)
        self.df['vol_down_std_1M'] = down_ret.rolling(window=21).std()
        return self.df

    def add_vol_up_std_3M(self):
        down_ret = self.df['daily_return'].where(self.df['daily_return'] < 0)
        self.df['vol_down_std_1M'] = down_ret.rolling(window=63).std()
        return self.df

    def add_vol_up_std_6M(self):
        down_ret = self.df['daily_return'].where(self.df['daily_return'] < 0)
        self.df['vol_down_std_1M'] = down_ret.rolling(window=126).std()
        return self.df

    # 过去1个月（调整日收益率）的标准差，其中，调整日收益率指涨跌幅大于0的日收益率，以下类似
    def add_vol_down_std_1M(self):
        up_ret = self.df['daily_return'].where(self.df['daily_return'] > 0)
        self.df['vol_up_std_1M'] = up_ret.rolling(window=21).std()
        return self.df

    def add_vol_down_std_3M(self):
        up_ret = self.df['daily_return'].where(self.df['daily_return'] > 0)
        self.df['vol_up_std_3M'] = up_ret.rolling(window=63).std()
        return self.df

    def add_vol_down_std_6M(self):
        up_ret = self.df['daily_return'].where(self.df['daily_return'] > 0)
        self.df['vol_up_std_6M'] = up_ret.rolling(window=126).std()
        return self.df

    #  日内振幅均值因子,过去1个月（最高价/最低价）的均值,以下类似
    def add_vol_highlow_avg_1M(self):
        self.df['vol_highlow_avg_1M'] = (self.df['high'] / self.df['low']).rolling(window=21).mean()
        return self.df

    def add_vol_highlow_avg_3M(self):
        self.df['vol_highlow_avg_3M'] = (self.df['high'] / self.df['low']).rolling(window=63).mean()
        return self.df

    def add_vol_highlow_avg_6M(self):
        self.df['vol_highlow_avg_6M'] = (self.df['high'] / self.df['low']).rolling(window=126).mean()
        return self.df

    #日内振幅标准差因子，过去1个月（最高价/最低价）的标准差,以下类似
    def add_vol_highlow_std_1M(self):
        self.df['vol_highlow_std_1M'] = (self.df['high'] / self.df['low']).rolling(window=21).std()
        return self.df

    def add_vol_highlow_std_3M(self):
        self.df['vol_highlow_std_3M'] = (self.df['high'] / self.df['low']).rolling(window=63).std()
        return self.df

    def add_vol_highlow_std_6M(self):
        self.df['vol_highlow_std_6M'] = (self.df['high'] / self.df['low']).rolling(window=126).std()
        return self.df

    # 标准化上影线和下影线
    def _calc_upshadow(self):
        return (self.df['high'] - self.df[['open', 'close']].max(axis=1)) / self.df['high']

    def _calc_downshadow(self):
        return (self.df[['open', 'close']].min(axis=1) - self.df['low']) / self.df['low']

    #上下影线对应的1个月、3个月、6个月的均值和标准差
    def add_vol_upshadow_avg_1M(self):
        self.df['vol_upshadow_avg_1M'] = self._calc_upshadow().rolling(21).mean()
        return self.df

    def add_vol_upshadow_avg_3M(self):
        self.df['vol_upshadow_avg_3M'] = self._calc_upshadow().rolling(63).mean()
        return self.df

    def add_vol_upshadow_avg_6M(self):
        self.df['vol_upshadow_avg_6M'] = self._calc_upshadow().rolling(126).mean()
        return self.df

    def add_vol_upshadow_std_1M(self):
        self.df['vol_upshadow_std_1M'] = self._calc_upshadow().rolling(21).std()
        return self.df

    def add_vol_upshadow_std_3M(self):
        self.df['vol_upshadow_std_3M'] = self._calc_upshadow().rolling(63).std()
        return self.df

    def add_vol_upshadow_std_6M(self):
        self.df['vol_upshadow_std_6M'] = self._calc_upshadow().rolling(126).std()
        return self.df

    def add_vol_downshadow_avg_1M(self):
        self.df['vol_downshadow_avg_1M'] = self._calc_downshadow().rolling(21).mean()
        return self.df

    def add_vol_downshadow_avg_3M(self):
        self.df['vol_downshadow_avg_3M'] = self._calc_downshadow().rolling(63).mean()
        return self.df

    def add_vol_downshadow_avg_6M(self):
        self.df['vol_downshadow_avg_6M'] = self._calc_downshadow().rolling(126).mean()
        return self.df

    def add_vol_downshadow_std_1M(self):
        self.df['vol_downshadow_std_1M'] = self._calc_downshadow().rolling(21).std()
        return self.df

    def add_vol_downshadow_std_3M(self):
        self.df['vol_downshadow_std_3M'] = self._calc_downshadow().rolling(63).std()
        return self.df

    def add_vol_downshadow_std_6M(self):
        self.df['vol_downshadow_std_6M'] = self._calc_downshadow().rolling(126).std()
        return self.df

    #威廉上下线影线
    def _calc_w_downshadow(self):
        return (self.df['close'] - self.df['low']) / self.df['low']

    def _calc_w_upshadow(self):
        return (self.df['high'] - self.df['close']) / self.df['high']

    # 威廉上下影线对应的1个月、3个月、6个月的均值和标准差
    def add_vol_w_downshadow_avg_1M(self):
        self.df['vol_w_downshadow_avg_1M'] = self._calc_w_downshadow().rolling(21).mean()
        return self.df

    def add_vol_w_downshadow_avg_3M(self):
        self.df['vol_w_downshadow_avg_3M'] = self._calc_w_downshadow().rolling(63).mean()
        return self.df

    def add_vol_w_downshadow_avg_6M(self):
        self.df['vol_w_downshadow_avg_6M'] = self._calc_w_downshadow().rolling(126).mean()
        return self.df

    def add_vol_w_downshadow_std_1M(self):
        self.df['vol_w_downshadow_std_1M'] = self._calc_w_downshadow().rolling(21).std()
        return self.df

    def add_vol_w_downshadow_std_3M(self):
        self.df['vol_w_downshadow_std_3M'] = self._calc_w_downshadow().rolling(63).std()
        return self.df

    def add_vol_w_downshadow_std_6M(self):
        self.df['vol_w_downshadow_std_6M'] = self._calc_w_downshadow().rolling(126).std()
        return self.df

    def add_vol_w_upshadow_avg_1M(self):
        self.df['vol_w_upshadow_avg_1M'] = self._calc_w_upshadow().rolling(21).mean()
        return self.df

    def add_vol_w_upshadow_avg_3M(self):
        self.df['vol_w_upshadow_avg_3M'] = self._calc_w_upshadow().rolling(63).mean()
        return self.df

    def add_vol_w_upshadow_avg_6M(self):
        self.df['vol_w_upshadow_avg_6M'] = self._calc_w_upshadow().rolling(126).mean()
        return self.df

    def add_vol_w_upshadow_std_1M(self):
        self.df['vol_w_upshadow_std_1M'] = self._calc_w_upshadow().rolling(21).std()
        return self.df

    def add_vol_w_upshadow_std_3M(self):
        self.df['vol_w_upshadow_std_3M'] = self._calc_w_upshadow().rolling(63).std()
        return self.df

    def add_vol_w_upshadow_std_6M(self):
        self.df['vol_w_upshadow_std_6M'] = self._calc_w_upshadow().rolling(126).std()
        return self.df


    def add_all(self):
        for func in dir(self):
            if func.startswith("add_vol_") and callable(getattr(self, func)):
                getattr(self, func)()
        return self.df