"""
自主实践①：给 merge_sort 加递归深度打印
观察 8000 元素的递归深度（应≈13，因为 log₂8000≈12.97）
"""
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def merge_sort_with_depth(nums, depth=0, max_depth_holder=None):
    """
    带递归深度统计的 merge_sort。
    max_depth_holder 是一个 list，外面传进来用来"拿回"最大深度：
        holder = [0]
        merge_sort_with_depth(arr, max_depth_holder=holder)
        print(holder[0])   # 就是最大递归深度
    """
    if max_depth_holder is not None:
        max_depth_holder[0] = max(max_depth_holder[0], depth)   # 更新当前最大深度

    if len(nums) <= 1:
        return nums

    mid = len(nums) // 2
    left  = merge_sort_with_depth(nums[:mid],  depth + 1, max_depth_holder)
    right = merge_sort_with_depth(nums[mid:], depth + 1, max_depth_holder)

    return _merge(left, right)


def _merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ========== 实测 ==========
print("=" * 60)
print("【自主实践①】递归深度实测")
print("=" * 60)

for n in [1000, 2000, 4000, 8000]:
    arr = [random.randint(0, 100000) for _ in range(n)]
    holder = [0]                          # 用来承接最大深度
    sorted_arr = merge_sort_with_depth(arr, max_depth_holder=holder)

    # 验证排对了
    assert sorted_arr == sorted(arr), f"n={n} 排序结果错误！"

    import math
    expected = math.ceil(math.log2(n))
    print(f"  n={n:>5}  实测最大递归深度 = {holder[0]}  "
          f"理论 log₂{n} ≈ {math.log2(n):.2f}  "
          f"ceil = {expected}  "
          f"{'✅' if holder[0] == expected else '⚠'}")

print()
print("结论：递归深度 = ceil(log₂n)，与理论一致。")
print("      Python 默认递归上限 1000，8000 才用 13，远远够用。")
