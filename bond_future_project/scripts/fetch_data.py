# fetch_main_contracts.py
# 批量抓取 TS、TF、T、TL 主连期货日行情数据（来自 AkShare）

import pandas as pd
import akshare as ak
from datetime import datetime, timedelta
import os

# ✅ 保存路径（建议使用本地路径或挂载路径）
SAVE_PATH = "/content/drive/MyDrive/quantitiave interest/data"
os.makedirs(SAVE_PATH, exist_ok=True)

# === 保存函数（支持 csv 或 parquet） ===
def save_data(df: pd.DataFrame, name: str, folder: str = SAVE_PATH, filetype: str = "csv"):
    file_path = os.path.join(folder, f"{name}_主连_国债期货.{filetype}")
    if filetype == "csv":
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
    elif filetype == "parquet":
        df.to_parquet(file_path, index=False)
    print(f"✅ 已保存：{file_path} 共 {len(df)} 条记录")

# === 抓取某一主连数据（近 N 天） ===
def fetch_main_contract(symbol: str, name: str, days: int = 3650) -> pd.DataFrame:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    df = ak.futures_zh_daily_sina(symbol=symbol)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df["symbol"] = name
    return df[["symbol", "date", "open", "high", "low", "close", "volume"]]

# === 批量抓取四个主连数据 ===
def fetch_all_main():
    contracts = {
        "TS0": "TS_2Y",
        "TF0": "TF_5Y",
        "T0": "T_10Y",
        "TL0": "TL_30Y"
    }

    for symbol, name in contracts.items():
        try:
            print(f"\n🚀 正在抓取 {name} 主连数据...")
            df = fetch_main_contract(symbol, name)
            save_data(df, name)
        except Exception as e:
            print(f"❌ 抓取失败：{name}，错误：{e}")

if __name__ == "__main__":
    fetch_all_main()
