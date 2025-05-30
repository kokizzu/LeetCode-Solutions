# Time:  O(n)
# Space: O(1)

# greedy
class Solution(object):
    def answerString(self, word, numFriends):
        """
        :type word: str
        :type numFriends: int
        :rtype: str
        """
        if numFriends == 1:
            return word
        idx = l = 0
        for i in xrange(1, len(word)):
            if word[i] == word[idx+l]:
                l += 1
            elif word[i] < word[idx+l]:
                l = 0
            elif word[i] > word[idx+l]:
                if word[i-l] >= word[i]:
                    idx = i-l
                else:
                    idx = i
                l = 0
        return word[idx:len(word)-max((numFriends-1)-idx, 0)]



# Time:  O(n * m)
# Space: O(m)
# greedy
class Solution2(object):
    def answerString(self, word, numFriends):
        """
        :type word: str
        :type numFriends: int
        :rtype: str
        """
        if numFriends == 1:
            return word
        m = len(word)-(numFriends-1)
        c = max(word)
        return max(word[i:i+m] for i in xrange(len(word)) if word[i] == c)
