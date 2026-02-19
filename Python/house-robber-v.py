# Time:  O(n)
# Space: O(1)

# dp
class Solution(object):
    def rob(self, nums, colors):
        """
        :type nums: List[int]
        :type colors: List[int]
        :rtype: int
        """
        dp = [0]*2
        for i in xrange(len(nums)):
            dp[i%2] = max(dp[(i-2)%2]+nums[i], dp[(i-1)%2]) if i-1 >= 0 and colors[i-1] == colors[i] else dp[(i-1)%2]+nums[i]
        return dp[(len(nums)-1)%2]


# Time:  O(n)
# Space: O(1)
# dp
class Solution2(object):
    def rob(self, nums, colors):
        """
        :type nums: List[int]
        :type colors: List[int]
        :rtype: int
        """
        dp = [0]*2
        for i in xrange(len(nums)):
            dp[0], dp[1] = max(dp[0], dp[1]), (dp[0] if i-1 >= 0 and colors[i-1] == colors[i] else max(dp[0], dp[1]))+nums[i]
        return max(dp[0], dp[1])
