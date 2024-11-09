from scipy.optimize import minimize

rarity = 5
weaponbase = 542

def objective(x):
    mvhps = 0.263
    vaperatio = 1
    h, r, d, e = x
    # h...HP% r...会心率 d...会心ダメージ e...元素熟知
    return -((15185*(1+h)*mvhps)*(1.466)*(1+r*d)*(1+vaperatio+(2.78*2*vaperatio*e)/(e+1400)))

def constraint(x, StatsPool):
    # KQMC Rev-AのSub roll scalarに基づくステータス分布 
    h, r, d, e = x
    return h/0.0496 + r/0.0331 + d/0.0662 + e/19.82 - StatsPool

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
        
# StatsPoolの値を指定(聖遺物メインOP: 10x3 聖遺物サブOP: 20 + 基礎会心 + 武器 + 突破)
# 参考:https://x.com/karashina82/status/1496846515838799879
StatsPool = 59 + base + rarity

# 初期値を設定
x0 = [0.1, 0.1, 0.1, 10]

# 制約条件付き最小化問題を解く
cons = ({'type': 'eq', 'fun': constraint, 'args':(StatsPool,)})
bounds = ((0, None), (0.192, 1), (0.5, None), (0, None))
result = minimize(objective, x0, method='SLSQP', constraints=cons, bounds=bounds, tol=1e-04)

print("ステータス制約:", StatsPool)
print("成否:", result.success)
print("出力:", result.message)
print("元素熟知:", result.x[3])
print("HP:", f"{result.x[0]:.10f}")
print("会心率:", result.x[1])
print("会心ダメージ:", result.x[1])
print("コピペ用:",f"{result.x[3]:.4f}",",",f"{result.x[1]:.4f}",",",f"{result.x[2]:.4f}",",",f"{result.x[0]:.4f}")