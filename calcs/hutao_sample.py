from scipy.optimize import minimize

def objective(x, StatsPool):
    waeponbase = 608
    skillratio = 0.0596 #T9 = 0.0596
    mvps = 2.8739 # 9N1CJ
    vaperatio = 0.75
    flatatk = 0
    x, y, z, w = x
    return -(((106+waeponbase+flatatk+skillratio*15552*(1+x))*mvps)*(1+y*z)*(1+(2.78*vaperatio*w)/(w+1400)))

def constraint(x, StatsPool):
    x, y, z, w = x
    return x/0.0496 + y/0.0331 + z/0.0662 + w/19.82 - StatsPool

# StatsPoolの値を指定
StatsPool = 70

# 初期値を設定
x0 = [10, 10, 10, 10]

# 制約条件付き最小化問題を解く
cons = ({'type': 'eq', 'fun': constraint, 'args':(StatsPool,)})
bounds = ((0, None), (0, 1), (0, None), (0, None))
result = minimize(objective, x0, args=(StatsPool,), method='SLSQP', constraints=cons, bounds=bounds)

print(result)