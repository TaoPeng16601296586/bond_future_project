---

# 中国国债期货多因子研究项目扩展指南

本项目聚焦国债期货主连合约（TS、TF、T、TL）行情数据的获取、清洗、因子构建与量化研究。未来将进一步扩展模型建模与因子评估，涵盖：

* 动态集成模型（Dynamic Ensemble Selection）
* 多种集成学习方法（XGBoost、LightGBM、CatBoost）
* 假设检验与统计评估（如 Kolmogorov-Smirnov Test）


---

---

## 未来模型模块配置

### 1️ 模型构建脚本（如 `run_xgboost.py`）

```bash
python models/run_xgboost.py --input data/model_input/merged.csv --label direction --test-size 0.2
```

### 2️ 动态集成选择模块

学习链接：[Dynamic Ensemble Selection](https://machinelearningmastery.com/dynamic-ensemble-selection-in-python/)

我们将使用 `deslib` 库：

```bash
pip install deslib
```

### 3️ KS 检验（用于因子分布、模型结果比较）

参考链接：[GFG - KS-Test](https://www.geeksforgeeks.org/kolmogorov-smirnov-test-ks-test/)

示例：

```python
from scipy.stats import ks_2samp

stat, p_value = ks_2samp(predicted_prob_1, predicted_prob_2)
```

---

##  requirements.txt 需加入的扩展依赖

```
xgboost
lightgbm
catboost
scipy
scikit-learn
deslib
```

---

## 新增运行说明（使用说明补充段）

### 4️ 构造模型训练数据

```bash
python scripts/prepare_model_data.py
```

### 5️ 模型训练与评估

```bash
python models/run_xgboost.py
python models/run_dynamic_ensemble.py
```

### 6️ KS 检验评估指标分布差异

```bash
python models/evaluate_ks_test.py
```

---


