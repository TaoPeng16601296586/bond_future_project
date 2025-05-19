
# 🇨🇳 国债期货因子研究项目（Bond Futures Factor Research Project）

本项目聚焦中国国债期货（TF、T、TS、TL）市场的数据抓取、清洗与技术指标计算。  
数据来源于 [AkShare](https://github.com/jindaxiang/akshare)，因子来源包括 TA-Lib 以及中金公司研报中适用于国债期货的动量、波动率、价量因子。

---

## 项目结构

```

bond\_future\_project/
├── data/                          # 存储原始或更新后的 CSV 数据
│   ├── TF\_5Y\_Bond\_Futures.csv
│   ├── T\_10Y\_Bond\_Futures.csv
│   ├── TS\_2Y\_Bond\_Futures.csv
│   └── TL\_30Y\_Bond\_Futures.csv
│
├── scripts/                       # 项目核心逻辑脚本
│   ├── fetch\_data.py             # 全量抓取历史数据（首次使用）
│   ├── update\_data.py            # 每日增量更新
│   ├── clean\_data.py             # 批量清洗所有 CSV 数据
│   └── compute\_factors/          # 因子计算模块（按来源分类）
│       ├── **init**.py
│       ├── ta\_lib\_factors.py     # 使用 TA-Lib 计算技术指标
│       └── cicc\_factors.py       # 基于中金研报的特定因子
│
├── requirements.txt              # 项目依赖包列表
└── README.md                     # 当前说明文档

````

---

## 环境安装（建议使用虚拟环境）

```bash
# 克隆仓库
git clone https://github.com/your_username/bond_future_project.git
cd bond_future_project

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 安装依赖包
pip install -r requirements.txt
````

---

## 快速使用指南

### 第一次抓取全量数据

```bash
python scripts/fetch_data.py
```

### 每日增量更新

```bash
python scripts/update_data.py
```

### 批量清洗数据（去重、缺失、负数处理）

```bash
python scripts/clean_data.py
```

### 技术指标计算（动量、波动率等）

#### 使用 TA-Lib 计算技术指标：

```bash
python scripts/compute_factors/ta_lib_factors.py
```

#### 使用中金研报方法计算特色因子：

```bash
python scripts/compute_factors/cicc_factors.py
```

> 也可以将因子封装为函数批量计算并输出 CSV。

---

## 注意事项

* 数据默认保存在 `data/` 目录下。
* 建议先运行 `clean_data.py` 再进行因子计算。
* 使用 `ta-lib` 前请先安装对应的 C 库，参考：[TA-Lib 安装文档](https://mrjbq7.github.io/ta-lib/install.html)



