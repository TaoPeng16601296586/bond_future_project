import os
import pandas as pd
from cicc_factors import CICCVolatilityFactors

# === 路径设置 ===
DATA_DIR =  r"C:/Users/l/OneDrive/桌面/浙商固收/bond_future_project/data/raw data"
OUTPUT_DIR = r"C:\Users\l\OneDrive\桌面\浙商固收\bond_future_project\data\factors\cicc_vol"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === 扫描所有主连合约文件 ===
files = [f for f in os.listdir(DATA_DIR) if "国债期货" in f and f.endswith(".csv")]

for file in files:
    print(f"\n📂 正在处理：{file}")
    file_path = os.path.join(DATA_DIR, file)
    df = pd.read_csv(file_path, parse_dates=["date"])

    # === 计算波动率因子 ===
    factor_engine = CICCVolatilityFactors(df)
    df_with_factors = factor_engine.add_all()

    # === 保存 ===
    output_file = file.replace("_\u56fd\u503a\u671f\u8d27.csv", "_\u6ce2\u52a8\u56e0\u5b50.csv")
    output_path = os.path.join(OUTPUT_DIR, output_file)
    df_with_factors.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 保存至：{output_path}")
