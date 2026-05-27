"""
Comprehensive DSA Question Bank with 22 real coding interview problems.
Each question has full problem statements, examples, test cases, hints,
starter code, and metadata for adaptive difficulty selection.
"""

import random
from typing import Optional


# ---------------------------------------------------------------------------
# Full Question Definitions
# ---------------------------------------------------------------------------

QUESTIONS: list[dict] = [
    # ======================================================================
    # 1. Two Sum (Easy, Arrays)
    # ======================================================================
    {
        "id": "two-sum",
        "title": "Two Sum",
        "description": (
            "Given an array of integers `nums` and an integer `target`, return the "
            "indices of the two numbers such that they add up to `target`.\n\n"
            "You may assume that each input would have exactly one solution, and you "
            "may not use the same element twice.\n\n"
            "You can return the answer in any order.\n\n"
            "**Example 1:**\n"
            "Input: nums = [2,7,11,15], target = 9\n"
            "Output: [0,1]\n"
            "Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].\n\n"
            "**Example 2:**\n"
            "Input: nums = [3,2,4], target = 6\n"
            "Output: [1,2]\n\n"
            "**Example 3:**\n"
            "Input: nums = [3,3], target = 6\n"
            "Output: [0,1]"
        ),
        "difficulty": "easy",
        "topic": "arrays",
        "constraints": [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists.",
        ],
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "nums[1] + nums[2] = 2 + 4 = 6"},
            {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 3 + 3 = 6"},
        ],
        "test_cases": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected_output": [0, 1]},
            {"input": {"nums": [3, 2, 4], "target": 6}, "expected_output": [1, 2]},
            {"input": {"nums": [3, 3], "target": 6}, "expected_output": [0, 1]},
            {"input": {"nums": [1, 5, 3, 7], "target": 8}, "expected_output": [1, 2]},
            {"input": {"nums": [-1, -2, -3, -4, -5], "target": -8}, "expected_output": [2, 4]},
            {"input": {"nums": [0, 4, 3, 0], "target": 0}, "expected_output": [0, 3]},
            {"input": {"nums": [1, 2], "target": 3}, "expected_output": [0, 1]},
        ],
        "hints": [
            "Think about using a hash map to store numbers you've already seen.",
            "For each number, check if (target - number) exists in your hash map.",
            "Iterate once: for each element, look up complement in map, then insert current element.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(n)"},
        "solution_approach": (
            "Use a hash map to store each number's index as you iterate. For each "
            "element, check if target - current_number is already in the map. If so, "
            "return [map[complement], current_index]."
        ),
        "starter_code": {
            "python": "def twoSum(nums: list[int], target: int) -> list[int]:\n    pass",
            "javascript": "function twoSum(nums, target) {\n    \n}",
            "cpp": (
                "#include <vector>\n#include <unordered_map>\nusing namespace std;\n\n"
                "class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        \n    }\n};"
            ),
        },
        "tags": ["hash-map", "complement", "one-pass"],
    },

    # ======================================================================
    # 2. Best Time to Buy and Sell Stock (Easy, Arrays)
    # ======================================================================
    {
        "id": "buy-sell-stock",
        "title": "Best Time to Buy and Sell Stock",
        "description": (
            "You are given an array `prices` where `prices[i]` is the price of a "
            "given stock on the i-th day.\n\n"
            "You want to maximize your profit by choosing a single day to buy one "
            "stock and choosing a different day in the future to sell that stock.\n\n"
            "Return the maximum profit you can achieve from this transaction. If you "
            "cannot achieve any profit, return 0.\n\n"
            "**Example 1:**\n"
            "Input: prices = [7,1,5,3,6,4]\n"
            "Output: 5\n"
            "Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.\n\n"
            "**Example 2:**\n"
            "Input: prices = [7,6,4,3,1]\n"
            "Output: 0\n"
            "Explanation: No profit possible since prices only decrease."
        ),
        "difficulty": "easy",
        "topic": "arrays",
        "constraints": [
            "1 <= prices.length <= 10^5",
            "0 <= prices[i] <= 10^4",
        ],
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explanation": "Buy at 1, sell at 6"},
            {"input": "prices = [7,6,4,3,1]", "output": "0", "explanation": "No profitable transaction"},
        ],
        "test_cases": [
            {"input": {"prices": [7, 1, 5, 3, 6, 4]}, "expected_output": 5},
            {"input": {"prices": [7, 6, 4, 3, 1]}, "expected_output": 0},
            {"input": {"prices": [1, 2]}, "expected_output": 1},
            {"input": {"prices": [2, 1]}, "expected_output": 0},
            {"input": {"prices": [1]}, "expected_output": 0},
            {"input": {"prices": [3, 3, 3, 3]}, "expected_output": 0},
            {"input": {"prices": [1, 4, 2, 7]}, "expected_output": 6},
        ],
        "hints": [
            "Track the minimum price seen so far as you iterate.",
            "At each step, calculate profit = current_price - min_price_so_far.",
            "Keep a running maximum of the profit seen.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(1)"},
        "solution_approach": (
            "Single pass: maintain min_price and max_profit. For each price, update "
            "min_price if lower, then update max_profit = max(max_profit, price - min_price)."
        ),
        "starter_code": {
            "python": "def maxProfit(prices: list[int]) -> int:\n    pass",
            "javascript": "function maxProfit(prices) {\n    \n}",
            "cpp": (
                "#include <vector>\nusing namespace std;\n\n"
                "class Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        \n    }\n};"
            ),
        },
        "tags": ["greedy", "single-pass", "tracking-minimum"],
    },

    # ======================================================================
    # 3. Valid Parentheses (Easy, Stacks & Queues)
    # ======================================================================
    {
        "id": "valid-parentheses",
        "title": "Valid Parentheses",
        "description": (
            "Given a string `s` containing just the characters '(', ')', '{', '}', "
            "'[' and ']', determine if the input string is valid.\n\n"
            "An input string is valid if:\n"
            "1. Open brackets must be closed by the same type of brackets.\n"
            "2. Open brackets must be closed in the correct order.\n"
            "3. Every close bracket has a corresponding open bracket of the same type.\n\n"
            "**Example 1:** Input: s = \"()\" → Output: true\n"
            "**Example 2:** Input: s = \"()[]{}\" → Output: true\n"
            "**Example 3:** Input: s = \"(]\" → Output: false"
        ),
        "difficulty": "easy",
        "topic": "stacks_queues",
        "constraints": ["1 <= s.length <= 10^4", "s consists of parentheses only '()[]{}'"],
        "examples": [
            {"input": 's = "()"', "output": "true", "explanation": "Single pair matches"},
            {"input": 's = "()[]{}"', "output": "true", "explanation": "All pairs match"},
            {"input": 's = "(]"', "output": "false", "explanation": "Mismatched types"},
        ],
        "test_cases": [
            {"input": {"s": "()"}, "expected_output": True},
            {"input": {"s": "()[]{}"}, "expected_output": True},
            {"input": {"s": "(]"}, "expected_output": False},
            {"input": {"s": "([)]"}, "expected_output": False},
            {"input": {"s": "{[]}"}, "expected_output": True},
            {"input": {"s": ""}, "expected_output": True},
            {"input": {"s": "("}, "expected_output": False},
            {"input": {"s": "((()))"}, "expected_output": True},
        ],
        "hints": [
            "Use a stack to keep track of opening brackets.",
            "When you see a closing bracket, check if the top of stack has the matching opening bracket.",
            "At the end, the stack should be empty if all brackets were matched.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(n)"},
        "solution_approach": "Use a stack. Push opening brackets, pop and match for closing brackets. Return stack.empty() at end.",
        "starter_code": {
            "python": "def isValid(s: str) -> bool:\n    pass",
            "javascript": "function isValid(s) {\n    \n}",
            "cpp": "#include <string>\n#include <stack>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isValid(string s) {\n        \n    }\n};",
        },
        "tags": ["stack", "matching", "brackets"],
    },

    # ======================================================================
    # 4. Merge Two Sorted Lists (Easy, Linked Lists)
    # ======================================================================
    {
        "id": "merge-two-sorted-lists",
        "title": "Merge Two Sorted Lists",
        "description": (
            "You are given the heads of two sorted linked lists `list1` and `list2`.\n\n"
            "Merge the two lists into one sorted list. The list should be made by "
            "splicing together the nodes of the first two lists.\n\n"
            "Return the head of the merged linked list.\n\n"
            "**Example 1:**\n"
            "Input: list1 = [1,2,4], list2 = [1,3,4]\n"
            "Output: [1,1,2,3,4,4]\n\n"
            "**Example 2:**\n"
            "Input: list1 = [], list2 = []\n"
            "Output: []"
        ),
        "difficulty": "easy",
        "topic": "linked_lists",
        "constraints": [
            "The number of nodes in both lists is in the range [0, 50].",
            "-100 <= Node.val <= 100",
            "Both list1 and list2 are sorted in non-decreasing order.",
        ],
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]", "explanation": "Merge two sorted lists"},
            {"input": "list1 = [], list2 = []", "output": "[]", "explanation": "Both empty"},
        ],
        "test_cases": [
            {"input": {"list1": [1, 2, 4], "list2": [1, 3, 4]}, "expected_output": [1, 1, 2, 3, 4, 4]},
            {"input": {"list1": [], "list2": []}, "expected_output": []},
            {"input": {"list1": [], "list2": [0]}, "expected_output": [0]},
            {"input": {"list1": [1], "list2": [2]}, "expected_output": [1, 2]},
            {"input": {"list1": [5, 10, 15], "list2": [2, 3, 20]}, "expected_output": [2, 3, 5, 10, 15, 20]},
        ],
        "hints": [
            "Use a dummy head node to simplify the merge logic.",
            "Compare current nodes of both lists and append the smaller one.",
            "Don't forget to append the remaining nodes when one list is exhausted.",
        ],
        "optimal_complexity": {"time": "O(n + m)", "space": "O(1)"},
        "solution_approach": "Iterative merge with a dummy head. Compare head nodes, link the smaller one, advance pointer. Append remainder.",
        "starter_code": {
            "python": (
                "# Using arrays to represent linked lists for simplicity\n"
                "def mergeTwoLists(list1: list[int], list2: list[int]) -> list[int]:\n    pass"
            ),
            "javascript": "function mergeTwoLists(list1, list2) {\n    \n}",
            "cpp": (
                "#include <vector>\nusing namespace std;\n\n"
                "class Solution {\npublic:\n    vector<int> mergeTwoLists(vector<int>& list1, vector<int>& list2) {\n        \n    }\n};"
            ),
        },
        "tags": ["linked-list", "merge", "two-pointer"],
    },

    # ======================================================================
    # 5. Maximum Depth of Binary Tree (Easy, Trees)
    # ======================================================================
    {
        "id": "max-depth-binary-tree",
        "title": "Maximum Depth of Binary Tree",
        "description": (
            "Given the root of a binary tree, return its maximum depth.\n\n"
            "A binary tree's maximum depth is the number of nodes along the longest "
            "path from the root node down to the farthest leaf node.\n\n"
            "The tree is represented as a list in level-order where None/null "
            "represents empty nodes.\n\n"
            "**Example 1:**\n"
            "Input: root = [3,9,20,null,null,15,7]\n"
            "Output: 3\n\n"
            "**Example 2:**\n"
            "Input: root = [1,null,2]\n"
            "Output: 2"
        ),
        "difficulty": "easy",
        "topic": "trees",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 10^4].",
            "-100 <= Node.val <= 100",
        ],
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3", "explanation": "Longest path has 3 nodes"},
            {"input": "root = [1,null,2]", "output": "2", "explanation": "Depth is 2"},
        ],
        "test_cases": [
            {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "expected_output": 3},
            {"input": {"root": [1, None, 2]}, "expected_output": 2},
            {"input": {"root": []}, "expected_output": 0},
            {"input": {"root": [1]}, "expected_output": 1},
            {"input": {"root": [1, 2, 3, 4, 5]}, "expected_output": 3},
        ],
        "hints": [
            "Think recursively: the depth of a tree = 1 + max(depth of left subtree, depth of right subtree).",
            "Base case: an empty tree has depth 0.",
            "You can also solve this iteratively using BFS (level-order traversal).",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(h) where h is height"},
        "solution_approach": "DFS recursion: return 0 if null, else 1 + max(maxDepth(left), maxDepth(right)).",
        "starter_code": {
            "python": (
                "# Tree given as level-order list, None for empty nodes\n"
                "def maxDepth(root: list) -> int:\n    pass"
            ),
            "javascript": "function maxDepth(root) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxDepth(vector<int>& root) {\n        \n    }\n};",
        },
        "tags": ["tree", "dfs", "recursion", "bfs"],
    },

    # ======================================================================
    # 6. Climbing Stairs (Easy, DP)
    # ======================================================================
    {
        "id": "climbing-stairs",
        "title": "Climbing Stairs",
        "description": (
            "You are climbing a staircase. It takes `n` steps to reach the top.\n\n"
            "Each time you can either climb 1 or 2 steps. In how many distinct ways "
            "can you climb to the top?\n\n"
            "**Example 1:**\n"
            "Input: n = 2\nOutput: 2\n"
            "Explanation: (1+1) or (2)\n\n"
            "**Example 2:**\n"
            "Input: n = 3\nOutput: 3\n"
            "Explanation: (1+1+1), (1+2), (2+1)"
        ),
        "difficulty": "easy",
        "topic": "dynamic_programming",
        "constraints": ["1 <= n <= 45"],
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "Two ways: 1+1 or 2"},
            {"input": "n = 3", "output": "3", "explanation": "Three ways"},
        ],
        "test_cases": [
            {"input": {"n": 1}, "expected_output": 1},
            {"input": {"n": 2}, "expected_output": 2},
            {"input": {"n": 3}, "expected_output": 3},
            {"input": {"n": 4}, "expected_output": 5},
            {"input": {"n": 5}, "expected_output": 8},
            {"input": {"n": 10}, "expected_output": 89},
            {"input": {"n": 20}, "expected_output": 10946},
        ],
        "hints": [
            "This is essentially the Fibonacci sequence. dp[i] = dp[i-1] + dp[i-2].",
            "Base cases: dp[1] = 1, dp[2] = 2.",
            "You only need to keep track of the last two values, so O(1) space is possible.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(1)"},
        "solution_approach": "DP / Fibonacci: ways(n) = ways(n-1) + ways(n-2). Use two variables to track previous values.",
        "starter_code": {
            "python": "def climbStairs(n: int) -> int:\n    pass",
            "javascript": "function climbStairs(n) {\n    \n}",
            "cpp": "class Solution {\npublic:\n    int climbStairs(int n) {\n        \n    }\n};",
        },
        "tags": ["dp", "fibonacci", "memoization"],
    },

    # ======================================================================
    # 7. Binary Search (Easy, Searching)
    # ======================================================================
    {
        "id": "binary-search",
        "title": "Binary Search",
        "description": (
            "Given an array of integers `nums` which is sorted in ascending order, "
            "and an integer `target`, write a function to search `target` in `nums`. "
            "If `target` exists, then return its index. Otherwise, return -1.\n\n"
            "You must write an algorithm with O(log n) runtime complexity.\n\n"
            "**Example 1:**\n"
            "Input: nums = [-1,0,3,5,9,12], target = 9\n"
            "Output: 4\n\n"
            "**Example 2:**\n"
            "Input: nums = [-1,0,3,5,9,12], target = 2\n"
            "Output: -1"
        ),
        "difficulty": "easy",
        "topic": "searching",
        "constraints": [
            "1 <= nums.length <= 10^4",
            "-10^4 < nums[i], target < 10^4",
            "All integers in nums are unique.",
            "nums is sorted in ascending order.",
        ],
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 is at index 4"},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1", "explanation": "2 not in array"},
        ],
        "test_cases": [
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}, "expected_output": 4},
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}, "expected_output": -1},
            {"input": {"nums": [5], "target": 5}, "expected_output": 0},
            {"input": {"nums": [5], "target": -5}, "expected_output": -1},
            {"input": {"nums": [1, 2, 3, 4, 5], "target": 1}, "expected_output": 0},
            {"input": {"nums": [1, 2, 3, 4, 5], "target": 5}, "expected_output": 4},
        ],
        "hints": [
            "Use two pointers: left and right. Calculate mid = (left + right) // 2.",
            "Compare nums[mid] with target. Narrow the search range accordingly.",
            "Be careful with integer overflow when computing mid in some languages.",
        ],
        "optimal_complexity": {"time": "O(log n)", "space": "O(1)"},
        "solution_approach": "Standard binary search with left/right pointers and mid comparison.",
        "starter_code": {
            "python": "def search(nums: list[int], target: int) -> int:\n    pass",
            "javascript": "function search(nums, target) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        \n    }\n};",
        },
        "tags": ["binary-search", "divide-and-conquer"],
    },

    # ======================================================================
    # 8. Maximum Subarray (Medium, Arrays)
    # ======================================================================
    {
        "id": "maximum-subarray",
        "title": "Maximum Subarray",
        "description": (
            "Given an integer array `nums`, find the subarray with the largest sum, "
            "and return its sum.\n\n"
            "A subarray is a contiguous non-empty sequence of elements.\n\n"
            "**Example 1:**\n"
            "Input: nums = [-2,1,-3,4,-1,2,1,-5,4]\n"
            "Output: 6\n"
            "Explanation: The subarray [4,-1,2,1] has the largest sum 6.\n\n"
            "**Example 2:**\n"
            "Input: nums = [1]\n"
            "Output: 1\n\n"
            "**Example 3:**\n"
            "Input: nums = [5,4,-1,7,8]\n"
            "Output: 23"
        ),
        "difficulty": "medium",
        "topic": "arrays",
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
        ],
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "[4,-1,2,1] has sum 6"},
            {"input": "nums = [1]", "output": "1", "explanation": "Single element"},
            {"input": "nums = [5,4,-1,7,8]", "output": "23", "explanation": "Entire array"},
        ],
        "test_cases": [
            {"input": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, "expected_output": 6},
            {"input": {"nums": [1]}, "expected_output": 1},
            {"input": {"nums": [5, 4, -1, 7, 8]}, "expected_output": 23},
            {"input": {"nums": [-1]}, "expected_output": -1},
            {"input": {"nums": [-2, -1]}, "expected_output": -1},
            {"input": {"nums": [1, 2, 3, 4]}, "expected_output": 10},
        ],
        "hints": [
            "Kadane's algorithm: keep a running sum, reset when it goes below 0.",
            "current_sum = max(num, current_sum + num) for each number.",
            "Track the maximum of all current_sum values.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(1)"},
        "solution_approach": "Kadane's algorithm: iterate maintaining current_sum and max_sum. Reset current_sum when extending makes it worse than starting fresh.",
        "starter_code": {
            "python": "def maxSubArray(nums: list[int]) -> int:\n    pass",
            "javascript": "function maxSubArray(nums) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxSubArray(vector<int>& nums) {\n        \n    }\n};",
        },
        "tags": ["kadane", "dp", "greedy"],
    },

    # ======================================================================
    # 9. 3Sum (Medium, Arrays)
    # ======================================================================
    {
        "id": "three-sum",
        "title": "3Sum",
        "description": (
            "Given an integer array `nums`, return all the triplets "
            "`[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and "
            "`j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\n"
            "Notice that the solution set must not contain duplicate triplets.\n\n"
            "**Example 1:**\n"
            "Input: nums = [-1,0,1,2,-1,-4]\n"
            "Output: [[-1,-1,2],[-1,0,1]]\n\n"
            "**Example 2:**\n"
            "Input: nums = [0,1,1]\n"
            "Output: []\n\n"
            "**Example 3:**\n"
            "Input: nums = [0,0,0]\n"
            "Output: [[0,0,0]]"
        ),
        "difficulty": "medium",
        "topic": "arrays",
        "constraints": [
            "3 <= nums.length <= 3000",
            "-10^5 <= nums[i] <= 10^5",
        ],
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "Two unique triplets"},
            {"input": "nums = [0,1,1]", "output": "[]", "explanation": "No triplet sums to 0"},
            {"input": "nums = [0,0,0]", "output": "[[0,0,0]]", "explanation": "Triple zero"},
        ],
        "test_cases": [
            {"input": {"nums": [-1, 0, 1, 2, -1, -4]}, "expected_output": [[-1, -1, 2], [-1, 0, 1]]},
            {"input": {"nums": [0, 1, 1]}, "expected_output": []},
            {"input": {"nums": [0, 0, 0]}, "expected_output": [[0, 0, 0]]},
            {"input": {"nums": [0, 0, 0, 0]}, "expected_output": [[0, 0, 0]]},
            {"input": {"nums": [-2, 0, 1, 1, 2]}, "expected_output": [[-2, 0, 2], [-2, 1, 1]]},
        ],
        "hints": [
            "Sort the array first. This enables the two-pointer technique.",
            "Fix one element and use two pointers for the remaining two.",
            "Skip duplicates to avoid duplicate triplets.",
        ],
        "optimal_complexity": {"time": "O(n²)", "space": "O(1) ignoring output"},
        "solution_approach": "Sort, then for each i, use two pointers (lo, hi) to find pairs that sum to -nums[i]. Skip duplicates.",
        "starter_code": {
            "python": "def threeSum(nums: list[int]) -> list[list[int]]:\n    pass",
            "javascript": "function threeSum(nums) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> threeSum(vector<int>& nums) {\n        \n    }\n};",
        },
        "tags": ["two-pointer", "sorting", "dedup"],
    },

    # ======================================================================
    # 10. Longest Substring Without Repeating Characters (Medium, Strings)
    # ======================================================================
    {
        "id": "longest-substring-no-repeat",
        "title": "Longest Substring Without Repeating Characters",
        "description": (
            "Given a string `s`, find the length of the longest substring without "
            "repeating characters.\n\n"
            "**Example 1:**\n"
            "Input: s = \"abcabcbb\"\nOutput: 3\n"
            "Explanation: \"abc\" is the longest substring.\n\n"
            "**Example 2:**\n"
            "Input: s = \"bbbbb\"\nOutput: 1\n\n"
            "**Example 3:**\n"
            "Input: s = \"pwwkew\"\nOutput: 3\n"
            "Explanation: \"wke\" is the longest substring."
        ),
        "difficulty": "medium",
        "topic": "strings",
        "constraints": [
            "0 <= s.length <= 5 * 10^4",
            "s consists of English letters, digits, symbols and spaces.",
        ],
        "examples": [
            {"input": 's = "abcabcbb"', "output": "3", "explanation": "abc"},
            {"input": 's = "bbbbb"', "output": "1", "explanation": "b"},
            {"input": 's = "pwwkew"', "output": "3", "explanation": "wke"},
        ],
        "test_cases": [
            {"input": {"s": "abcabcbb"}, "expected_output": 3},
            {"input": {"s": "bbbbb"}, "expected_output": 1},
            {"input": {"s": "pwwkew"}, "expected_output": 3},
            {"input": {"s": ""}, "expected_output": 0},
            {"input": {"s": " "}, "expected_output": 1},
            {"input": {"s": "dvdf"}, "expected_output": 3},
            {"input": {"s": "abcdef"}, "expected_output": 6},
        ],
        "hints": [
            "Use a sliding window approach with two pointers.",
            "Use a set or hash map to track characters in the current window.",
            "When you find a duplicate, shrink the window from the left.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(min(m, n)) where m is charset size"},
        "solution_approach": "Sliding window with a hash set. Expand right, if duplicate found, shrink left until no duplicates.",
        "starter_code": {
            "python": "def lengthOfLongestSubstring(s: str) -> int:\n    pass",
            "javascript": "function lengthOfLongestSubstring(s) {\n    \n}",
            "cpp": "#include <string>\n#include <unordered_set>\nusing namespace std;\n\nclass Solution {\npublic:\n    int lengthOfLongestSubstring(string s) {\n        \n    }\n};",
        },
        "tags": ["sliding-window", "hash-set", "two-pointer"],
    },

    # ======================================================================
    # 11. Container With Most Water (Medium, Arrays)
    # ======================================================================
    {
        "id": "container-with-most-water",
        "title": "Container With Most Water",
        "description": (
            "You are given an integer array `height` of length `n`. There are `n` "
            "vertical lines drawn such that the two endpoints of the i-th line are "
            "(i, 0) and (i, height[i]).\n\n"
            "Find two lines that together with the x-axis form a container that "
            "holds the most water.\n\n"
            "Return the maximum amount of water a container can store.\n\n"
            "**Example 1:**\n"
            "Input: height = [1,8,6,2,5,4,8,3,7]\n"
            "Output: 49\n\n"
            "**Example 2:**\n"
            "Input: height = [1,1]\n"
            "Output: 1"
        ),
        "difficulty": "medium",
        "topic": "arrays",
        "constraints": [
            "n == height.length",
            "2 <= n <= 10^5",
            "0 <= height[i] <= 10^4",
        ],
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49", "explanation": "Lines at index 1 and 8"},
            {"input": "height = [1,1]", "output": "1", "explanation": "Only one container possible"},
        ],
        "test_cases": [
            {"input": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}, "expected_output": 49},
            {"input": {"height": [1, 1]}, "expected_output": 1},
            {"input": {"height": [4, 3, 2, 1, 4]}, "expected_output": 16},
            {"input": {"height": [1, 2, 1]}, "expected_output": 2},
            {"input": {"height": [2, 3, 10, 5, 7, 8, 9]}, "expected_output": 36},
        ],
        "hints": [
            "Use two pointers, one at each end of the array.",
            "Calculate area = min(height[left], height[right]) * (right - left).",
            "Move the pointer pointing to the shorter line inward.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(1)"},
        "solution_approach": "Two pointers from ends. Compute area, move the shorter side inward. Greedy reasoning: moving the taller side can only decrease width without guaranteed height increase.",
        "starter_code": {
            "python": "def maxArea(height: list[int]) -> int:\n    pass",
            "javascript": "function maxArea(height) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxArea(vector<int>& height) {\n        \n    }\n};",
        },
        "tags": ["two-pointer", "greedy"],
    },

    # ======================================================================
    # 12. Group Anagrams (Medium, Strings)
    # ======================================================================
    {
        "id": "group-anagrams",
        "title": "Group Anagrams",
        "description": (
            "Given an array of strings `strs`, group the anagrams together. "
            "You can return the answer in any order.\n\n"
            "An anagram is a word formed by rearranging the letters of another word.\n\n"
            "**Example 1:**\n"
            "Input: strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]\n"
            "Output: [[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]\n\n"
            "**Example 2:**\n"
            "Input: strs = [\"\"]\n"
            "Output: [[\"\"]]\n\n"
            "**Example 3:**\n"
            "Input: strs = [\"a\"]\n"
            "Output: [[\"a\"]]"
        ),
        "difficulty": "medium",
        "topic": "strings",
        "constraints": [
            "1 <= strs.length <= 10^4",
            "0 <= strs[i].length <= 100",
            "strs[i] consists of lowercase English letters.",
        ],
        "examples": [
            {"input": 'strs = ["eat","tea","tan","ate","nat","bat"]', "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]', "explanation": "Grouped by sorted letters"},
        ],
        "test_cases": [
            {"input": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}, "expected_output": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]},
            {"input": {"strs": [""]}, "expected_output": [[""]]},
            {"input": {"strs": ["a"]}, "expected_output": [["a"]]},
            {"input": {"strs": ["abc", "bca", "cab", "xyz", "zyx"]}, "expected_output": [["abc", "bca", "cab"], ["xyz", "zyx"]]},
            {"input": {"strs": ["a", "b", "c"]}, "expected_output": [["a"], ["b"], ["c"]]},
        ],
        "hints": [
            "Two strings are anagrams if their sorted versions are equal.",
            "Use sorted string as a hash map key to group anagrams.",
            "Alternatively, use a character count tuple as the key for O(n*k) time.",
        ],
        "optimal_complexity": {"time": "O(n * k log k) or O(n * k)", "space": "O(n * k)"},
        "solution_approach": "Hash map with sorted(word) as key. Group all words with the same sorted key.",
        "starter_code": {
            "python": "def groupAnagrams(strs: list[str]) -> list[list[str]]:\n    pass",
            "javascript": "function groupAnagrams(strs) {\n    \n}",
            "cpp": "#include <vector>\n#include <string>\n#include <unordered_map>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<string>> groupAnagrams(vector<string>& strs) {\n        \n    }\n};",
        },
        "tags": ["hash-map", "sorting", "string-manipulation"],
    },

    # ======================================================================
    # 13. Number of Islands (Medium, Graphs)
    # ======================================================================
    {
        "id": "number-of-islands",
        "title": "Number of Islands",
        "description": (
            "Given an m x n 2D binary grid `grid` which represents a map of '1's "
            "(land) and '0's (water), return the number of islands.\n\n"
            "An island is surrounded by water and is formed by connecting adjacent "
            "lands horizontally or vertically. You may assume all four edges of "
            "the grid are surrounded by water.\n\n"
            "**Example 1:**\n"
            "Input: grid = [\n"
            '  ["1","1","1","1","0"],\n'
            '  ["1","1","0","1","0"],\n'
            '  ["1","1","0","0","0"],\n'
            '  ["0","0","0","0","0"]\n'
            "]\nOutput: 1\n\n"
            "**Example 2:**\n"
            "Input: grid = [\n"
            '  ["1","1","0","0","0"],\n'
            '  ["1","1","0","0","0"],\n'
            '  ["0","0","1","0","0"],\n'
            '  ["0","0","0","1","1"]\n'
            "]\nOutput: 3"
        ),
        "difficulty": "medium",
        "topic": "graphs",
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 <= m, n <= 300",
            "grid[i][j] is '0' or '1'.",
        ],
        "examples": [
            {"input": "4x5 grid with one island", "output": "1", "explanation": "All land is connected"},
            {"input": "4x5 grid with three islands", "output": "3", "explanation": "Three disconnected land masses"},
        ],
        "test_cases": [
            {"input": {"grid": [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]}, "expected_output": 1},
            {"input": {"grid": [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]}, "expected_output": 3},
            {"input": {"grid": [["0"]]}, "expected_output": 0},
            {"input": {"grid": [["1"]]}, "expected_output": 1},
            {"input": {"grid": [["1","0"],["0","1"]]}, "expected_output": 2},
        ],
        "hints": [
            "Use DFS or BFS to explore and mark all connected land cells.",
            "When you find a '1', increment island count and mark all connected '1's as visited.",
            "You can mark visited cells by setting them to '0' to avoid extra space.",
        ],
        "optimal_complexity": {"time": "O(m * n)", "space": "O(m * n) worst case for DFS stack"},
        "solution_approach": "Iterate grid; when '1' found, BFS/DFS flood-fill to mark entire island, increment count.",
        "starter_code": {
            "python": "def numIslands(grid: list[list[str]]) -> int:\n    pass",
            "javascript": "function numIslands(grid) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    int numIslands(vector<vector<char>>& grid) {\n        \n    }\n};",
        },
        "tags": ["dfs", "bfs", "flood-fill", "graph-traversal"],
    },

    # ======================================================================
    # 14. Course Schedule (Medium, Graphs)
    # ======================================================================
    {
        "id": "course-schedule",
        "title": "Course Schedule",
        "description": (
            "There are a total of `numCourses` courses you have to take, labeled "
            "from 0 to numCourses - 1. You are given an array `prerequisites` where "
            "prerequisites[i] = [ai, bi] indicates that you must take course bi "
            "first if you want to take course ai.\n\n"
            "Return true if you can finish all courses. Otherwise, return false.\n\n"
            "**Example 1:**\n"
            "Input: numCourses = 2, prerequisites = [[1,0]]\n"
            "Output: true\n\n"
            "**Example 2:**\n"
            "Input: numCourses = 2, prerequisites = [[1,0],[0,1]]\n"
            "Output: false\n"
            "Explanation: Circular dependency."
        ),
        "difficulty": "medium",
        "topic": "graphs",
        "constraints": [
            "1 <= numCourses <= 2000",
            "0 <= prerequisites.length <= 5000",
            "prerequisites[i].length == 2",
            "0 <= ai, bi < numCourses",
        ],
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "true", "explanation": "Take 0 then 1"},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "false", "explanation": "Cycle"},
        ],
        "test_cases": [
            {"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "expected_output": True},
            {"input": {"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]}, "expected_output": False},
            {"input": {"numCourses": 1, "prerequisites": []}, "expected_output": True},
            {"input": {"numCourses": 3, "prerequisites": [[1, 0], [2, 1]]}, "expected_output": True},
            {"input": {"numCourses": 3, "prerequisites": [[0, 1], [1, 2], [2, 0]]}, "expected_output": False},
        ],
        "hints": [
            "This is a cycle detection problem in a directed graph.",
            "Use topological sort (BFS with in-degree) or DFS with coloring.",
            "If all nodes can be visited in topological order, there's no cycle.",
        ],
        "optimal_complexity": {"time": "O(V + E)", "space": "O(V + E)"},
        "solution_approach": "Topological sort using Kahn's algorithm (BFS with in-degree). If all nodes processed, return true.",
        "starter_code": {
            "python": "def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:\n    pass",
            "javascript": "function canFinish(numCourses, prerequisites) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {\n        \n    }\n};",
        },
        "tags": ["topological-sort", "dfs", "bfs", "cycle-detection"],
    },

    # ======================================================================
    # 15. Coin Change (Medium, DP)
    # ======================================================================
    {
        "id": "coin-change",
        "title": "Coin Change",
        "description": (
            "You are given an integer array `coins` representing coins of different "
            "denominations and an integer `amount` representing a total amount of money.\n\n"
            "Return the fewest number of coins that you need to make up that amount. "
            "If that amount cannot be made up by any combination, return -1.\n\n"
            "You may assume that you have an infinite number of each kind of coin.\n\n"
            "**Example 1:**\n"
            "Input: coins = [1,5,10,25], amount = 30\n"
            "Output: 2\nExplanation: 5 + 25 = 30\n\n"
            "**Example 2:**\n"
            "Input: coins = [2], amount = 3\n"
            "Output: -1\n\n"
            "**Example 3:**\n"
            "Input: coins = [1], amount = 0\n"
            "Output: 0"
        ),
        "difficulty": "medium",
        "topic": "dynamic_programming",
        "constraints": [
            "1 <= coins.length <= 12",
            "1 <= coins[i] <= 2^31 - 1",
            "0 <= amount <= 10^4",
        ],
        "examples": [
            {"input": "coins = [1,5,10,25], amount = 30", "output": "2", "explanation": "25 + 5"},
            {"input": "coins = [2], amount = 3", "output": "-1", "explanation": "Not possible"},
        ],
        "test_cases": [
            {"input": {"coins": [1, 5, 10, 25], "amount": 30}, "expected_output": 2},
            {"input": {"coins": [2], "amount": 3}, "expected_output": -1},
            {"input": {"coins": [1], "amount": 0}, "expected_output": 0},
            {"input": {"coins": [1, 2, 5], "amount": 11}, "expected_output": 3},
            {"input": {"coins": [1], "amount": 1}, "expected_output": 1},
            {"input": {"coins": [1], "amount": 2}, "expected_output": 2},
        ],
        "hints": [
            "Use bottom-up DP. dp[i] = minimum coins to make amount i.",
            "For each amount, try every coin and take the minimum.",
            "dp[i] = min(dp[i - coin] + 1) for all valid coins. Initialize dp[0] = 0.",
        ],
        "optimal_complexity": {"time": "O(amount * len(coins))", "space": "O(amount)"},
        "solution_approach": "Bottom-up DP: dp array of size amount+1, initialize to infinity except dp[0]=0. For each amount, try each coin.",
        "starter_code": {
            "python": "def coinChange(coins: list[int], amount: int) -> int:\n    pass",
            "javascript": "function coinChange(coins, amount) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    int coinChange(vector<int>& coins, int amount) {\n        \n    }\n};",
        },
        "tags": ["dp", "bottom-up", "unbounded-knapsack"],
    },

    # ======================================================================
    # 16. Kth Largest Element in an Array (Medium, Heaps)
    # ======================================================================
    {
        "id": "kth-largest-element",
        "title": "Kth Largest Element in an Array",
        "description": (
            "Given an integer array `nums` and an integer `k`, return the kth "
            "largest element in the array.\n\n"
            "Note that it is the kth largest element in the sorted order, not the "
            "kth distinct element.\n\n"
            "Can you solve it without sorting?\n\n"
            "**Example 1:**\n"
            "Input: nums = [3,2,1,5,6,4], k = 2\n"
            "Output: 5\n\n"
            "**Example 2:**\n"
            "Input: nums = [3,2,3,1,2,4,5,5,6], k = 4\n"
            "Output: 4"
        ),
        "difficulty": "medium",
        "topic": "heaps",
        "constraints": [
            "1 <= k <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
        ],
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5", "explanation": "Sorted: [1,2,3,4,5,6], 2nd largest is 5"},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4", "explanation": "4th largest"},
        ],
        "test_cases": [
            {"input": {"nums": [3, 2, 1, 5, 6, 4], "k": 2}, "expected_output": 5},
            {"input": {"nums": [3, 2, 3, 1, 2, 4, 5, 5, 6], "k": 4}, "expected_output": 4},
            {"input": {"nums": [1], "k": 1}, "expected_output": 1},
            {"input": {"nums": [7, 6, 5, 4, 3, 2, 1], "k": 5}, "expected_output": 3},
            {"input": {"nums": [2, 1], "k": 2}, "expected_output": 1},
        ],
        "hints": [
            "Use a min-heap of size k. The root will be the kth largest.",
            "Alternatively, use Quickselect for average O(n) time.",
            "Python's heapq module is a min-heap by default.",
        ],
        "optimal_complexity": {"time": "O(n) average (Quickselect) or O(n log k) (heap)", "space": "O(k)"},
        "solution_approach": "Min-heap of size k: push elements, if heap size > k pop the min. Final heap root is answer. Or use Quickselect.",
        "starter_code": {
            "python": "def findKthLargest(nums: list[int], k: int) -> int:\n    pass",
            "javascript": "function findKthLargest(nums, k) {\n    \n}",
            "cpp": "#include <vector>\n#include <queue>\nusing namespace std;\n\nclass Solution {\npublic:\n    int findKthLargest(vector<int>& nums, int k) {\n        \n    }\n};",
        },
        "tags": ["heap", "quickselect", "priority-queue"],
    },

    # ======================================================================
    # 17. Merge Intervals (Medium, Sorting)
    # ======================================================================
    {
        "id": "merge-intervals",
        "title": "Merge Intervals",
        "description": (
            "Given an array of `intervals` where intervals[i] = [start_i, end_i], "
            "merge all overlapping intervals, and return an array of the non-overlapping "
            "intervals that cover all the intervals in the input.\n\n"
            "**Example 1:**\n"
            "Input: intervals = [[1,3],[2,6],[8,10],[15,18]]\n"
            "Output: [[1,6],[8,10],[15,18]]\n\n"
            "**Example 2:**\n"
            "Input: intervals = [[1,4],[4,5]]\n"
            "Output: [[1,5]]"
        ),
        "difficulty": "medium",
        "topic": "sorting",
        "constraints": [
            "1 <= intervals.length <= 10^4",
            "intervals[i].length == 2",
            "0 <= start_i <= end_i <= 10^4",
        ],
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "[1,3] and [2,6] overlap"},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Touch at boundary"},
        ],
        "test_cases": [
            {"input": {"intervals": [[1,3],[2,6],[8,10],[15,18]]}, "expected_output": [[1,6],[8,10],[15,18]]},
            {"input": {"intervals": [[1,4],[4,5]]}, "expected_output": [[1,5]]},
            {"input": {"intervals": [[1,4],[0,4]]}, "expected_output": [[0,4]]},
            {"input": {"intervals": [[1,4],[2,3]]}, "expected_output": [[1,4]]},
            {"input": {"intervals": [[1,2]]}, "expected_output": [[1,2]]},
        ],
        "hints": [
            "Sort the intervals by start time.",
            "Iterate and check if current interval overlaps with the last merged one.",
            "If they overlap, merge by updating the end to max(end1, end2).",
        ],
        "optimal_complexity": {"time": "O(n log n)", "space": "O(n)"},
        "solution_approach": "Sort by start. Iterate: if current overlaps with last merged, extend end. Otherwise, append as new interval.",
        "starter_code": {
            "python": "def merge(intervals: list[list[int]]) -> list[list[int]]:\n    pass",
            "javascript": "function merge(intervals) {\n    \n}",
            "cpp": "#include <vector>\n#include <algorithm>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> merge(vector<vector<int>>& intervals) {\n        \n    }\n};",
        },
        "tags": ["sorting", "intervals", "merging"],
    },

    # ======================================================================
    # 18. Word Break (Medium, DP)
    # ======================================================================
    {
        "id": "word-break",
        "title": "Word Break",
        "description": (
            "Given a string `s` and a dictionary of strings `wordDict`, return true "
            "if `s` can be segmented into a space-separated sequence of one or more "
            "dictionary words.\n\n"
            "Note that the same word in the dictionary may be reused multiple times.\n\n"
            "**Example 1:**\n"
            "Input: s = \"leetcode\", wordDict = [\"leet\",\"code\"]\n"
            "Output: true\n\n"
            "**Example 2:**\n"
            "Input: s = \"applepenapple\", wordDict = [\"apple\",\"pen\"]\n"
            "Output: true\n\n"
            "**Example 3:**\n"
            "Input: s = \"catsandog\", wordDict = [\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]\n"
            "Output: false"
        ),
        "difficulty": "medium",
        "topic": "dynamic_programming",
        "constraints": [
            "1 <= s.length <= 300",
            "1 <= wordDict.length <= 1000",
            "1 <= wordDict[i].length <= 20",
            "s and wordDict[i] consist of only lowercase English letters.",
        ],
        "examples": [
            {"input": 's = "leetcode", wordDict = ["leet","code"]', "output": "true", "explanation": "leet + code"},
            {"input": 's = "applepenapple", wordDict = ["apple","pen"]', "output": "true", "explanation": "apple + pen + apple"},
        ],
        "test_cases": [
            {"input": {"s": "leetcode", "wordDict": ["leet", "code"]}, "expected_output": True},
            {"input": {"s": "applepenapple", "wordDict": ["apple", "pen"]}, "expected_output": True},
            {"input": {"s": "catsandog", "wordDict": ["cats", "dog", "sand", "and", "cat"]}, "expected_output": False},
            {"input": {"s": "a", "wordDict": ["a"]}, "expected_output": True},
            {"input": {"s": "ab", "wordDict": ["a", "b"]}, "expected_output": True},
            {"input": {"s": "bb", "wordDict": ["a", "b", "bbb", "bbbb"]}, "expected_output": True},
        ],
        "hints": [
            "Use DP where dp[i] means s[:i] can be segmented.",
            "For each position i, check all words in dict to see if s[i-len(word):i] matches.",
            "dp[0] = True (empty string). Answer is dp[len(s)].",
        ],
        "optimal_complexity": {"time": "O(n² * m) or O(n * m * k)", "space": "O(n)"},
        "solution_approach": "DP: dp[i] = True if s[:i] can be segmented. For each i, check if any word ends at position i and dp[i-len(word)] is True.",
        "starter_code": {
            "python": "def wordBreak(s: str, wordDict: list[str]) -> bool:\n    pass",
            "javascript": "function wordBreak(s, wordDict) {\n    \n}",
            "cpp": "#include <string>\n#include <vector>\n#include <unordered_set>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool wordBreak(string s, vector<string>& wordDict) {\n        \n    }\n};",
        },
        "tags": ["dp", "string", "hash-set"],
    },

    # ======================================================================
    # 19. Trapping Rain Water (Hard, Arrays)
    # ======================================================================
    {
        "id": "trapping-rain-water",
        "title": "Trapping Rain Water",
        "description": (
            "Given `n` non-negative integers representing an elevation map where the "
            "width of each bar is 1, compute how much water it can trap after raining.\n\n"
            "**Example 1:**\n"
            "Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]\n"
            "Output: 6\n"
            "Explanation: 6 units of rain water are trapped.\n\n"
            "**Example 2:**\n"
            "Input: height = [4,2,0,3,2,5]\n"
            "Output: 9"
        ),
        "difficulty": "hard",
        "topic": "arrays",
        "constraints": [
            "n == height.length",
            "1 <= n <= 2 * 10^4",
            "0 <= height[i] <= 10^5",
        ],
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "6 units trapped"},
            {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": "9 units trapped"},
        ],
        "test_cases": [
            {"input": {"height": [0,1,0,2,1,0,1,3,2,1,2,1]}, "expected_output": 6},
            {"input": {"height": [4,2,0,3,2,5]}, "expected_output": 9},
            {"input": {"height": [1,2,3,4,5]}, "expected_output": 0},
            {"input": {"height": [5,4,3,2,1]}, "expected_output": 0},
            {"input": {"height": [0]}, "expected_output": 0},
            {"input": {"height": [3,0,3]}, "expected_output": 3},
        ],
        "hints": [
            "Water at each position = min(max_left, max_right) - height[i].",
            "You can precompute max_left and max_right arrays.",
            "Or use a two-pointer approach for O(1) space.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(1) with two pointers"},
        "solution_approach": "Two-pointer: maintain left_max and right_max. Process the side with smaller max first, accumulate water.",
        "starter_code": {
            "python": "def trap(height: list[int]) -> int:\n    pass",
            "javascript": "function trap(height) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    int trap(vector<int>& height) {\n        \n    }\n};",
        },
        "tags": ["two-pointer", "stack", "dynamic-programming"],
    },

    # ======================================================================
    # 20. Median of Two Sorted Arrays (Hard, Arrays)
    # ======================================================================
    {
        "id": "median-two-sorted-arrays",
        "title": "Median of Two Sorted Arrays",
        "description": (
            "Given two sorted arrays `nums1` and `nums2` of size m and n respectively, "
            "return the median of the two sorted arrays.\n\n"
            "The overall run time complexity should be O(log(m+n)).\n\n"
            "**Example 1:**\n"
            "Input: nums1 = [1,3], nums2 = [2]\n"
            "Output: 2.0\n\n"
            "**Example 2:**\n"
            "Input: nums1 = [1,2], nums2 = [3,4]\n"
            "Output: 2.5\n"
            "Explanation: merged = [1,2,3,4], median = (2+3)/2 = 2.5"
        ),
        "difficulty": "hard",
        "topic": "arrays",
        "constraints": [
            "nums1.length == m",
            "nums2.length == n",
            "0 <= m <= 1000",
            "0 <= n <= 1000",
            "1 <= m + n <= 2000",
            "-10^6 <= nums1[i], nums2[i] <= 10^6",
        ],
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.0", "explanation": "Merged: [1,2,3]"},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.5", "explanation": "Merged: [1,2,3,4]"},
        ],
        "test_cases": [
            {"input": {"nums1": [1, 3], "nums2": [2]}, "expected_output": 2.0},
            {"input": {"nums1": [1, 2], "nums2": [3, 4]}, "expected_output": 2.5},
            {"input": {"nums1": [], "nums2": [1]}, "expected_output": 1.0},
            {"input": {"nums1": [2], "nums2": []}, "expected_output": 2.0},
            {"input": {"nums1": [1, 2, 3], "nums2": [4, 5, 6]}, "expected_output": 3.5},
            {"input": {"nums1": [1], "nums2": [2, 3, 4, 5, 6]}, "expected_output": 3.5},
        ],
        "hints": [
            "Binary search on the shorter array to find the correct partition.",
            "Partition both arrays such that left halves combined have half the total elements.",
            "Ensure maxLeft1 <= minRight2 and maxLeft2 <= minRight1.",
        ],
        "optimal_complexity": {"time": "O(log(min(m,n)))", "space": "O(1)"},
        "solution_approach": "Binary search on the shorter array. Find partition where all left elements ≤ all right elements. Compute median from partition boundary values.",
        "starter_code": {
            "python": "def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:\n    pass",
            "javascript": "function findMedianSortedArrays(nums1, nums2) {\n    \n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {\n        \n    }\n};",
        },
        "tags": ["binary-search", "divide-and-conquer", "partition"],
    },

    # ======================================================================
    # 21. Serialize and Deserialize Binary Tree (Hard, Trees)
    # ======================================================================
    {
        "id": "serialize-deserialize-tree",
        "title": "Serialize and Deserialize Binary Tree",
        "description": (
            "Design an algorithm to serialize and deserialize a binary tree. "
            "Serialization is converting a tree to a string. Deserialization is "
            "reconstructing the tree from the string.\n\n"
            "The tree is represented as a list in level-order traversal where None "
            "represents empty nodes.\n\n"
            "**Example 1:**\n"
            "Input: root = [1,2,3,null,null,4,5]\n"
            "Serialized: \"1,2,3,null,null,4,5\"\n"
            "Deserialized back to: [1,2,3,null,null,4,5]\n\n"
            "**Example 2:**\n"
            "Input: root = []\n"
            "Serialized: \"\"\n"
            "Deserialized back to: []"
        ),
        "difficulty": "hard",
        "topic": "trees",
        "constraints": [
            "The number of nodes is in the range [0, 10^4].",
            "-1000 <= Node.val <= 1000",
        ],
        "examples": [
            {"input": "root = [1,2,3,null,null,4,5]", "output": "\"1,2,3,null,null,4,5\"", "explanation": "Level-order serialization"},
        ],
        "test_cases": [
            {"input": {"root": [1, 2, 3, None, None, 4, 5]}, "expected_output": [1, 2, 3, None, None, 4, 5]},
            {"input": {"root": []}, "expected_output": []},
            {"input": {"root": [1]}, "expected_output": [1]},
            {"input": {"root": [1, 2]}, "expected_output": [1, 2]},
            {"input": {"root": [1, None, 3]}, "expected_output": [1, None, 3]},
        ],
        "hints": [
            "Use BFS (level-order traversal) for serialization.",
            "Represent null nodes explicitly in the serialized string.",
            "For deserialization, use a queue to rebuild the tree level by level.",
        ],
        "optimal_complexity": {"time": "O(n)", "space": "O(n)"},
        "solution_approach": "BFS serialize: queue-based level-order, output values and 'null' markers. Deserialize: parse tokens, rebuild with queue.",
        "starter_code": {
            "python": (
                "# Using lists to represent trees in level-order\n"
                "def serialize(root: list) -> str:\n    pass\n\n"
                "def deserialize(data: str) -> list:\n    pass"
            ),
            "javascript": "function serialize(root) {\n    \n}\n\nfunction deserialize(data) {\n    \n}",
            "cpp": "#include <string>\n#include <vector>\nusing namespace std;\n\nclass Codec {\npublic:\n    string serialize(vector<int>& root) {\n        \n    }\n    vector<int> deserialize(string data) {\n        \n    }\n};",
        },
        "tags": ["tree", "bfs", "serialization", "design"],
    },

    # ======================================================================
    # 22. LRU Cache (Hard, Linked Lists / Design)
    # ======================================================================
    {
        "id": "lru-cache",
        "title": "LRU Cache",
        "description": (
            "Design a data structure that follows the constraints of a Least Recently "
            "Used (LRU) cache.\n\n"
            "Implement the LRUCache class:\n"
            "- `LRUCache(int capacity)` Initialize the cache with positive size capacity.\n"
            "- `int get(int key)` Return the value of the key if it exists, otherwise -1.\n"
            "- `void put(int key, int value)` Update or insert the value. When the cache "
            "reaches its capacity, evict the least recently used key.\n\n"
            "The functions get and put must each run in O(1) average time.\n\n"
            "**Example:**\n"
            "Input:\n"
            "[\"LRUCache\", \"put\", \"put\", \"get\", \"put\", \"get\", \"put\", \"get\", \"get\", \"get\"]\n"
            "[[2], [1,1], [2,2], [1], [3,3], [2], [4,4], [1], [3], [4]]\n"
            "Output: [null, null, null, 1, null, -1, null, -1, 3, 4]"
        ),
        "difficulty": "hard",
        "topic": "linked_lists",
        "constraints": [
            "1 <= capacity <= 3000",
            "0 <= key <= 10^4",
            "0 <= value <= 10^5",
            "At most 2 * 10^5 calls to get and put.",
        ],
        "examples": [
            {
                "input": "operations = [\"LRUCache\",\"put\",\"put\",\"get\",\"put\",\"get\",\"put\",\"get\",\"get\",\"get\"], args = [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]",
                "output": "[null, null, null, 1, null, -1, null, -1, 3, 4]",
                "explanation": "Standard LRU eviction behavior",
            },
        ],
        "test_cases": [
            {
                "input": {
                    "operations": ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
                    "args": [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
                },
                "expected_output": [None, None, None, 1, None, -1, None, -1, 3, 4],
            },
            {
                "input": {
                    "operations": ["LRUCache", "put", "get", "put", "get", "get"],
                    "args": [[1], [2, 1], [2], [3, 2], [2], [3]],
                },
                "expected_output": [None, None, 1, None, -1, 2],
            },
            {
                "input": {
                    "operations": ["LRUCache", "put", "put", "put", "get", "get"],
                    "args": [[2], [1, 1], [2, 2], [3, 3], [1], [3]],
                },
                "expected_output": [None, None, None, None, -1, 3],
            },
            {
                "input": {
                    "operations": ["LRUCache", "get"],
                    "args": [[1], [1]],
                },
                "expected_output": [None, -1],
            },
            {
                "input": {
                    "operations": ["LRUCache", "put", "put", "get", "put", "put", "get"],
                    "args": [[2], [2, 1], [2, 2], [2], [1, 1], [4, 1], [2]],
                },
                "expected_output": [None, None, None, 2, None, None, -1],
            },
        ],
        "hints": [
            "Use a hash map for O(1) lookup and a doubly linked list for O(1) insertion/deletion.",
            "The most recently used item goes to the head; the least recently used is at the tail.",
            "On get(): move the accessed node to head. On put(): insert at head, evict tail if capacity exceeded.",
        ],
        "optimal_complexity": {"time": "O(1) per operation", "space": "O(capacity)"},
        "solution_approach": "OrderedDict in Python, or HashMap + doubly linked list. Move-to-front on access, evict from tail on overflow.",
        "starter_code": {
            "python": (
                "class LRUCache:\n"
                "    def __init__(self, capacity: int):\n        pass\n\n"
                "    def get(self, key: int) -> int:\n        pass\n\n"
                "    def put(self, key: int, value: int) -> None:\n        pass"
            ),
            "javascript": (
                "class LRUCache {\n"
                "    constructor(capacity) {\n        \n    }\n\n"
                "    get(key) {\n        \n    }\n\n"
                "    put(key, value) {\n        \n    }\n}"
            ),
            "cpp": (
                "#include <unordered_map>\n#include <list>\nusing namespace std;\n\n"
                "class LRUCache {\npublic:\n"
                "    LRUCache(int capacity) {\n        \n    }\n\n"
                "    int get(int key) {\n        \n    }\n\n"
                "    void put(int key, int value) {\n        \n    }\n};"
            ),
        },
        "tags": ["design", "hash-map", "doubly-linked-list", "lru"],
    },
]


