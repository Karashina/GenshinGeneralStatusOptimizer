from scipy.optimize import minimize

rarity = 5
weaponbase = 608

def objective(x):
    mvps = 6.535
    vaperatio = 0.138
    swirl = 0.782
    a, r, d, e = x
    # a...攻撃力% r...会心率 d...会心ダメージ e...元素熟知
    return -(((347+weaponbase)*(1+a))*mvps)*(1+r*d)*(1+0.5*vaperatio+(4.17*vaperatio*e)/(e+1400))+868.1118*(1+(16*e)/(e+2000))*swirl

def constraint(x, StatsPool):
    # KQMC Rev-AのSub roll scalarに基づくステータス分布 
    a, r, d, e = x
    return a/0.0496 + r/0.0331 + d/0.0662 + e/19.82 - StatsPool

match weaponbase:
    case 741:
        base = 3
    case 674:
        base = 6
    case 608:
        base = 10
    case 542:
        base = 13
    case 620:
        base = 2
    case 565:
        base = 5
    case 510:
        base = 8
    case 454:
        base = 11
    case _:
        99999999 # as invalid
        
# StatsPoolの値を指定(聖遺物メインOP: 10x3 聖遺物サブOP: 20 + 武器 + 突破)
# 参考:https://x.com/karashina82/status/1496846515838799879
StatsPool = 50 + base + rarity

# 初期値を設定
x0 = [0.1, 0.1, 0.1, 10]

# 制約条件付き最小化問題を解く
cons = ({'type': 'eq', 'fun': constraint, 'args':(StatsPool,)})
bounds = ((0, 2), (0.192, 1), (0, None), (0, None))
result = minimize(objective, x0, method='SLSQP', constraints=cons, bounds=bounds, tol=1e-04)

print("ステータス制約:", StatsPool)
print("成否:", result.success)
print("出力:", result.message)
print("攻撃力:", f"{result.x[0]:.10f}")
print("元素熟知:", result.x[3])
print("会心率:", result.x[1])
print("会心ダメージ:", result.x[2])
print("コピペ用:",f"{result.x[0]:.4f}",",",f"{result.x[1]:.4f}",",",f"{result.x[2]:.4f}",",",f"{result.x[3]:.4f}")