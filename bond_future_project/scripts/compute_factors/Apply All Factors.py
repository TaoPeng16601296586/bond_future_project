# apply_all_factors.py
# 批量计算国债期货的 TA-Lib + CICC 动量因子 + CICC 波动率因子，标准化并保存合并输出结果

import os
import pandas as pd
from cicc_momentum_factors import CICC_MomentumFactors
from cicc_volatility_factors import CICCVolatilityFactors
from ta_lib_factors import TALibFactors
from sklearn.preprocessing import StandardScaler

# === 路径设置 ===
DATA_DIR = r"C:/Users/l/OneDrive/桌面/浙商固收/bond_future_project/data/raw data"
OUTPUT_DIR = r"C:/Users/l/OneDrive/桌面/浙商固收/bond_future_project/data/factors/merged"
ALL_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "全品种_合并因子汇总.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === 扫描所有主连合约文件 ===
files = [f for f in os.listdir(DATA_DIR) if "国债期货" in f and f.endswith(".csv")]

# 全部合约结果汇总容器
all_results = []

for file in files:
    print(f"\n📂 正在处理：{file}")
    file_path = os.path.join(DATA_DIR, file)
    df = pd.read_csv(file_path, parse_dates=["date"])

    # === 初始化并计算 TA-Lib 因子 ===
    df_talib = TALibFactors(df).add_all()

    # === 计算 CICC 动量因子 ===
    df_mmt = CICC_MomentumFactors(df).apply_all_momentum_factors()

    # === 计算 CICC 波动率因子 ===
    df_vol = CICCVolatilityFactors(df).add_all()

    # === 合并因子表（按 date 合并） ===
    df_merged = df_talib.merge(df_mmt, on="date", how="left")
    df_merged = df_merged.merge(df_vol, on="date", how="left")

    # === 添加 symbol 字段 ===
    symbol = file.split("_")[0]
    if "symbol" not in df_merged.columns:
        df_merged.insert(0, "symbol", symbol)
    else:
        df_merged["symbol"] = symbol

    # === 选择需标准化的数值列（排除非数值字段） ===
    numeric_cols = df_merged.select_dtypes(include=["float64", "int64"]).columns.drop(["volume"], errors="ignore")
    standard_cols = [col for col in numeric_cols if col not in ["open", "high", "low", "close"]]

    # === （可选）标准化处理（Z-score） ===（当前已跳过，保留原始因子值）
# scaler = StandardScaler()
# df_scaled = df_merged.copy()
# df_scaled[standard_cols] = scaler.fit_transform(df_scaled[standard_cols])

# 当前直接使用原始因子结果
    df_scaled = df_merged.copy()

    output_file = file.replace("_国债期货.csv", "_合并因子.csv")
    output_path = os.path.join(OUTPUT_DIR, output_file)
    df_scaled.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 合并因子保存至：{output_path}")

    all_results.append(df_scaled)

# === 合并所有品种为一个总表 ===
if all_results:
    df_all = pd.concat(all_results, ignore_index=True)
    df_all.to_csv(ALL_OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\n✅ 全品种合并因子已保存至：{ALL_OUTPUT_PATH}")