# ---------------------------------------------------------------------------
# Build lookup indices
# ---------------------------------------------------------------------------

_BY_ID: dict[str, dict] = {q["id"]: q for q in QUESTIONS}
_BY_TOPIC: dict[str, list[dict]] = {}
_BY_DIFFICULTY: dict[str, list[dict]] = {}

for _q in QUESTIONS:
    _BY_TOPIC.setdefault(_q["topic"], []).append(_q)
    _BY_DIFFICULTY.setdefault(_q["difficulty"], []).append(_q)


# ---------------------------------------------------------------------------
# Public API functions
# ---------------------------------------------------------------------------

def get_question(question_id: str) -> Optional[dict]:
    """Return a question by its unique id, or None if not found."""
    return _BY_ID.get(question_id)


def get_questions_by_topic(topic: str, difficulty: Optional[str] = None) -> list[dict]:
    """Return all questions for a given topic, optionally filtered by difficulty."""
    questions = _BY_TOPIC.get(topic, [])
    if difficulty:
        questions = [q for q in questions if q["difficulty"] == difficulty]
    return questions


def get_questions_by_difficulty(difficulty: str) -> list[dict]:
    """Return all questions of a given difficulty level."""
    return _BY_DIFFICULTY.get(difficulty, [])


def get_all_topics() -> list[str]:
    """Return all available topics."""
    return sorted(_BY_TOPIC.keys())


