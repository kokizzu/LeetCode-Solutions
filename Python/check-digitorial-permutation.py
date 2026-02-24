# Time:  O(logn + 10)
# Space: O(10)

# freq table
FACT = [1]*2
def factorial(n):
    while len(FACT) <= n:
        FACT.append(FACT[-1]*len(FACT))
    return FACT[n]

class Solution(object):
    def isDigitorialPermutation(self, n):
        """
        :type n: int
        :rtype: bool
        """
        def f(x):
            cnt = [0]*10
            while x:
                x, r = divmod(x, 10)
                cnt[r] += 1
            return cnt

        total = 0
        x = n
        while x:
            x, r = divmod(x, 10)
            total += factorial(r)
        return f(total) == f(n)
