
# Selection Sort
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr, [(i, min_idx)]

# Bubble Sort
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, [(j, j + 1)]

# Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        yield arr, [(j, j + 1)]

# Merge Sort
def merge_sort(arr):
    def merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = arr[l:l + n1]
        R = arr[m + 1:m + 1 + n2]
        i = j = 0
        k = l
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            yield arr, [(k,)]
            k += 1
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            yield arr, [(k,)]
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            yield arr, [(k,)]

    def merge_sort_helper(arr, l, r):
        if l < r:
            m = l + (r - l) // 2
            yield from merge_sort_helper(arr, l, m)
            yield from merge_sort_helper(arr, m + 1, r)
            yield from merge(arr, l, m, r)

    yield from merge_sort_helper(arr, 0, len(arr) - 1)
    yield arr, []

# Quick Sort
def quick_sort(arr, low, high):
    if low < high:
        pi, swaps = partition(arr, low, high)
        yield arr, swaps
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high]
    swaps = []
    for j in range(low, high):
        if arr[j] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
            swaps.append((i, j))
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    swaps.append((i + 1, high))
    return (i + 1), swaps

# Heap Sort
def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr, [(i, largest)]
            yield from heapify(arr, n, largest)
    
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr, [(i, 0)]
        yield from heapify(arr, i, 0)

# Counting Sort
def counting_sort(arr):
    max_val = max(arr)
    min_val = min(arr)
    range_of_elements = max_val - min_val + 1
    count = [0] * range_of_elements
    output = [0] * len(arr)
    for i in range(len(arr)):
        count[arr[i] - min_val] += 1
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
        yield output[:], [(count[arr[i] - min_val],)]
    for i in range(len(arr)):
        arr[i] = output[i]
        yield arr, [(i,)]