def get_all_question_ids() -> list[str]:
    """Return all question IDs."""
    return [q["id"] for q in QUESTIONS]


def select_next_question(
    topic_scores: dict[str, float],
    attempted_ids: list[str],
    preferred_topics: Optional[list[str]] = None,
) -> Optional[dict]:
    """
    Adaptively select the next question based on user performance.

    Algorithm:
      1. Filter out already attempted questions.
      2. If preferred_topics are given, favour them.
      3. Pick the weakest topic (lowest score) first.
      4. Within that topic, pick the easiest unattempted question if score is low,
         or a harder one if score is high.
      5. If all questions in weak topics are attempted, fall back to any unattempted.

    Args:
        topic_scores: mapping of topic -> performance score (0-100)
        attempted_ids: list of already attempted question ids
        preferred_topics: optional list of topics the user wants to practice

    Returns:
        A question dict, or None if all questions exhausted.
    """
    attempted_set = set(attempted_ids)
    available = [q for q in QUESTIONS if q["id"] not in attempted_set]

    if not available:
        return None

    # Build per-topic available questions
    topic_available: dict[str, list[dict]] = {}
    for q in available:
        topic_available.setdefault(q["topic"], []).append(q)

    # Filter to preferred topics if provided and available
    if preferred_topics:
        preferred_available = {
            t: qs for t, qs in topic_available.items() if t in preferred_topics
        }
        if preferred_available:
            topic_available = preferred_available

    if not topic_available:
        # All preferred topics exhausted, use any available
        topic_available = {}
        for q in available:
            topic_available.setdefault(q["topic"], []).append(q)

    # Find weakest topic
    topic_list = list(topic_available.keys())
    if topic_scores:
        # Sort by score ascending (weakest first), then alphabetically for ties
        topic_list.sort(key=lambda t: (topic_scores.get(t, 50.0), t))
    else:
        random.shuffle(topic_list)

    target_topic = topic_list[0]
    candidates = topic_available[target_topic]

    # Determine difficulty based on score
    score = topic_scores.get(target_topic, 50.0)
    difficulty_order = ["easy", "medium", "hard"]
    if score < 40:
        difficulty_order = ["easy", "medium", "hard"]
    elif score < 70:
        difficulty_order = ["medium", "easy", "hard"]
    else:
        difficulty_order = ["hard", "medium", "easy"]

    # Pick the first question matching the preferred difficulty
    for diff in difficulty_order:
        matches = [q for q in candidates if q["difficulty"] == diff]
        if matches:
            return random.choice(matches)

    # Fallback: any candidate
    return random.choice(candidates)


