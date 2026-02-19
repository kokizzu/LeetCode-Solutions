# Time:  O(n)
# Space: O(n)

import collections


# freq table
class Solution(object):
    def firstUniqueFreq(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        cnt = collections.defaultdict(int)
        for x in nums:
            cnt[x] += 1
        cnt2 = collections.defaultdict(int)
        for v in cnt.itervalues():
            cnt2[v] += 1
        return next((x for x in nums if cnt2[cnt[x]] == 1), -1)