# Radix Sort
def radix_sort(arr):
    def counting_sort_exp(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            yield output[:], [(count[index % 10],)]
        for i in range(n):
            arr[i] = output[i]
            yield arr, [(i,)]
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        yield from counting_sort_exp(arr, exp)
        exp *= 10


# Bucket Sort
def bucket_sort(arr):
    max_val = max(arr)
    size = max_val // len(arr)
    buckets = [[] for _ in range(len(arr))]
    for i in range(len(arr)):
        j = min(len(arr) - 1, arr[i] // size)
        buckets[j].append(arr[i])
    for i in range(len(arr)):
        yield from insertion_sort(buckets[i])
    result = []
    for i in range(len(arr)):
        result.extend(buckets[i])
    for i in range(len(arr)):
        arr[i] = result[i]
        yield arr, [(i,)]

# ShellSort
def shell_sort(arr):
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                yield arr, [(j, j - gap)]
            arr[j] = temp
        gap //= 2
    yield arr, []

# TimSort
def tim_sort(arr):
    min_run = 32
    n = len(arr)
    
    def insertion_sort_subarray(arr, left, right):
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                yield arr, [(j, j + 1)]
            arr[j + 1] = key
    
    def merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = arr[l:l + n1]
        M = arr[m + 1:m + 1 + n2]
        i = j = 0
        k = l
        while i < n1 and j < n2:
            if L[i] <= M[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = M[j]
                j += 1
            yield arr, [(k,)]
            k += 1
        while i < n1:
            arr[k] = L[i]
            i += 1
            yield arr, [(k,)]
            k += 1
        while j < n2:
            arr[k] = M[j]
            j += 1
            yield arr, [(k,)]
            k += 1
    
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        yield from insertion_sort_subarray(arr, start, end)
    
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                yield from merge(arr, left, mid, right)
        size = 2 * size

# Comb Sort
def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
                yield arr, [(i, i + gap)]

# Pigeonhole Sort
def pigeonhole_sort(arr):
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    holes = [0] * size
    for x in arr:
        holes[x - min_val] += 1
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + min_val
            i += 1
            yield arr, [(i,)]
    yield arr, []

# Cycle Sort
def cycle_sort(arr):
    writes = 0
    for cycle_start in range(len(arr) - 1):
        item = arr[cycle_start]
        pos = cycle_start
        for i in range(cycle_start + 1, len(arr)):
            if arr[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        writes += 1
        yield arr, [(pos,)]
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, len(arr)):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
            writes += 1
            yield arr, [(pos,)]

# Cocktail Sort
def cocktail_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                yield arr, [(i, i + 1)]
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                yield arr, [(i, i + 1)]
        start += 1

# Strand Sort
def strand_sort(arr):
    def merge(a, b):
        result = []
        while len(a) and len(b):
            if a[0] < b[0]:
                result.append(a.pop(0))
            else:
                result.append(b.pop(0))
        result.extend(a if len(a) else b)
        return result

    if len(arr) <= 1:
        return arr

    sorted_list = []
    while len(arr):
        sublist = [arr.pop(0)]
        i = 0
        while i < len(arr):
            if arr[i] > sublist[-1]:
                sublist.append(arr.pop(i))
            else:
                i += 1
        sorted_list = merge(sorted_list, sublist)
        yield sorted_list, [(i,)]
    for i in range(len(sorted_list)):
        arr[i] = sorted_list[i]
        yield arr, [(i,)]

# Pancake Sorting
def pancake_sort(arr):
    def flip(arr, i):
        start = 0
        while start < i:
            arr[start], arr[i] = arr[i], arr[start]
            start += 1
            i -= 1

    n = len(arr)
    for curr_size in range(n, 1, -1):
        mi = arr.index(max(arr[:curr_size]))
        if mi != curr_size - 1:
            flip(arr, mi)
            yield arr, [(mi,)]
            flip(arr, curr_size - 1)
            yield arr, [(curr_size - 1,)]

# BogoSort or Permutation Sort
import random
def bogo_sort(arr):
    def is_sorted(arr):
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                return False
        return True

    while not is_sorted(arr):
        random.shuffle(arr)
        yield arr, []
    yield arr, []


# Gnome Sort
def gnome_sort(arr):
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            yield arr, [(index, index - 1)]
            index -= 1

# Stooge Sort
def stooge_sort(arr):
    def stoogesort_helper(arr, l, h):
        if l >= h:
            return
        if arr[l] > arr[h]:
            arr[l], arr[h] = arr[h], arr[l]
            yield arr, [(l, h)]
        if h - l + 1 > 2:
            t = (h - l + 1) // 3
            yield from stoogesort_helper(arr, l, h - t)
            yield from stoogesort_helper(arr, l + t, h)
            yield from stoogesort_helper(arr, l, h - t)

    yield from stoogesort_helper(arr, 0, len(arr) - 1)

# Tag Sort
def tag_sort(arr):
    tagged_arr = [(i, arr[i]) for i in range(len(arr))]
    tagged_arr.sort(key=lambda x: x[1])
    for i in range(len(tagged_arr)):
        arr[i] = tagged_arr[i][1]
        yield arr, [(i,)]

# Odd-Even Sort / Brick Sort
def odd_even_sort(arr):
    n = len(arr)
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
                yield arr, [(i, i + 1)]
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
                yield arr, [(i, i + 1)]

# 3-way Merge Sort
def merge_sort_3way(arr):
    def merge(arr, l, m1, m2, r):
        n1 = m1 - l + 1
        n2 = m2 - m1
        n3 = r - m2
        L = arr[l:m1 + 1]
        M = arr[m1 + 1:m2 + 1]
        R = arr[m2 + 1:r + 1]
        i = j = k = 0
        while i < n1 and j < n2 and k < n3:
            if L[i] <= M[j] and L[i] <= R[k]:
                arr[l] = L[i]
                i += 1
            elif M[j] <= L[i] and M[j] <= R[k]:
                arr[l] = M[j]
                j += 1
            else:
                arr[l] = R[k]
                k += 1
            l += 1
            yield arr, [(l,)]
        while i < n1 and j < n2:
            if L[i] <= M[j]:
                arr[l] = L[i]
                i += 1
            else:
                arr[l] = M[j]
                j += 1
            l += 1
            yield arr, [(l,)]
        while j < n2 and k < n3:
            if M[j] <= R[k]:
                arr[l] = M[j]
                j += 1
            else:
                arr[l] = R[k]
                k += 1
            l += 1
            yield arr, [(l,)]
        while i < n1 and k < n3:
            if L[i] <= R[k]:
                arr[l] = L[i]
                i += 1
            else:
                arr[l] = R[k]
                k += 1
            l += 1
            yield arr, [(l,)]
        while i < n1:
            arr[l] = L[i]
            i += 1
            l += 1
            yield arr, [(l,)]
        while j < n2:
            arr[l] = M[j]
            j += 1
            l += 1
            yield arr, [(l,)]
        while k < n3:
            arr[l] = R[k]
            k += 1
            l += 1
            yield arr, [(l,)]

    def merge_sort_3way_helper(arr, l, r):
        if l < r:
            m1 = l + (r - l) // 3
            m2 = l + 2 * (r - l) // 3
            yield from merge_sort_3way_helper(arr, l, m1)
            yield from merge_sort_3way_helper(arr, m1 + 1, m2)
            yield from merge_sort_3way_helper(arr, m2 + 1, r)
            yield from merge(arr, l, m1, m2, r)

    yield from merge_sort_3way_helper(arr, 0, len(arr) - 1)
    yield arr, []



