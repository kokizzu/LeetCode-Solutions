# Time:  O(n^2)
# Space: O(1)

# two pointers
class Solution(object):
    def almostPalindromic(self, s):
        """
        :type s: str
        :rtype: int
        """
        def expand(left, right):
            while 0 <= left and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return left, right

        result = 0
        for i in xrange(2*len(s)-1):
            left, right = expand(i//2, (i+1)//2)
            for left, right in ((left-1, right), (left, right+1)):
                l, r = expand(left, right)
                result = max(result, min((r-l+1)-2, len(s)))
        return result
