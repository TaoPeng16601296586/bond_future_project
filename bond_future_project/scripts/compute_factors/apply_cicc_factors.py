import os
import pandas as pd
from cicc_volatility_factors import CICCVolatilityFactors
from cicc_momentum_factors import CICC_MomentumFactors

# === 路径设置 ===
DATA_DIR = r"C:/Users/l/OneDrive/桌面/浙商固收/bond_future_project/data/raw data"
VOL_OUTPUT_DIR = r"C:/Users/l/OneDrive/桌面/浙商固收/bond_future_project/data/factors/cicc_vol"
MMT_OUTPUT_DIR = r"C:/Users/l/OneDrive/桌面/浙商固收/bond_future_project/data/factors/cicc_mmt"
os.makedirs(VOL_OUTPUT_DIR, exist_ok=True)
os.makedirs(MMT_OUTPUT_DIR, exist_ok=True)

# === 扫描所有主连合约文件 ===
files = [f for f in os.listdir(DATA_DIR) if "国债期货" in f and f.endswith(".csv")]

for file in files:
    print(f"\n📂 正在处理：{file}")
    file_path = os.path.join(DATA_DIR, file)
    df = pd.read_csv(file_path, parse_dates=["date"])

    # === 计算波动率因子 ===
    vol_engine = CICCVolatilityFactors(df)
    df_vol = vol_engine.add_all()

    # === 计算动量因子 ===
    mmt_engine = CICC_MomentumFactors(df)
    df_mmt = mmt_engine.apply_all_momentum_factors()

    # === 保存波动率因子结果 ===
    vol_output_file = file.replace("_国债期货.csv", "_波动因子.csv")
    vol_output_path = os.path.join(VOL_OUTPUT_DIR, vol_output_file)
    df_vol.to_csv(vol_output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 波动率因子保存至：{vol_output_path}")

    # === 保存动量因子结果 ===
    mmt_output_file = file.replace("_国债期货.csv", "_动量因子.csv")
    mmt_output_path = os.path.join(MMT_OUTPUT_DIR, mmt_output_file)
    df_mmt.to_csv(mmt_output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 动量因子保存至：{mmt_output_path}")
