import pandas as pd
import os

# ✅ 数据文件所在目录（如 Google Drive 挂载路径）
CLEAN_PATH = "/content/drive/MyDrive/quantitiave interest/data"

# === 单文件清洗函数 ===
def clean_futures_csv(file_path: str):
    print(f"\n📂 正在处理文件：{file_path}")
    try:
        df = pd.read_csv(file_path, parse_dates=["date"])
    except Exception as e:
        print(f"❌ 读取失败：{e}")
        return

    print(f"✅ 原始记录数：{len(df)}")

    # 去重
    df.drop_duplicates(subset=["symbol", "date"], inplace=True)

    # 缺失值处理
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print("⚠️ 存在缺失值：")
        print(missing[missing > 0])
        df.dropna(inplace=True)
        print(f"✅ 已删除缺失值行，剩余 {len(df)} 条")

    # 去除价格为0或负数的记录
    for col in ["open", "high", "low", "close"]:
        if col in df.columns:
            df = df[df[col] > 0]

    # 成交量与持仓量非负
    if "volume" in df.columns:
        df = df[df["volume"] >= 0]
    if "open_interest" in df.columns:
        df = df[df["open_interest"] >= 0]

    # 排序
    if "date" in df.columns and "symbol" in df.columns:
        df.sort_values(by=["date", "symbol"], inplace=True)

    # 保存清洗后文件
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"✅ 清洗完成，最终记录数：{len(df)}")

    # 跳空统计
    df = df.sort_values("date")
    df["prev_close"] = df["close"].shift(1)
    df["gap"] = df["open"] - df["prev_close"]
    gap_df = df[["date", "symbol", "open", "prev_close", "gap"]].dropna()
    gap_df = gap_df[gap_df["gap"] != 0]
    gap_output = file_path.replace(".csv", "_gap_stats.csv")
    gap_df.to_csv(gap_output, index=False, encoding="utf-8-sig")
    print(f"📈 跳空统计已保存至：{gap_output}")

# === 批量清洗入口 ===
def batch_clean_all_csv(folder_path=CLEAN_PATH):
    print(f"\n🔎 扫描目录：{folder_path}")
    all_csv = [f for f in os.listdir(folder_path) if f.endswith(".csv") and not f.endswith("_gap_stats.csv")]

    if not all_csv:
        print("⚠️ 未发现任何 .csv 文件")
        return

    for filename in all_csv:
        full_path = os.path.join(folder_path, filename)
        clean_futures_csv(full_path)

if __name__ == "__main__":
    print("🚿 启动国债期货数据清洗程序")
    batch_clean_all_csv()
    print("\n✅ 所有 .csv 文件清洗完成")
