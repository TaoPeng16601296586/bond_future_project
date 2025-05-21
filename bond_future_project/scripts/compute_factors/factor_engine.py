import pandas as pd
from compute_factors.ta_lib_factors import TALibFactors
from compute_factors.cicc_factors import add_all_cicc_factors

class FactorEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def apply(self, sources: list = ["talib", "cicc"], talib_list: list = None):
        """
        sources: 可以包含 'talib' 和/或 'cicc'
        talib_list: 指定要使用的 talib 指标，若为 None 默认使用全部
        """
        if "talib" in sources:
            talib_factors = TALibFactors(self.df)
            if talib_list is None:
                self.df = talib_factors.add_all()
            else:
                self.df = talib_factors.add_by_list(talib_list)

        if "cicc" in sources:
            self.df = add_all_cicc_factors(self.df)

        return self.df

