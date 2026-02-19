# Time:  O(n * k)
# Space: O(n * k)

import collections


# freq table
class Solution(object):
    def prefixConnected(self, words, k):
        """
        :type words: List[str]
        :type k: int
        :rtype: int
        """
        cnt = collections.defaultdict(int)
        for w in words:
            if len(w) < k:
                continue
            cnt[w[:k]] += 1
        return sum(v >= 2 for v in cnt.itervalues())
