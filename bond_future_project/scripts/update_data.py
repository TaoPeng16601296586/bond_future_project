import pandas as pd
import akshare as ak
from datetime import datetime
import os

# 统一保存路径（保持与 fetch_all_main.py 一致）
SAVE_PATH = "/content/drive/MyDrive/quantitiave interest/data"

# 加载本地数据并判断最新日期
def load_existing_data(file_path: str) -> pd.DataFrame:
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8-sig", parse_dates=["date"])
        print(f"📂 已加载历史数据：{file_path}（至 {df['date'].max().date()}）")
        return df
    else:
        print(f"⚠️ 未找到历史数据文件，将初始化抓取：{file_path}")
        return pd.DataFrame()

# 从 akshare 获取新数据
def fetch_latest_main(symbol: str, name: str) -> pd.DataFrame:
    df = ak.futures_zh_daily_sina(symbol=symbol)
    df["date"] = pd.to_datetime(df["date"])
    df["symbol"] = name
    return df[["symbol", "date", "open", "high", "low", "close", "volume"]]

# 执行单个合约的数据更新逻辑
def update_main_contract(symbol: str, name: str):
    file_path = os.path.join(SAVE_PATH, f"{name}_主连_国债期货.csv")
    existing = load_existing_data(file_path)
    latest = fetch_latest_main(symbol, name)

    if not existing.empty:
        latest = latest[latest["date"] > existing["date"].max()]

    if latest.empty:
        print(f"✅ {name} 无需更新，数据已是最新。")
    else:
        updated = pd.concat([existing, latest], ignore_index=True).drop_duplicates(subset="date").sort_values("date")
        updated.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"✅ {name} 已更新 {len(latest)} 条数据 → 共 {len(updated)} 条记录")

# 合约映射
contracts = {
    "TS0": "TS_2Y",
    "TF0": "TF_5Y",
    "T0": "T_10Y",
    "TL0": "TL_30Y"
}

if __name__ == "__main__":
    for symbol, name in contracts.items():
        print(f"\n🔄 正在更新：{name} 主连数据...")
        update_main_contract(symbol, name)
    print("\n✅ 所有合约数据更新完成！")
