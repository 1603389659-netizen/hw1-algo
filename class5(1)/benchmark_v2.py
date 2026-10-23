"""
自主实践② + 独立研究③：扩展 benchmark，对比三种排序
- 冒泡（自造 O(n²)）
- 合并（自造 O(n log n) 纯 Python）
- Python 内置 sorted（Timsort，C 实现 O(n log n)）
同时对比随机数组 vs 逆序数组 耗时差异
"""
import timeit
import random
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_sort import merge_sort


def bubble_sort(nums):
    n = len(nums)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:
            break
    return nums


def make_array(n, seed=42):
    rng = random.Random(seed)
    return [rng.randint(0, 100000) for _ in range(n)]


# 自检
_SANITY = [8, 3, 5, 1, 9, 2]
assert bubble_sort(_SANITY[:]) == [1, 2, 3, 5, 8, 9]
assert merge_sort(_SANITY[:])  == [1, 2, 3, 5, 8, 9]
assert sorted(_SANITY)         == [1, 2, 3, 5, 8, 9]
print("【自检通过】冒泡 / 合并 / sorted 三种算法都排对")
print()


SIZES   = [1000, 2000, 4000, 8000]
REPEATS = 3

# ========== Part A：三种算法横比（随机数组） ==========
print("=" * 80)
print("【自主实践②】冒泡 vs 自造合并 vs Python 内置 sorted —— 同一份随机数组")
print("=" * 80)

header = (
    f"{'n':>6}  "
    f"{'冒泡(s)':>10}  "
    f"{'自造合并(s)':>12}  "
    f"{'sorted(s)':>10}  "
    f"{'合并/冒泡':>10}  "
    f"{'sorted/合并':>12}  "
    f"{'sorted/冒泡':>12}"
)
print(header)
print("-" * len(header))

rows = []
for n in SIZES:
    arr = make_array(n)
    t_bubble = timeit.timeit(lambda: bubble_sort(arr[:]), number=REPEATS) / REPEATS
    t_merge  = timeit.timeit(lambda: merge_sort(arr[:]),  number=REPEATS) / REPEATS
    t_sorted = timeit.timeit(lambda: sorted(arr[:]),       number=REPEATS) / REPEATS

    print(
        f"{n:>6}  "
        f"{t_bubble:>10.4f}  "
        f"{t_merge:>12.4f}  "
        f"{t_sorted:>10.4f}  "
        f"{t_bubble/t_merge:>9.1f}×  "
        f"{t_merge/t_sorted:>11.1f}×  "
        f"{t_bubble/t_sorted:>11.1f}×"
    )
    rows.append({
        "n": n,
        "冒泡_s": round(t_bubble, 6),
        "自造合并_s": round(t_merge, 6),
        "sorted_s": round(t_sorted, 6),
        "合并比冒泡快": round(t_bubble/t_merge, 1),
        "sorted比合并快": round(t_merge/t_sorted, 1),
        "sorted比冒泡快": round(t_bubble/t_sorted, 1),
    })

# 导 CSV
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_v2_result.csv")
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["n", "冒泡_s", "自造合并_s", "sorted_s",
                                            "合并比冒泡快", "sorted比合并快", "sorted比冒泡快"])
    writer.writeheader()
    writer.writerows(rows)
print(f"\n【已导出】benchmark_v2_result.csv")

# ========== Part B：独立研究③ 随机 vs 逆序 —— 合并耗时对比 ==========
print()
print("=" * 80)
print("【独立研究③】随机数组 vs 逆序数组 —— 自造合并排序耗时对比")
print("=" * 80)

for n in SIZES:
    random_arr = make_array(n)              # 随机
    reverse_arr = list(range(n, 0, -1))     # 严格逆序，最坏情况

    # 先断言都能排对
    assert merge_sort(random_arr)  == sorted(random_arr)
    assert merge_sort(reverse_arr) == sorted(reverse_arr)

    t_rand = timeit.timeit(lambda: merge_sort(random_arr[:]),  number=REPEATS) / REPEATS
    t_rev  = timeit.timeit(lambda: merge_sort(reverse_arr[:]), number=REPEATS) / REPEATS
    ratio  = t_rand / t_rev if t_rev > 0 else float("nan")
    print(f"  n={n:>5}  随机耗时={t_rand:.4f}s  逆序耗时={t_rev:.4f}s  "
          f"随机/逆序 ≈ {ratio:.2f}  {'几乎不变 ✅' if abs(1 - ratio) < 0.15 else '有差'}")

print()
print("【为什么几乎不变？】")
print("  合并排序对任何输入的工作量都是 O(n log n)：")
print("  - 分解阶段：无论输入是随机、有序、逆序，切两半都是切两半，跟数据分布无关。")
print("  - 合并阶段：双指针扫描两个有序子表，每比较一次就放一个元素进结果，")
print("    无论左小还是右小，比较次数总量恒等于 len(left)+len(right)。")
print("  只有在某个子表耗光、另一个剩余直接 extend 的时机略有先后，")
print("  这种微差远不足以抵消常数项噪声。")
print("  → 合并排序没有'最好情况'——它的复杂度对任何输入都一样。")
print("  → 这既是优点（最坏情况也不会炸），也是它不如快排快的原因"
      "（快排平均 O(n log n) 常数更小，但逆序会退化）。")
