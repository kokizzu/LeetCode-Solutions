# Time:  O(n)
# Space: O(n)

import collections


# graph, prefix sum, two pointers, sliding window
class Solution(object):
    def getMaxFunctionValue(self, receiver, k):
        """
        :type receiver: List[int]
        :type k: int
        :rtype: int
        """
        def find_cycles(adj):
            result = []
            lookup = [False]*len(adj)
            for u in xrange(len(adj)):
                cnt = {}
                while not lookup[u]:
                    lookup[u] = True
                    cnt[u] = len(cnt)
                    u = adj[u]
                if u in cnt:
                    result.append((u, len(cnt)-cnt[u]))
            return result

        def find_prefixes(cycles):
            lookup = [(-1, -1)]*len(receiver)
            prefixes = [[0] for _ in xrange(len(cycles))]
            for idx, (u, l) in enumerate(cycles):
                for i in xrange(l):
                    lookup[u] = (idx, i)
                    prefixes[idx].append(prefixes[idx][i]+u)
                    u = receiver[u]
            return lookup, prefixes
        
        def get_sum(prefix, i, cnt):
            q, r = divmod(cnt, len(prefix)-1)
            return (q*prefix[-1]+
                    (prefix[min(i+r, len(prefix)-1)]-prefix[i])+
                    (prefix[(max(((i+r)-(len(prefix)-1), 0)))]-prefix[0]))
        
        def start_in_cycle():
            result = 0
            for u, l in cycles:
                for _ in xrange(l):
                    idx, i = lookup[u]
                    result = max(result, get_sum(prefixes[idx], i, k+1))
                    u = receiver[u]
            return result
    
        def start_out_of_cycle():
            result = 0
            degree = [0]*len(receiver)
            for x in receiver:
                degree[x] += 1
            for u in xrange(len(receiver)):
                if degree[u]:
                    continue
                curr = 0
                dq = collections.deque()
                while lookup[u][0] == -1:
                    curr += u
                    dq.append(u)
                    if len(dq) == k+1:
                        result = max(result, curr)
                        curr -= dq.popleft()
                    u = receiver[u]
                idx, i = lookup[u]
                while dq:
                    result = max(result, curr+get_sum(prefixes[idx], i, (k+1)-len(dq)))
                    curr -= dq.popleft()
            return result
            
        cycles = find_cycles(receiver)
        lookup, prefixes = find_prefixes(cycles)
        return max(start_in_cycle(), start_out_of_cycle())


# Time:  O(nlogk)
# Space: O(nlogk)
# binary lifting
class Solution2(object):
    def getMaxFunctionValue(self, receiver, k):
        """
        :type receiver: List[int]
        :type k: int
        :rtype: int
        """
        l = (k+1).bit_length()
        P = [receiver[:] for _ in xrange(l)]
        S = [range(len(receiver)) for _ in xrange(l)]
        for i in xrange(1, len(P)):
            for u in xrange(len(receiver)):
                P[i][u] = P[i-1][P[i-1][u]]
                S[i][u] = S[i-1][u]+S[i-1][P[i-1][u]]
        result = 0
        for u in xrange(len(receiver)):
            curr = 0
            for i in xrange(l):
                if (k+1)&(1<<i):
                    curr += S[i][u]
                    u = P[i][u]
            result = max(result, curr)
        return result
