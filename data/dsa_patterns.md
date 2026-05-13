---
topic: DSA Patterns
framework: Algorithms
difficulty: Intermediate
---

# Data Structures and Algorithms Patterns

## Binary Search Pattern

Binary search is used to find elements in sorted arrays in O(log n) time.

**Template:**
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found
```

**When to use:**
- Searching in sorted array
- Finding first/last occurrence
- Search in rotated sorted array
- Finding peak element

**Common variations:**
1. Find first occurrence
2. Find last occurrence
3. Find insertion position
4. Search in 2D matrix

## Two Pointers Pattern

Use two pointers to solve problems involving arrays or linked lists.

**Template:**
```python
def two_pointers(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        # Process elements at left and right
        if condition:
            left += 1
        else:
            right -= 1
```

**When to use:**
- Finding pairs with target sum
- Removing duplicates
- Reversing array
- Container with most water
- Three sum problem

**Example: Two Sum in Sorted Array**
```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []
```

## Sliding Window Pattern

Maintain a window of elements and slide it through the array.

**Template:**
```python
def sliding_window(arr, k):
    window_start = 0
    result = []
    
    for window_end in range(len(arr)):
        # Add element to window
        
        # Shrink window if needed
        while window_condition:
            # Remove element from window
            window_start += 1
        
        # Process current window
        result.append(window_result)
    
    return result
```

**When to use:**
- Maximum sum subarray of size k
- Longest substring without repeating characters
- Minimum window substring
- Find all anagrams

**Example: Maximum Sum Subarray**
```python
def max_sum_subarray(arr, k):
    max_sum = 0
    window_sum = 0
    window_start = 0
    
    for window_end in range(len(arr)):
        window_sum += arr[window_end]
        
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]
            window_start += 1
    
    return max_sum
```

## DFS (Depth-First Search) Pattern

Explore as deep as possible before backtracking.

**Recursive Template:**
```python
def dfs(node, visited):
    if node is None or node in visited:
        return
    
    visited.add(node)
    # Process node
    
    for neighbor in node.neighbors:
        dfs(neighbor, visited)
```

**When to use:**
- Tree/graph traversal
- Finding connected components
- Detecting cycles
- Path finding
- Backtracking problems

**Why stack overflow happens:**
- Deep recursion without base case
- Large input causing deep call stack
- No visited set causing infinite recursion

**Solution: Use iterative DFS**
```python
def dfs_iterative(start):
    stack = [start]
    visited = set()
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        # Process node
        
        for neighbor in node.neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
```

## BFS (Breadth-First Search) Pattern

Explore level by level using a queue.

**Template:**
```python
from collections import deque

def bfs(start):
    queue = deque([start])
    visited = set([start])
    
    while queue:
        node = queue.popleft()
        # Process node
        
        for neighbor in node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**When to use:**
- Shortest path in unweighted graph
- Level order traversal
- Minimum steps problems
- Word ladder

## Dynamic Programming Pattern

Break problem into overlapping subproblems and store results.

**Bottom-up Template:**
```python
def dp_bottom_up(n):
    dp = [0] * (n + 1)
    dp[0] = base_case
    
    for i in range(1, n + 1):
        dp[i] = compute_from_previous(dp)
    
    return dp[n]
```

**Top-down (Memoization) Template:**
```python
def dp_top_down(n, memo={}):
    if n in memo:
        return memo[n]
    
    if n <= base_case:
        return base_value
    
    memo[n] = compute_recursively(n, memo)
    return memo[n]
```

**When to use:**
- Fibonacci sequence
- Climbing stairs
- Coin change
- Longest common subsequence
- Knapsack problems

**Example: Climbing Stairs**
```python
def climb_stairs(n):
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

## Fast and Slow Pointers (Floyd's Cycle Detection)

Use two pointers moving at different speeds.

**Template:**
```python
def has_cycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False
```

**When to use:**
- Detect cycle in linked list
- Find middle of linked list
- Find cycle start
- Happy number problem

## Backtracking Pattern

Explore all possibilities and backtrack when needed.

**Template:**
```python
def backtrack(path, choices):
    if is_solution(path):
        result.append(path.copy())
        return
    
    for choice in choices:
        # Make choice
        path.append(choice)
        
        # Recurse
        backtrack(path, remaining_choices)
        
        # Undo choice (backtrack)
        path.pop()
```

**When to use:**
- Permutations
- Combinations
- Subsets
- N-Queens
- Sudoku solver

## Tips for Problem Solving

1. **Identify the pattern** from problem description
2. **Draw examples** to understand the problem
3. **Start with brute force** then optimize
4. **Consider edge cases** (empty input, single element)
5. **Analyze time and space complexity**
6. **Practice similar problems** to recognize patterns
7. **Use appropriate data structures** (hash map, heap, stack)

## Common Time Complexities

- O(1): Constant - hash map lookup
- O(log n): Logarithmic - binary search
- O(n): Linear - single loop
- O(n log n): Linearithmic - merge sort
- O(n²): Quadratic - nested loops
- O(2ⁿ): Exponential - recursive fibonacci
