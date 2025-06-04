import argparse
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier


def load_data(path: str) -> pd.DataFrame:
    """加载并预处理因子数据"""
    print(f"\n📂 读取数据: {path}")
    df = pd.read_csv(path)

    # 方向标签推断
    if 'direction' not in df.columns:
        if 'valid_return' in df.columns:
            df['direction'] = (df['valid_return'] > 0).astype(int)
        elif 'up_flag' in df.columns:
            df['direction'] = df['up_flag']
        else:
            raise ValueError('未找到 direction 或可推断的标签列')

    df.dropna(subset=['direction'], inplace=True)

    # 仅保留数值型特征
    feature_cols = df.select_dtypes(include='number').columns.tolist()
    if 'direction' in feature_cols:
        feature_cols.remove('direction')
    if not feature_cols:
        raise ValueError('未找到数值型特征列')

    X = df[feature_cols]
    y = df['direction']
    return X, y


def train_xgboost(X: pd.DataFrame, y: pd.Series, test_size: float):
    """训练并评估 XGBoost 模型"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, shuffle=False
    )
    model = XGBClassifier(eval_metric='logloss')
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\n✅ 测试集准确率: {acc:.4f}")

    # 简单回测指标
    if 'valid_return' in X.columns:
        returns = X_test['valid_return']
    else:
        returns = pd.Series([0]*len(preds))
    strategy_ret = returns * (preds * 2 - 1)
    win_rate = (strategy_ret > 0).mean()
    print(f"✅ 胜率: {win_rate:.4f}")
    cum_ret = strategy_ret.cumsum().iloc[-1]
    print(f"✅ 累计收益: {cum_ret:.4f}")


def main():
    parser = argparse.ArgumentParser(description='XGBoost 利率方向预测')
    parser.add_argument('--input', default='bond_future_project/data/factors/merged/全品种_合并因子汇总.csv')
    parser.add_argument('--test-size', type=float, default=0.2)
    args = parser.parse_args()

    X, y = load_data(args.input)
    train_xgboost(X, y, args.test_size)


if __name__ == '__main__':
    main()
