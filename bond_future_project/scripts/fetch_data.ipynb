{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ec4b3019",
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install -i https://pypi.tuna.tsinghua.edu.cn/simple akshare"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0f7b5b98",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import akshare as ak\n",
    "from datetime import datetime, timedelta\n",
    "import os\n",
    "\n",
    "SAVE_PATH = \"/content/drive/MyDrive/quantitiave interest/data\"\n",
    "os.makedirs(SAVE_PATH, exist_ok=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c687a52d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 保存路径（Google Drive 或本地）\n",
    "SAVE_PATH = \"/content/drive/MyDrive/quantitiave interest/data\"\n",
    "os.makedirs(SAVE_PATH, exist_ok=True)\n",
    "\n",
    "# 保存函数\n",
    "def save_data(df: pd.DataFrame, name: str, folder: str = SAVE_PATH, filetype: str = \"csv\"):\n",
    "    file_path = os.path.join(folder, f\"{name}_主连_国债期货.{filetype}\")\n",
    "    if filetype == \"csv\":\n",
    "        df.to_csv(file_path, index=False, encoding=\"utf-8-sig\")\n",
    "    elif filetype == \"parquet\":\n",
    "        df.to_parquet(file_path, index=False)\n",
    "    print(f\"✅ 已保存：{file_path} 共 {len(df)} 条记录\")\n",
    "\n",
    "# 抓取某一主连数据\n",
    "def fetch_main_contract(symbol: str, name: str, days: int = 3650) -> pd.DataFrame:\n",
    "    end_date = datetime.today()\n",
    "    start_date = end_date - timedelta(days=days)\n",
    "\n",
    "    df = ak.futures_zh_daily_sina(symbol=symbol)\n",
    "    df[\"date\"] = pd.to_datetime(df[\"date\"])\n",
    "    df = df[(df[\"date\"] >= start_date) & (df[\"date\"] <= end_date)]\n",
    "    df[\"symbol\"] = name\n",
    "    return df[[\"symbol\", \"date\", \"open\", \"high\", \"low\", \"close\", \"volume\"]]\n",
    "\n",
    "# 批量抓取四个主连数据\n",
    "def fetch_all_main():\n",
    "    contracts = {\n",
    "        \"TS0\": \"TS_2Y\",\n",
    "        \"TF0\": \"TF_5Y\",\n",
    "        \"T0\": \"T_10Y\",\n",
    "        \"TL0\": \"TL_30Y\"\n",
    "    }\n",
    "\n",
    "    for symbol, name in contracts.items():\n",
    "        try:\n",
    "            print(f\"\\n🚀 正在抓取 {name} 主连数据...\")\n",
    "            df = fetch_main_contract(symbol, name)\n",
    "            save_data(df, name)\n",
    "        except Exception as e:\n",
    "            print(f\"❌ 抓取失败：{name}，错误：{e}\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    fetch_all_main()\n"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
