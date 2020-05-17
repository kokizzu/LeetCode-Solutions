# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem D. Emacs++
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033893b
#
# Time:  O(K * (logK)^2 + Q * logK)
# Space: O(KlogK)
#

from collections import defaultdict
from itertools import izip
from heapq import heappop, heappush

def dijkstra(PRG, L, R, P, lookup, brackets, i):  # Time: O(KlogK)
    # start to all, all to start (run twice)
    # - for outer region, remember to adjust the cost of last of A to/from the first of E in A(B(C)D)E
    pass
    # adj = [[] for _ in xrange(len(brackets))]
    # for u, v, w in times:
    #     adj[u-1].append((v-1, w))
    # result = 0
    # lookup = set()
    # best = defaultdict(lambda: float("inf"))
    # min_heap = [(0, K-1)]
    # while min_heap and len(lookup) != N:
    #     result, u = heappop(min_heap)
    #     lookup.add(u)
    #     if best[u] < result:
    #         continue
    #     for v, w in adj[u]:
    #         if v in lookup: continue
    #         if result+w < best[v]:
    #             best[v] = result+w
    #             heappush(min_heap, (result+w, v))
    # return dis  # the shortest of [s, ps], [ps, s]

def find_partitions(PRG, brackets):  # Time: O(K)
    # find the spans cover (cross or touch) "middle bracket" brackets[len(bracket)//2] as pivot,
    # s.t. outer span size > 1/2, inner span size < 1/2, and outer is parent of inner
    # split to 4 regions 
    return [0, 1, 2, 3]

def regions(find_partitions, s):  # Time: O(K)
    return s

def recurse(PRG, L, R, P, lookup, brackets, s, e):  # run at most O(KlogK) in each depth, at most logK depth
    if len(brackets) == 2:  # only "()" we added
        return 0
    partitions = find_partitions(PRG, brackets)
    for i in partitions:
        if i in lookup:  # (0, len(PRG)-1) may be in lookup, but others may not yet
            continue
        # new_brackets = "(" + bracket[i:j] + ")"
        lookup[i] = dijkstra(PRG, L, R, P, lookup, brackets, i)
    a, b = regions(partitions, s), regions(partitions, e)  # find s, e in which A, B, C, D, E
    if a == b:  # same region
        # new_brackets = bracket[i:j] + bracket[j:k] (optional)
        new_brackets = brackets
        return recurse(PRG, L, R, P, lookup, new_brackets, s, e)
    c = max(a, b)
    return min(lookup[c][s, c] + lookup[c][c, e]) # find min of entering left or right

def emacs():
    K, Q = map(int, raw_input().strip().split())
    PRG = "(" + raw_input().strip() + ")"
    L = [float("inf")] + map(int, raw_input().strip().split()) + [float("inf")]
    L[1] = float("inf")
    R = [float("inf")] + map(int, raw_input().strip().split()) + [float("inf")]
    R[-2] = float("inf")
    P = [float("inf")] + map(int, raw_input().strip().split()) + [float("inf")]
    S = map(int, raw_input().strip().split())
    E = map(int, raw_input().strip().split())
    result, lookup, brackets = 0, {}, tuple(range(len(PRG)))
    for s, e in izip(S, E):
        result += recurse(PRG, L, R, P, lookup, brackets, s, e)
    return result
    
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, emacs())
