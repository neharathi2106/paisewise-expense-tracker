"""Manual DAA implementations and reproducible-enough benchmark helpers."""
from time import perf_counter
import random

def _key(item): return float(item["amount"] if isinstance(item, dict) else item)

def merge_sort(items, descending=False):
    data = list(items)
    def sort(seq):
        if len(seq) < 2: return seq
        mid = len(seq)//2; left, right = sort(seq[:mid]), sort(seq[mid:]); out=[]; i=j=0
        while i < len(left) and j < len(right):
            take_left = _key(left[i]) >= _key(right[j]) if descending else _key(left[i]) <= _key(right[j])
            if take_left: out.append(left[i]); i+=1
            else: out.append(right[j]); j+=1
        return out + left[i:] + right[j:]
    return sort(data)

def bubble_sort(items, descending=False):
    data=list(items)
    for end in range(len(data)-1, 0, -1):
        swapped=False
        for i in range(end):
            a,b=_key(data[i]),_key(data[i+1])
            if (a < b if descending else a > b): data[i],data[i+1]=data[i+1],data[i]; swapped=True
        if not swapped: break
    return data

def binary_search_amount(sorted_items, amount):
    """Return every matching item. Input must be ascending by amount."""
    low, high=0,len(sorted_items)-1; found=-1; target=float(amount)
    while low<=high:
        mid=(low+high)//2; value=_key(sorted_items[mid])
        if value==target: found=mid; break
        if value<target: low=mid+1
        else: high=mid-1
    if found < 0: return []
    start=end=found
    while start>0 and _key(sorted_items[start-1])==target: start-=1
    while end+1<len(sorted_items) and _key(sorted_items[end+1])==target: end+=1
    return list(sorted_items[start:end+1])

def benchmark_sorts(items, repeats=1):
    """Compare equivalent independent copies; return median timings in seconds."""
    if repeats < 1: raise ValueError("repeats must be at least 1")
    bubble_times=[]; merge_times=[]
    for _ in range(repeats):
        a=list(items); b=list(items)
        start=perf_counter(); bubble_sort(a); bubble_times.append(perf_counter()-start)
        start=perf_counter(); merge_sort(b); merge_times.append(perf_counter()-start)
    bubble_times.sort(); merge_times.sort()
    return {"input_size":len(items),"repeats":repeats,"bubble_seconds":bubble_times[len(bubble_times)//2],"merge_seconds":merge_times[len(merge_times)//2]}

def synthetic_amounts(size, seed=42):
    if size < 0: raise ValueError("size cannot be negative")
    rng=random.Random(seed); return [round(rng.uniform(1,10000),2) for _ in range(size)]
