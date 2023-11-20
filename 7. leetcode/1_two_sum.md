Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

 
```text
Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]
```

Constraints:
```text
2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
Only one valid answer exists.
```

Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?


```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {value: index for index, value in enumerate(nums)}
        for index, have_in_hand in enumerate(nums):
            look_for = target - have_in_hand
            other_index = hash_map.get(look_for, -1)
            if other_index != -1 and index != other_index:
                return [index, other_index]
```

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]):
        nums_dict = {}
        #loop through the list of index and value
        for i, num in enumerate(nums): 
            #check if the target - num is in the dictionary,
            if target - num in nums_dict:

                return [nums_dict[target - num], i]
            nums_dict[num] = i
        return []
```