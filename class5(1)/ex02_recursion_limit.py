"""
独立研究②：sys.setrecursionlimit + 10 万元素递归上限实验
看点：
  1. Python 默认递归上限是多少？
  2. 合并排序 10 万元素的递归深度是多少？会不会撞？
  3. 如果会撞，setrecursionlimit 到多少才够？
"""
import sys
import os
import math
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_sort import merge_sort


print("=" * 60)
print("【独立研究②】递归上限实验")
print("=" * 60)

# 1. 默认上限
default_limit = sys.getrecursionlimit()
print(f"  Python 默认递归上限 = {default_limit}")

# 2. 先算理论递归深度
n_big = 100000
expected_depth = math.ceil(math.log2(n_big))
print(f"  合并排序 {n_big} 元素 → 理论递归深度 = ceil(log₂{n_big}) = {expected_depth}")
print(f"  {expected_depth} 远小于 {default_limit}，按理不会撞。")
print()

# 3. 实测 10 万元素会不会撞
arr = [random.randint(0, 1000000) for _ in range(n_big)]
print(f"  实测：对 {n_big} 个随机元素跑 merge_sort ... ", end="", flush=True)

try:
    result = merge_sort(arr)
    print("✅ 成功，未触发 RecursionError")
    # 验证排对了
    assert result == sorted(arr), "排序结果错误！"
    print(f"  结果已校验，耗时正常。")
except RecursionError as e:
    print(f"❌ 炸了！RecursionError: {e}")

print()

# 4. 那 setrecursionlimit 到底是给什么人用的？
# 给一个人为低上限的例子，演示它会炸
print("  ↓ 演示：把上限降到理论深度以下，merge_sort 会不会炸？")
print(f"     先看看 10 万元素理论深度是 {expected_depth}，")
print(f"     把上限设为 20 应该仍然 > {expected_depth}，不会炸；")
print(f"     把上限设为 5 应该会炸。")
print()

for limit in [20, 15, 10, 5]:
    sys.setrecursionlimit(limit)
    try:
        result = merge_sort(arr)
        print(f"  上限={limit:>2}:  ✅ 成功")
    except RecursionError:
        print(f"  上限={limit:>2}:  ❌ RecursionError 炸了")
    # 用完恢复
    sys.setrecursionlimit(default_limit)

print()
print("【结论】")
print(f"  sys.setrecursionlimit(N) 设置递归深度上限，超过就 RecursionError。")
print(f"  默认 1000，对合并排序来说 {expected_depth} 就够，远远碰不上；")
print(f"  但如果把上限人为降低到 {expected_depth} 以下，合并排序会立刻炸。")
print("  工程上几乎不会有人调这个——除非你在写深度神经网络的反向传播")
print("  或编译器的 AST 遍历，那种递归深度可能真上千。")
print("  另外注意：递归不等于'分治'——有些分治可以写成迭代"
      "（归并排序可迭代实现），")
print("  递归只是 Python 实现分治最顺手的一种写法。")
