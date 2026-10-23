"""
二分查找 binary_search —— 严格依赖"待查表有序"的前提
tag: O5-step2
"""


def binary_search(rates, target):
    """
    在有序列表 rates 中查找 target，返回下标；若不存在返回 -1。
    同时返回比较次数，用于验证时间复杂度 O(log n)。
    """
    low, high = 0, len(rates) - 1
    count = 0                     # 查找/比较次数统计
    while low <= high:
        mid = (low + high) // 2   # 取中点下标
        count += 1
        if rates[mid] == target:
            return mid, count     # 命中，返回 (下标, 次数)
        elif rates[mid] < target:
            low = mid + 1         # 目标在右半
        else:
            high = mid - 1        # 目标在左半
    return -1, count              # 未命中


# ========== 构造 1024 档模拟利率表 ==========
# 0.00% ~ 10.23%，步长 0.01%，共 1024 档
# 人为选 1024 档位是因为 log2(1024)=10，刚好能用来验证"查找次数 ≤ 10"
rates_table = [round(0.01 * i, 4) for i in range(1024)]

# 验证一下是否真是 1024 档、且有序
assert len(rates_table) == 1024
assert rates_table == sorted(rates_table)

# ========== 检查点 2：在 1024 档表中找 3.75% ==========
TARGET = 3.75
idx, cnt = binary_search(rates_table, TARGET)
print("=" * 60)
print("【检查点 2】在 1024 档有序利率表中找 3.75%")
print("=" * 60)
print(f"  表长 n = {len(rates_table)}")
print(f"  理论下界 log2(n) = {__import__('math').log2(len(rates_table))}")
print(f"  目标 target = {TARGET}")
print(f"  返回下标 idx = {idx}")
print(f"  rates[{idx}] = {rates_table[idx] if idx != -1 else 'N/A'}")
print(f"  实际比较次数 = {cnt}")
print(f"  次数 ≤ 10?   {'YES' if cnt <= 10 else 'NO'}")
print()

# ========== 故意实验：传入未排序数组 ==========
print("=" * 60)
print("【故意实验】在未排序数组中用二分查找，看看会发生什么")
print("=" * 60)
# 故意制造一个"极端坏"的未排序数组：
# 最大值 99 放在最前面，最小值 0 放在最后面
unsorted = [99, 7, 1, 12, 3, 20, 5, 8, 0]
target_try = 5
print(f"  未排序数组 = {unsorted}")
print(f"  目标       = {target_try}")

idx_bad, cnt_bad = binary_search(unsorted, target_try)
print(f"  二分返回 idx = {idx_bad}, 比较次数 = {cnt_bad}")

# 但用线性扫描就能找到它
idx_linear = unsorted.index(target_try) if target_try in unsorted else -1
print(f"  线性扫描 idx = {idx_linear}")

print()
if idx_bad == -1 and idx_linear != -1:
    print("  ★ 二分找不到实际存在的元素 —— 前提被破坏，算法直接失效！")
elif idx_bad != idx_linear:
    print(f"  ★ 二分返回 idx={idx_bad} 但那并不是 {target_try} —— 前提被破坏，结果不可预测！")
else:
    print("  ★ 碰巧对了（巧合），但换一组数据就不一定。")

# 再一次：找末尾的最小值 0
print()
print("【再一次故意实验】找数组末尾的 0")
target_try2 = 0
idx_bad2, cnt_bad2 = binary_search(unsorted, target_try2)
idx_linear2 = unsorted.index(target_try2) if target_try2 in unsorted else -1
print(f"  目标        = {target_try2}")
print(f"  二分 idx    = {idx_bad2},  比较次数 = {cnt_bad2}")
print(f"  线性扫描 idx = {idx_linear2}")
if idx_bad2 == -1 and idx_linear2 != -1:
    print("  ★ 二分找不到实际存在的元素 —— 前提被破坏，算法直接失效！")
elif idx_bad2 != idx_linear2:
    print(f"  ★ 二分返回 idx={idx_bad2} 但那并不是 {target_try2} —— 结果不可预测！")
else:
    print("  ★ 又碰巧对了（巧合），但换一组数据就不一定。")

print()
print("【结论】二分查找正确性 = 有序前提 + 折半逻辑，二者缺一不可。")
