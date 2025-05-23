import pandas as pd

# 中金动量因子封装类（20个）

class CICC_MomentumFactors:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df.sort_values("date", inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def add_mmt_normal_1M(self):
        self.df["mmt_normal_1M"] = self.df["close"].pct_change(periods=20)
        return self

    def add_mmt_normal_A(self):
        ret_12m = self.df["close"].pct_change(periods=240)
        ret_1m = self.df["close"].pct_change(periods=20)
        self.df["mmt_normal_A"] = ret_12m - ret_1m
        return self

    def add_mmt_avg_1M(self):
        self.df["mmt_avg_1M"] = self.df["close"] / self.df["close"].rolling(window=20).mean()
        return self

    def add_mmt_avg_1Y(self):
        self.df["close_1m_ago"] = self.df["close"].shift(21)
        self.df["avg_close_1y"] = self.df["close"].rolling(window=252).mean()
        self.df["mmt_avg_1Y"] = self.df["close_1m_ago"] / self.df["avg_close_1y"]
        return self

    def add_mmt_intraday_1M(self):
        self.df["intraday_return"] = self.df["close"] / self.df["open"] - 1
        self.df["mmt_intraday_1M"] = self.df["intraday_return"].rolling(window=21).sum()
        return self

    def add_mmt_overnight_1M(self):
        self.df["overnight_return"] = self.df["open"] / self.df["close"].shift(1) - 1
        self.df["mmt_overnight_1M"] = self.df["overnight_return"].rolling(window=21).sum()
        return self

    def add_mmt_overnight_1Y(self):
        self.df["overnight_return"] = self.df["open"] / self.df["close"].shift(1) - 1
        self.df["overnight_sum_1y"] = self.df["overnight_return"].rolling(window=252).sum()
        self.df["overnight_sum_1m"] = self.df["overnight_return"].rolling(window=21).sum()
        self.df["mmt_overnight_1Y"] = self.df["overnight_sum_1y"] - self.df["overnight_sum_1m"]
        return self

    def add_mmt_off_limit_1M(self):
        self.df["daily_return"] = self.df["close"] / self.df["close"].shift(1) - 1
        self.df["limit_flag"] = self.df["daily_return"].abs() >= 0.07
        self.df["valid_return"] = self.df["daily_return"].where(~self.df["limit_flag"], pd.NA)
        self.df["mmt_off_limit_1M"] = self.df["valid_return"].rolling(window=21, min_periods=1).sum()
        return self

    def add_mmt_off_limit_1Y(self):
        self.df["daily_return"] = self.df["close"] / self.df["close"].shift(1) - 1
        self.df["limit_flag"] = self.df["daily_return"].abs() >= 0.07
        self.df["valid_return"] = self.df["daily_return"].where(~self.df["limit_flag"], pd.NA)
        self.df["off_limit_sum_1y"] = self.df["valid_return"].rolling(window=252, min_periods=1).sum()
        self.df["off_limit_sum_1m"] = self.df["valid_return"].rolling(window=21, min_periods=1).sum()
        self.df["mmt_off_limit_1Y"] = self.df["off_limit_sum_1y"] - self.df["off_limit_sum_1m"]
        return self

    def add_mmt_range_1M(self):
        self.df["daily_return"] = self.df["close"] / self.df["close"].shift(1) - 1
        self.df["range"] = (self.df["high"] - self.df["low"]) / self.df["close"].shift(1)
        self.df["range_gt_20"] = self.df["daily_return"].where(self.df["range"] > 0.20, 0)
        self.df["range_le_20"] = self.df["daily_return"].where(self.df["range"] <= 0.20, 0)
        self.df["range_gt_20_sum"] = self.df["range_gt_20"].rolling(window=21, min_periods=1).sum()
        self.df["range_le_20_sum"] = self.df["range_le_20"].rolling(window=21, min_periods=1).sum()
        self.df["mmt_range_1M"] = self.df["range_gt_20_sum"] - self.df["range_le_20_sum"]
        return self

    def add_mmt_range_1Y(self):
        self.df["daily_return"] = self.df["close"] / self.df["close"].shift(1) - 1
        self.df["range"] = (self.df["high"] - self.df["low"]) / self.df["close"].shift(1)
        self.df["range_gt_20"] = self.df["daily_return"].where(self.df["range"] > 0.20, 0)
        self.df["range_le_20"] = self.df["daily_return"].where(self.df["range"] <= 0.20, 0)
        self.df["range_gt_20_sum"] = self.df["range_gt_20"].rolling(window=252, min_periods=1).sum()
        self.df["range_le_20_sum"] = self.df["range_le_20"].rolling(window=252, min_periods=1).sum()
        self.df["mmt_range_1Y"] = self.df["range_gt_20_sum"] - self.df["range_le_20_sum"]
        return self

    def add_mmt_route_1M(self):
        self.df["daily_return"] = self.df["close"] / self.df["close"].shift(1) - 1
        self.df["cumulative_return_1m"] = self.df["close"] / self.df["close"].shift(21) - 1
        self.df["sum_abs_return_1m"] = self.df["daily_return"].abs().rolling(window=21, min_periods=1).sum()
        self.df["mmt_route_1M"] = (self.df["cumulative_return_1m"] / self.df["sum_abs_return_1m"]).where(self.df["sum_abs_return_1m"] != 0)
        return self

    def add_mmt_route_1Y(self):
        self.df["daily_return"] = self.df["close"] / self.df["close"].shift(1) - 1
        self.df["cumulative_return_1y"] = self.df["close"] / self.df["close"].shift(252) - 1
        self.df["sum_abs_return_1y"] = self.df["daily_return"].abs().rolling(window=252, min_periods=1).sum()
        self.df["mmt_route_1Y"] = (self.df["cumulative_return_1y"] / self.df["sum_abs_return_1y"]).where(self.df["sum_abs_return_1y"] != 0)
        return self

    def add_mmt_discrete_1M(self):
        self.df["daily_return"] = self.df["close"] / self.df["close"].shift(1) - 1
        self.df["up_flag"] = (self.df["daily_return"] > 0).astype(int)
        self.df["down_flag"] = (self.df["daily_return"] < 0).astype(int)
        self.df["up_ratio_1m"] = self.df["up_flag"].rolling(window=21, min_periods=1).mean()
        self.df["down_ratio_1m"] = self.df["down_flag"].rolling(window=21, min_periods=1).mean()
        self.df["mmt_discrete_1M"] = self.df["up_ratio_1m"] - self.df["down_ratio_1m"]
        return self

    def add_mmt_discrete_1Y(self):
        self.df["daily_return"] = self.df["close"] / self.df["close"].shift(1) - 1
        self.df["up_flag"] = (self.df["daily_return"] > 0).astype(int)
        self.df["down_flag"] = (self.df["daily_return"] < 0).astype(int)
        self.df["up_ratio_1y"] = self.df["up_flag"].rolling(window=252, min_periods=1).mean()
        self.df["down_ratio_1y"] = self.df["down_flag"].rolling(window=252, min_periods=1).mean()
        self.df["mmt_discrete_1Y"] = self.df["up_ratio_1y"] - self.df["down_ratio_1y"]
        return self

    def add_mmt_self_rank_1M(self):
        self.df["daily_return"] = self.df["close"].pct_change()
        self.df["mmt_self_rank_1M"] = self.df["daily_return"].rolling(window=21).apply(
            lambda x: x.rank(pct=True).iloc[-1] if x.notna().sum() > 0 else pd.NA,
            raw=False
        )
        return self

    def add_mmt_time_rank_1M(self):
        self.df["ret_1y"] = self.df["close"] / self.df["close"].shift(252) - 1
        self.df["ret_rank_1y"] = self.df["ret_1y"].rolling(window=252, min_periods=1).apply(
            lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False
        )
        self.df["mmt_time_rank_1M"] = self.df["ret_rank_1y"].rolling(window=21, min_periods=1).mean()
        return self

    def add_mmt_year_open_return(self):
        self.df["year"] = self.df["date"].dt.year
        self.df["is_first_day"] = self.df["year"] != self.df["year"].shift(1)
        year_open = self.df[self.df["is_first_day"]][["date", "close", "year"]].copy()
        year_open["prev_close"] = year_open["close"].shift(1)
        year_open["mmt_year_open_return"] = year_open["close"] / year_open["prev_close"] - 1
        self.df = self.df.merge(year_open[["date", "mmt_year_open_return"]], on="date", how="left")
        return self

    def add_mmt_highest_days_1Y(self):
        max_day_list = []
        for i in range(len(self.df)):
            if i < 252:
                max_day_list.append(None)
                continue
            window = self.df.iloc[i - 252:i]
            max_idx = window["high"].idxmax()
            max_date = self.df.loc[max_idx, "date"]
            current_date = self.df.iloc[i]["date"]
            days_diff = (current_date - max_date).days
            max_day_list.append(days_diff)
        self.df["mmt_highest_days_1Y"] = max_day_list
        return self

    def apply_all_momentum_factors(self):
        return (
            self.add_mmt_normal_1M()
                .add_mmt_normal_A()
                .add_mmt_avg_1M()
                .add_mmt_avg_1Y()
                .add_mmt_intraday_1M()
                .add_mmt_overnight_1M()
                .add_mmt_overnight_1Y()
                .add_mmt_off_limit_1M()
                .add_mmt_off_limit_1Y()
                .add_mmt_range_1M()
                .add_mmt_range_1Y()
                .add_mmt_route_1M()
                .add_mmt_route_1Y()
                .add_mmt_discrete_1M()
                .add_mmt_discrete_1Y()
                .add_mmt_self_rank_1M()
                .add_mmt_time_rank_1M()
                .add_mmt_year_open_return()
                .add_mmt_highest_days_1Y()
                .df
        )

