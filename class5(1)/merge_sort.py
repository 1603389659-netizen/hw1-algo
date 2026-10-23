"""
合并排序 merge_sort —— 严格按"分解-解决-合并"三段结构实现
tag: O5-step1
"""


def merge_sort(nums):
    """对列表 nums 进行合并排序，返回排好序的新列表。"""

    # ========== 分解（Divide） ==========
    # 递归终止条件：长度 <= 1 的子表天然有序，直接返回
    if len(nums) <= 1:
        return nums

    # 1. 求中点，将原表一分为二
    mid = len(nums) // 2

    # 2. 分别对左右两个子表递归排序（解决过程的入口）
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    # ========== 合并（Merge） ==========
    # 将两个已排序的子表 left、right 合并成一个有序表
    return merge(left, right)


def merge(left, right):
    """把两个各自有序的列表 left 与 right 合并为一个有序列表并返回。"""
    result = []          # 合并结果
    i, j = 0, 0          # 双指针：i 指向 left，j 指向 right

    # 依次比较两个子表当前元素，把较小者放入结果
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 任一子表耗尽后，把另一子表剩余部分直接拼到结果末尾
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ========== main：验证入口 ==========
if __name__ == "__main__":
    data = [8, 3, 5, 1, 9, 2]
    sorted_data = merge_sort(data)
    print("原序列:", data)
    print("排序后:", sorted_data)

    # 检查点 1：期望输出 [1, 2, 3, 5, 8, 9]
    expected = [1, 2, 3, 5, 8, 9]
    print("期望序列:", expected)
    print("通过?" , "YES" if sorted_data == expected else "NO")
