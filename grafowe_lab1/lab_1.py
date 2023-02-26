from dimacs import loadWeightedGraph
from queue import PriorityQueue
import os
import sys

INF = float('inf')

def union(v, u, parent, rank):
    v = find_parent(v, parent)
    u = find_parent(u, parent)

    if rank[v] > rank[u]:
        parent[u] = v
    elif rank[u] > rank[v]:
        parent[v] = u
    else:
        parent[u] = v
        rank[v] += 1

def find_parent(v, parent):
    if v != parent[v]:
        parent[v] = find_parent(parent[v], parent)
    return parent[v]

def rozgrzewka_union(V, L, s, t):
    L.sort(key = lambda x : -1 * x[2])
    parent = [i for i in range(V + 1)]
    rank = [1 for _ in range(V + 1)]
    res = float('inf')
    for v, u, weight in L:
        if find_parent(s, parent) == find_parent(t, parent):
            return res

        if find_parent(v, parent) != find_parent(u, parent):
            res = min(res, weight)
            union(u, v, parent, rank)
    

    if find_parent(s, parent) == find_parent(t, parent):
            return res
    return -1


def rozgrzewka_dijkstra(V, L, s, t):
    for v, u, weight in L:
        N = max(v, u)

    N += 1
    G = [[] for _ in range(N + 1)]

    for v, u, weight in L:
        G[v].append((u, weight))
        G[u].append((v, weight))

    Q = PriorityQueue()
    d = [0 for _ in range(N + 1)]
    d[s] = float('inf')
    Q.put((-1 * d[s], s))

    while not Q.empty():
        tmp, v = Q.get()
        for u, weight in G[v]:
            weight = min(d[v], weight)
            if d[u] < weight:
                d[u] = weight
                Q.put((-1 * weight, u))
    
    return d[t]


def DFS(G, v, visited, min_weight):
    visited[v] = True

    for u, weight in G[v]:
        if visited[u] == False and weight >= min_weight:
            DFS(G, u, visited, min_weight)


def binsearch(V, L, s, t):

    G = [[] for _ in range(V + 1)]

    for v, u, weight in L:
        G[v].append((u, weight))
        G[u].append((v, weight))

    L.sort(key = lambda x : x[2])

    a = 0
    b = len(L) - 1

    while a < b:
        x = (a + b) // 2 + 1

        v, u, weight = L[x]
        visited = [False for _ in range(V + 1)]
        DFS(G , s, visited, weight)

        if visited[t] == True:
            a = x
        else:
            b = x - 1

    return L[a][2]

'''
sys.setrecursionlimit(10000000)
V, L = loadWeightedGraph('graphs/rand20_100')
print(binsearch(V, L, 1, 2))
'''


sys.setrecursionlimit(1000000000)
for file in os.listdir("graphs"):
    with open('graphs/' + file, 'r') as f:
        solution = int(f.readline().split()[3])
        V, L = loadWeightedGraph('graphs/' + file)
        print(file, "test: ", solution == binsearch(V, L, 1, 2))









