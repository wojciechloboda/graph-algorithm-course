
from dimacs import loadWeightedGraph
import os
from queue import Queue

def BFS(G, G_list, s, parent, L):
    Q = Queue()
    Q.put(s)
    while not Q.empty():
        v = Q.get()
        for u in G_list[v]:
            if G[v][u] > 0 and parent[u] == None:
                parent[u] = v
                Q.put(u)

def edmonds_karp(L, V, s, t):
    G = [[0 for _ in range(L + 1)] for _ in range(L + 1)]
    orig = [[False for _ in range(L + 1)] for _ in range(L + 1)]

    G_list = [[] for _ in range(L + 1)]

    for v, u, weight in V:
        G_list[v].append(u)
        G_list[u].append(v) 
        G[v][u] = weight
        orig[v][u] = True

    #for test in G:
    #    print(test)
    new_res = 0
    while True:
        parent = [None for _ in range(L + 1)]
        parent[s] = s

        BFS(G, G_list, s, parent, L)
        if parent[t] == None:
            res = 0
            for v in range(L + 1):
                if orig[s][v]:
                    res += G[v][s]
            return new_res

        current = t
        current_min = INF
        while parent[current] != current:
            current_min = min(current_min, G[parent[current]][current])
            current = parent[current]
        
        current = t
        while parent[current] != current:
            G[current][parent[current]] += current_min
            G[parent[current]][current] -= current_min
            current = parent[current]
        new_res += current_min


INF = float('inf')
def spojnosc(L, V):
    directed_G = []

    for v, u, weigth in V:
        directed_G.append((v, u, weigth))
        directed_G.append((u, v, weigth))
    res = INF

    for t in range(2, L + 1):
        res = min(res, edmonds_karp(L, directed_G, 1, t))
    return res

#V, L = loadWeightedGraph('graphs/trivial')
#print('simple', "test: ", spojnosc(V, L))
#sys.setrecursionlimit(1000000000)


for file in os.listdir("graphs"):
    with open('graphs/' + file, 'r') as f:
        solution = int(f.readline().split()[3])
        if file != 'grid100x100' and file != 'clique200':
            V, L = loadWeightedGraph('graphs/' + file)
            print(file, "test: ", solution == spojnosc(V, L))



