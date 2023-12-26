
## 2390. Removing Stars From a String
- 12/21/2023
https://leetcode.com/problems/removing-stars-from-a-string/?envType=study-plan-v2&envId=leetcode-75
```python
class Solution:
    def __init__(self):
        self.storage = {}
    def removeStars(self, s: str) -> str:
        stack = []
        for curr_char in s:
            # if char is not a star, add to the stack
            if curr_char != '*':
                stack.append(curr_char)
            # if char is a star, pop if the star is not empty
            elif stack:
                stack.pop()
        return "".join(stack)
```


## 206. Reverse Linked List
- 12/24/2023
https://leetcode.com/problems/reverse-linked-list/solutions/4439220/video-step-by-step-visualization-of-o-n-solution/?envType=study-plan-v2&envId=leetcode-75
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        new_list = None
        while head:
            pre = head
            head = head.next
            pre.next = new_list
            new_list = pre

        return new_list
```

solution 2:
```python
class Solution:
   def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head.next or not head:
            return head
        result = self.reverseList(head.next)
        print("head", head.val)
        print("head.next: ", head.next.val)
        res = ""
        rr = result
        while rr:
            res += str(rr.val) + " -> "
            rr = rr.next
        print("result: " + res)
        head.next.next = head
        head.next = None

        return result
```
```text
head 4
head.next:  5
result: 5 -> 
head 3
head.next:  4
result: 5 -> 4 -> 
head 2
head.next:  3
result: 5 -> 4 -> 3 -> 
head 1
head.next:  2
result: 5 -> 4 -> 3 -> 2 -> 
```


## 700 Search in a Binary Search Tree
- 12/24/2023

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if root is None or root.val == val:
            return root
        if root.val > val:
            return self.searchBST(root.left, val)
        else:
            return self.searchBST(root.right, val)

```

method 2:
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        while root and root.val != val:
            if root.val > val:
                root = root.left
            else:
                root = root.right
        return root
```


