from scipy.optimize import minimize

def objective(x, StatsPool):
    x, y, z = x
    return -(1+x)*(1+y*z)  # 目的関数を負にすることで最大化問題に変換

def constraint(x, StatsPool):
    x, y, z = x
    return x/0.0496 + y/0.0331 + z/0.0662 - StatsPool

# StatsPoolの値を指定（例: 100）
StatsPool = 62

# 初期値を設定
x0 = [10, 10, 10]

# 制約条件付き最小化問題を解く
cons = ({'type': 'eq', 'fun': constraint, 'args':(StatsPool,)})
bounds = ((0, None), (0, None), (0, None))
result = minimize(objective, x0, args=(StatsPool,), method='SLSQP', constraints=cons, bounds=bounds)

print("最適解:", result.x)
print("最大値:", -result.fun)