# ---------------------------------------------------------------------------
# QuestionBank class (wrapper)
# ---------------------------------------------------------------------------

class QuestionBank:
    """Object-oriented wrapper around the question bank functions."""

    def __init__(self):
        self.questions = QUESTIONS

    def get_question(self, question_id: str) -> Optional[dict]:
        return get_question(question_id)

    def get_questions_by_topic(self, topic: str, difficulty: Optional[str] = None) -> list[dict]:
        return get_questions_by_topic(topic, difficulty)

    def get_questions_by_difficulty(self, difficulty: str) -> list[dict]:
        return get_questions_by_difficulty(difficulty)

    def get_all_topics(self) -> list[str]:
        return get_all_topics()

    def get_all_question_ids(self) -> list[str]:
        return get_all_question_ids()

    def select_next_question(
        self,
        topic_scores: dict[str, float],
        attempted_ids: list[str],
        preferred_topics: Optional[list[str]] = None,
    ) -> Optional[dict]:
        return select_next_question(topic_scores, attempted_ids, preferred_topics)

    def get_random_question(self, difficulty: Optional[str] = None, topic: Optional[str] = None) -> Optional[dict]:
        """Get a random question, optionally filtered."""
        pool = QUESTIONS
        if difficulty:
            pool = [q for q in pool if q["difficulty"] == difficulty]
        if topic:
            pool = [q for q in pool if q["topic"] == topic]
        return random.choice(pool) if pool else None

    @property
    def total_questions(self) -> int:
        return len(QUESTIONS)
