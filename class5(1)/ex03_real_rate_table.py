"""
自主实践③：自制 100 档真实利率表，二分查找月供最接近 5000 的利率
- 年利率 1.00% ~ 5.95%，步长 0.05% → 正好 100 档
- 等额本息月供公式（贷款 50 万，30 年=360 月）：
    月供 = P * r * (1+r)^n / ((1+r)^n - 1)  其中 r = 年利率/12
- 二分在月供数组上找最接近 5000 的位置，再反查对应年利率
"""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binary_search import binary_search   # 复用 Step2 写的二分查找


# ========== 1. 自制 100 档年利率表 ==========
# 年利率 1.00%, 1.05%, 1.10%, ..., 5.95%  → 正好 100 档
RATES_100 = [round(1.00 + 0.05 * i, 2) for i in range(100)]
assert len(RATES_100) == 100, "利率表应该正好 100 档"
assert RATES_100[0]  == 1.00
assert RATES_100[-1] == 5.95
print("=" * 60)
print("【自主实践③】100 档真实利率表 + 二分找月供最接近 5000 的利率")
print("=" * 60)
print(f"  年利率范围: {RATES_100[0]}% ~ {RATES_100[-1]}%，步长 0.05%，共 {len(RATES_100)} 档")

# ========== 2. 月供计算 ==========
PRINCIPAL   = 1000000  # 贷款本金 100 万（50 万在 1%~6% 利率 + 30 年下月供最多才 2981，到不了 5000）
MONTHS      = 360      # 30 年 = 360 月
TARGET_PAY  = 5000     # 月供目标


def monthly_payment(annual_rate):
    """等额本息月供。annual_rate 是百分数形式（如 3.75 表示 3.75%）。"""
    r = annual_rate / 100 / 12    # 月利率
    n = MONTHS
    if r == 0:
        return PRINCIPAL / n
    return PRINCIPAL * r * (1 + r)**n / ((1 + r)**n - 1)


# 对每一档利率算月供
PAYMENTS = [monthly_payment(r) for r in RATES_100]

# 验证月供随利率单调递增（因为利率越高，月供越高）——这是二分的前提！
assert PAYMENTS == sorted(PAYMENTS), "月供必须随利率递增才能用二分"
print(f"  月供范围: {PAYMENTS[0]:.2f} ~ {PAYMENTS[-1]:.2f} 元")
print(f"  目标月供: {TARGET_PAY} 元")
print(f"  目标在范围内? {PAYMENTS[0] <= TARGET_PAY <= PAYMENTS[-1]}")
print()

# ========== 3. 二分查找 ==========
# 直接用 Step2 的 binary_search 找 TARGET_PAY
# 但 TARGET_PAY 可能并不恰好落在月供数组里（因为 0.05% 步长太粗），
# 我们可以先把最接近的那个"找等于"，如果找不到就退而求其次：
# 在 [idx-1, idx+1] 范围内扫一遍最接近的。
idx_hit, cnt = binary_search(PAYMENTS, TARGET_PAY)

if idx_hit != -1:
    best_idx = idx_hit
    print(f"  恰好命中！比较次数 = {cnt}")
else:
    print(f"  月供数组里没有恰好等于 {TARGET_PAY} 的档位（比较次数 = {cnt}）")
    # 二分能告诉我们的只是"目标应该插在哪个位置"
    # 但 binary_search 返回 -1 时不告诉我们位置，所以这里换一种方式：
    # 手动改一个"带位置返回"的二分来找最接近的
    low, high = 0, len(PAYMENTS) - 1
    insert_pos = 0
    while low <= high:
        mid = (low + high) // 2
        if PAYMENTS[mid] < TARGET_PAY:
            insert_pos = mid + 1
            low = mid + 1
        elif PAYMENTS[mid] > TARGET_PAY:
            high = mid - 1
        else:
            insert_pos = mid
            break

    # 在 insert_pos 附近扫一下谁最接近
    candidates = [c for c in [insert_pos - 1, insert_pos, insert_pos + 1]
                  if 0 <= c < len(PAYMENTS)]
    best_idx = min(candidates, key=lambda c: abs(PAYMENTS[c] - TARGET_PAY))
    print(f"  最接近的下标位置（二分给出插入点 ≈ {insert_pos}）→ 实际最佳 idx = {best_idx}")

best_rate    = RATES_100[best_idx]
best_payment = PAYMENTS[best_idx]
diff         = best_payment - TARGET_PAY

# 也看看旁边两档
left_idx  = max(0,        best_idx - 1)
right_idx = min(len(RATES_100) - 1, best_idx + 1)

print()
print("-" * 60)
print(f"  ★ 二分查找结果（共比较 {cnt} 次）")
print(f"    最接近的年利率 = {best_rate:.2f}%")
print(f"    对应月供       = {best_payment:.2f} 元")
print(f"    与目标 5000 差   = {abs(diff):.2f} 元  ({'偏高' if diff > 0 else '偏低'})")
print()
print("  附近对比（±0.05%）：")
for offset, idx in [("前一档(-0.05%)", left_idx), ("本档", best_idx), ("后一档(+0.05%)", right_idx)]:
    print(f"    {offset:>18}  利率 {RATES_100[idx]:.2f}%  月供 {PAYMENTS[idx]:.2f}  "
          f"差 {abs(PAYMENTS[idx] - TARGET_PAY):.2f} 元")

# ========== 4. 用线性扫描验证（二分结果正确性的交叉验证） ==========
print()
print("  ↓ 用线性扫描交叉验证（确保二分没错）")
linear_best = min(range(len(PAYMENTS)), key=lambda i: abs(PAYMENTS[i] - TARGET_PAY))
print(f"    线性扫描最接近 idx = {linear_best}（{RATES_100[linear_best]:.2f}%，月供 {PAYMENTS[linear_best]:.2f}）")
print(f"    二分 vs 线性扫描结果一致? {'✅ YES' if best_idx == linear_best else '❌ NO'}")

print()
print("【二分查找在 100 档上的效率：log₂100 ≈ 6.64，理论上 ≤ 7 次就搞定。】")
print(f"  本次实际比较次数 = {cnt}")
