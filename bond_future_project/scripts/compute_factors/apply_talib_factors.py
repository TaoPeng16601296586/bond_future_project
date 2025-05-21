import os
import pandas as pd
from ta_lib_factors import TALibFactors

# ✅ 指定你的真实本地路径（Windows OneDrive）
DATA_PATH = r"C:/Users/l/OneDrive/桌面/浙商固收/bond_future_project/data/raw data"
OUTPUT_PATH = r"C:/Users/l/OneDrive/桌面/浙商固收/bond_future_project/data/factors/talib"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# 遍历所有主连原始数据文件
for file in os.listdir(DATA_PATH):
    if "主连" in file and "国债期货" in file and file.endswith(".csv"):
        file_path = os.path.join(DATA_PATH, file)
        print(f"\n📂 正在处理：{file}...")

        df = pd.read_csv(file_path, parse_dates=["date"])

        # 添加 TA-Lib 因子
        factors = TALibFactors(df)
        df_with_factors = factors.add_all()

        # 保存结果
        output_file = file.replace(".csv", "_带因子.csv")
        df_with_factors.to_csv(os.path.join(OUTPUT_PATH, output_file), index=False, encoding="utf-8-sig")
        print(f"✅ 已保存至：{os.path.join(OUTPUT_PATH, output_file)}")
