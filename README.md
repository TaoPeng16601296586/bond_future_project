
# 中国国债期货因子研究项目（Bond Futures Factor Research Project）

本项目聚焦中国国债期货（TF、T、TS、TL）市场的数据抓取、清洗与技术指标计算。  
数据来源于 [AkShare](https://github.com/jindaxiang/akshare)，因子来源包括 TA-Lib 以及中金公司研报中适用于国债期货的动量、波动率、价量因子。

---

## 项目结构

```

bond\_future\_project/
├── data/
│   ├── raw data/                 # 原始数据（抓取或更新后存放）
│   │   ├── TF\_2年期主连\_2018至2025\_国债期货.csv
│   │   └── ...
│   └── factors/
│       ├── talib/               # TA-Lib 技术因子结果
│       └── cicc\_vol/            # 中金风格因子结果
│
├── scripts/
│   ├── fetch\_data.py            # 全量抓取
│   ├── update\_data.py           # 增量更新
│   ├── clean\_data.py            # 数据清洗
│   └── compute\_factors/
│       ├── apply\_talib\_factors.py     # 批量计算 TA-Lib 因子
│       ├── apply\_cicc\_factors.py      # 批量计算中金波动率因子
│       ├── ta\_lib\_factors.py
│       ├── cicc\_factors.py
│       └── factor\_engine.py
│
├── requirements/                # 环境依赖说明
│   └── requirements.txt
└── README.md

````

---

## 环境安装

```bash
# 克隆项目
git clone https://github.com/your_username/bond_future_project.git
cd bond_future_project

# 可选：创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements/requirements.txt
````
---

## 快速使用指南

### 1️ 抓取数据

```bash
python scripts/fetch_data.py        # 初次抓取
python scripts/update_data.py       # 增量更新
```

### 2️ 数据清洗（建议每次更新后执行）

```bash
python scripts/clean_data.py
```

### 3️ 计算技术因子

#### TA-Lib 动量、波动率类指标

```bash
python scripts/compute_factors/apply_talib_factors.py
```

#### 中金波动率、振幅、影线类指标

```bash
python scripts/compute_factors/apply_cicc_factors.py
```

---

## 注意事项

* 所有 `.csv` 原始数据应存放在 `data/raw data/` 下；
* 因子计算结果输出到 `data/factors/` 子目录中；
* `TA-Lib` 使用前请提前安装 C 库（详见：[TA-Lib 安装指南](https://mrjbq7.github.io/ta-lib/install.html)）；
* 推荐先执行数据清洗再运行因子计算。

---

