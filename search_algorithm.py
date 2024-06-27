"""File search algorithms implementation

Linear, Jump, Binary, KMP, and Exponential Search
"""

import math


def linear_search(arr, target):
    """Linear Search Inplementation Algorithm"""
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def jump_search(arr, target):
    """Jump Search Inplementation Algorithm"""
    length = len(arr)
    step = int(math.sqrt(length))
    prev = 0

    while prev < length and arr[min(step, length) - 1] < target:
        prev = step
        step += int(math.sqrt(length))
        if prev >= length:
            return -1

    for i in range(prev, min(step, length)):
        if arr[i] == target:
            return i
    return -1


def binary_search(arr, target):
    """Binary Search Inplementation Algorithm"""
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        elif arr[mid] > target:
            high = mid - 1
        else:
            return mid
    return -1


def kmp_search(text, pattern):
    """KMP Search Inplementation Algorithm"""
    def compute_lps_array(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps_array(pattern)
    i = 0
    j = 0

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def exponential_search(arr, target):
    """Exponential Search Inplementation Algorithm"""
    if arr[0] == target:
        return 0

    length = len(arr)
    i = 1
    while i < length and arr[i] <= target:
        i *= 2

    return binary_search(arr[:min(i, length)], target)
