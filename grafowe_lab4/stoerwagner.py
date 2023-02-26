
from dimacs import loadWeightedGraph
import os
from queue import PriorityQueue

INF = float('inf')

class Node:
    def __init__(self):
        self.edges = {}
        self.is_active = True
        self.mergedVerices = []

    def addEdge( self, to, weight):
        self.edges[to] = self.edges.get(to,0) + weight 

    def delEdge( self, to ):
        del self.edges[to]     

def createGraphRepresentation(V, L):
    G = [Node() for _ in range(V + 1)]
    for v, u, weight in L:
        G[v].addEdge(u, weight)
        G[u].addEdge(v, weight)

    return G

def printGraph(G):
    for v in range(1, V + 1):
        print(G[v].is_active, v, ' -> ', end = '')
        for u in G[v].edges:
            weight = G[v].edges[u]
            if weight > 0:
                print((u, weight), end = ', ')
        print(" ")

def mergeVertices(G, v, u):
    G[u].is_active = False
    G[v].mergedVerices.append(u)

    for x in G[u].edges:
        if x != v:
            G[v].addEdge(x, G[u].edges[x])
            G[x].addEdge(v, G[u].edges[x])
            G[x].delEdge(u)

def minCutPhase(G, V):
    Q = PriorityQueue()
    visited = [False for _ in range(len(G))]
    v = 1
    d_init = 0
    for u in G[v].edges:
        d_init += G[v].edges[u]
    
    S = []

    d = [0 for _ in range(len(G))]
    d[v] = d_init
    Q.put((-d[v], v))
    while len(S) != V:
        _, v = Q.get()
        while visited[v] == True:
            _, v = Q.get()
        visited[v] = True
        S.append(v)
        for u in G[v].edges:
            if G[u].is_active and visited[u] == False:
                d[u] += G[v].edges[u]
                Q.put((-d[u], u))
    
    mergeVertices(G, S[-1], S[-2])
    return (d[S[-1]], S[-1]) 

#def active_count(G):
#    V = 0
#    for x in G[1:]:
#        if x.is_active:
#            V += 1
#    return V

def stoerwagner(V, L):
    G = createGraphRepresentation(V, L)
    res_merged = 0
    res = INF

    while V > 1:
        current, s = minCutPhase(G, V)
        if current < res:
            res_merged = s
            res = current
        V -= 1

    return res

for file in os.listdir("graphs"):
    with open('graphs/' + file, 'r') as f:
        solution = int(f.readline().split()[3])
        if file != 'grid100x100':
            V, L = loadWeightedGraph('graphs/' + file)
            print(file, "test: ", solution == stoerwagner(V, L))
