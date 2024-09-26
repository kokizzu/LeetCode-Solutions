# Time:  O(n)
# Space: O(n)

import collections


# combinatorics, prefix sum, freq table, dp
class Solution(object):
    def getSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        def count(d):
            result = 0
            cnt = collections.defaultdict(int)
            prefix = collections.defaultdict(int)
            for x in nums:
                l = (cnt[x-d]+1)%MOD
                cnt[x] = (cnt[x]+l)%MOD
                total = (prefix[x-d]+(l*x))%MOD
                prefix[x] = (prefix[x]+total)%MOD
                result = (result+total)%MOD
            return result
    
        MOD = 10**9+7
        return (count(+1)+count(-1)-reduce(lambda accu, x: (accu+x)%MOD, nums, 0))%MOD
