"""
性能实验：冒泡排序 vs 合并排序 的计时对比
tag: O5-step3
"""
import timeit
import random
import csv
import os
import sys

# ========== 1. 导入 Step1 的合并排序 ==========
# 把当前目录加到 sys.path，方便直接 import merge_sort 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_sort import merge_sort


# ========== 2. 自己实现的冒泡排序（原地排序） ==========
def bubble_sort(nums):
    """原地冒泡排序，带中文注释。"""
    n = len(nums)
    # 外层控制"轮数"：共需 n-1 轮
    for i in range(n - 1):
        swapped = False                # 提前退出标记：若一轮无交换说明已排好
        # 内层比较相邻元素，每轮把最大的"冒泡"到末尾
        for j in range(n - 1 - i):     # 末尾 i 个已排好，无需再比较
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:
            break                      # 整个数组已有序，提前收工
    return nums


# ========== 3. 生成随机数组 ==========
def make_array(n, seed=42):
    """固定 seed 生成同一份随机数组，保证两种算法用完全相同的输入。"""
    rng = random.Random(seed)
    return [rng.randint(0, 100000) for _ in range(n)]


# ========== 4. 正确性自检（计时前先确认两种算法都排对了） ==========
_SANITY = [8, 3, 5, 1, 9, 2]
assert bubble_sort(_SANITY[:]) == [1, 2, 3, 5, 8, 9], "冒泡排序正确性失败！"
assert merge_sort(_SANITY[:]) == [1, 2, 3, 5, 8, 9], "合并排序正确性失败！"
print("【自检通过】冒泡 / 合并 排序都能正确输出 [1,2,3,5,8,9]")
print()


# ========== 5. 计时主循环 ==========
SIZES    = [1000, 2000, 4000, 8000]   # 待测试的 n
REPEATS  = 3                          # 每档跑几次取均值

# 结果表，同时准备写入 csv
rows = []

# 先打印表头
header = (
    f"{'n':>6}  "
    f"{'冒泡耗时(s)':>12}  "
    f"{'合并耗时(s)':>12}  "
    f"{'合并快几倍':>10}  "
    f"{'冒泡翻倍倍率':>12}  "
    f"{'合并翻倍倍率':>12}"
)
print(header)
print("-" * len(header))

prev_t_bubble, prev_t_merge = None, None   # 上一档耗时，用来算倍率

for n in SIZES:
    arr = make_array(n)                    # 同一份随机数组
    
    # 冒泡：原地排序，每次必须传副本 arr[:]
    # timeit 的 lambda 会被执行 number 次，每次都是新副本
    t_bubble = timeit.timeit(lambda: bubble_sort(arr[:]), number=REPEATS) / REPEATS
    
    # 合并：返回新列表，同样每次传副本
    t_merge  = timeit.timeit(lambda: merge_sort(arr[:]),  number=REPEATS) / REPEATS
    
    # 计算"翻倍倍率"（相对上一档）
    ratio_bubble = (t_bubble / prev_t_bubble) if prev_t_bubble else float("nan")
    ratio_merge  = (t_merge  / prev_t_merge)  if prev_t_merge  else float("nan")
    
    speedup = t_bubble / t_merge            # 合并比冒泡快几倍
    
    # 打印一行（第一档 n=1000 没有"翻倍倍率"参考）
    r_b_s = f"{ratio_bubble:>11.2f}×" if prev_t_bubble else "     —    "
    r_m_s = f"{ratio_merge:>11.2f}×"  if prev_t_merge  else "     —    "
    print(
        f"{n:>6}  "
        f"{t_bubble:>12.4f}  "
        f"{t_merge:>12.4f}  "
        f"{speedup:>9.1f}×  "
        f"{r_b_s}  "
        f"{r_m_s}"
    )
    
    rows.append({
        "n": n,
        "冒泡耗时_s": round(t_bubble, 6),
        "合并耗时_s": round(t_merge, 6),
        "合并快几倍": round(speedup, 1),
        "冒泡翻倍倍率": round(ratio_bubble, 2) if prev_t_bubble else None,
        "合并翻倍倍率":  round(ratio_merge,  2) if prev_t_merge  else None,
    })
    
    prev_t_bubble, prev_t_merge = t_bubble, t_merge


# ========== 6. 汇总检查点 3 ==========
print()
print("=" * 60)
print("【检查点 3】理论 vs 实测")
print("=" * 60)

# 验证 n=8000 时合并快一个数量级
final_speedup = rows[-1]["合并快几倍"]
print(f"  n=8000 时，合并比冒泡快约 {final_speedup:.0f} 倍  "
      f"{'✅ 数量级以上' if final_speedup >= 10 else '⚠ 未达 10 倍'}")

# 看看翻倍倍率的均值（剔除第一档的 None）
r_b = [r["冒泡翻倍倍率"] for r in rows if r["冒泡翻倍倍率"] is not None]
r_m = [r["合并翻倍倍率"] for r in rows if r["合并翻倍倍率"] is not None]
avg_r_b = sum(r_b) / len(r_b)
avg_r_m = sum(r_m) / len(r_m)
print(f"  冒泡平均翻倍倍率 ≈ {avg_r_b:.2f}  （理论 O(n²) → 应接近 4.00）"
      f"{' ✅' if abs(avg_r_b - 4.00) < 1.0 else ' ⚠'}")
print(f"  合并平均翻倍倍率 ≈ {avg_r_m:.2f}  （理论 O(n log n) → 应接近 2.00 略多）"
      f"{' ✅' if abs(avg_r_m - 2.00) < 0.5 else ' ⚠'}")

print()
print("【看懂了什么】")
print("  冒泡是 O(n²)：输入翻倍 → 工作量约 ×4 → 耗时也 ×4")
print("  合并是 O(n log n)：输入翻倍 → 工作量约 ×2 → 耗时也 ×2（略多一点点）")
print("  n=8000 时差距已经超过一个数量级——算法复杂度决定一切。")
print("  ↑ 把上面表格原样粘进 HW1 报告，这就是核心素材。")


# ========== 7. 顺手导出 csv（方便 HW1 粘表格） ==========
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_result.csv")
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["n", "冒泡耗时_s", "合并耗时_s",
                                            "合并快几倍", "冒泡翻倍倍率", "合并翻倍倍率"])
    writer.writeheader()
    writer.writerows(rows)
print()
print(f"【已导出】完整原始数据 → benchmark_result.csv")
