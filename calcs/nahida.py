from scipy.optimize import minimize

rarity = 5
weaponbase = 542

def objective(x):
    x, y, z, w = x
    dmgbonus = min(0.8,0.001*w)
    crbonus = min(0.24,0.0003*w)
    # w...元素熟知 x...攻撃力 y...会心率 z...会心ダメージ
    return -((0.743*(299+weaponbase)*(1+x)+1.274*(115+w)+0.975*1808.58*(1+(5*w)/(w+1200)))*(1+dmgbonus+0.466)*(1+(y+crbonus)*z))

def constraint(x, StatsPool):
    # KQMC Rev-AのSub roll scalarに基づくステータス分布    
    x, y, z, w = x
    return x/0.0496 + y/0.0331 + z/0.0662 + w/19.82 - StatsPool

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
        
# StatsPoolの値を指定(聖遺物メインOP: 10x2 or 10x3 聖遺物サブOP: 20 + 武器と突破)
# 参考:https://x.com/karashina82/status/1496846515838799879
StatsPool = 40 + rarity + base

# 初期値を設定
x0 = [0.5, 0.5, 0.5, 10]

# 制約条件付き最小化問題を解く
cons = ({'type': 'eq', 'fun': constraint, 'args':(StatsPool,)})
bounds = ((0, None), (0, 1), (0, None), (0, None))
result = minimize(objective, x0, method='SLSQP', constraints=cons, bounds=bounds, tol=1e-04)

print("ステータス制約:", StatsPool)
print("成否:", result.success)
print("出力:", result.message)
print("元素熟知:", result.x[3])
print("攻撃力:", f"{result.x[0]:.10f}")
print("会心率:", result.x[1])
print("会心ダメージ:", result.x[2])