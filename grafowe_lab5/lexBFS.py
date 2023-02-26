from dimacs import loadWeightedGraph
import os

def checkLexBFS(G, vs):
  n = len(G)
  pi = [None] * n
  for i, v in enumerate(vs):
    pi[v] = i

  for i in range(n-1):
    for j in range(i+1, n-1):
      Ni = G[vs[i]].out
      Nj = G[vs[j]].out

      verts = [pi[v] for v in Nj - Ni if pi[v] < i]
      if verts:
        viable = [pi[v] for v in Ni - Nj]
        if not viable or min(verts) <= min(viable):
          return False
  return True

class Node:
  def __init__(self, idx):
    self.idx = idx
    self.out = set()              # zbiór sąsiadów
    self.ordered_idx = -1

  def connect_to(self, v):
    self.out.add(v)


(V, L) = loadWeightedGraph('graphs/chordal/AT')

G = [None] + [Node(i) for i in range(1, V+1)]  # żeby móc indeksować numerem wierzchołka

for (u, v, _) in L:
  G[u].connect_to(v)
  G[v].connect_to(u)


def lexBFS(G):
    in_order = []
    l = [{v.idx for v in G[2:]}, {1}]

    while len(in_order) < len(G) - 1:
        v = l[-1].pop()
        in_order.append(v)
        new_l = []

        for X in l:
            Y = X & G[v].out
            K = X - Y
            if K:
                new_l.append(K)
            if Y:
                new_l.append(Y)
        l = new_l
    return in_order

def isPEO(lex_order, G):
  for i in range(len(lex_order)):
    G[lex_order[i]].ordered_idx = i
  
  RV = [set() for _ in range(len(G))]
  parents = [None for _ in range(len(G))]

  for v in G[1:]:
    for u in v.out:
      if v.ordered_idx > G[u].ordered_idx:
        RV[v.idx].add(u)
        if parents[v.idx] is not None and G[u].ordered_idx > G[parents[v.idx]].ordered_idx:
          parents[v.idx] = u
        elif parents[v.idx] is None:
          parents[v.idx] = u

  for v in G[1:]:
    if parents[v.idx] is not None and not(RV[v.idx] - {parents[v.idx]} <= RV[parents[v.idx]]):
      return False
  return True

def isChordal(G):
  l = lexBFS(G)
  return isPEO(l, G)

def largestClique(G):
  l = lexBFS(G)
  
  for i in range(len(l)):
    G[l[i]].ordered_idx = i
    
  
  RV = [set() for _ in range(len(G))]

  for v in G[1:]:
    RV[v.idx].add(v.idx)
    for u in v.out:
      if v.ordered_idx > G[u].ordered_idx:
        RV[v.idx].add(u)
    
  res = 0
  for v in G[1:]:
    res = max(res, len(RV[v.idx]))
  return res

def optimal_coloring(G):
  l = lexBFS(G)
  color = [0 for _ in range(len(G))]

  for v in l:
    used = {color[u] for u in G[v].out}
    for c in range(1, len(G)):
      if c not in used:
        color[v] = c
        break

  color_set = {c for c in color[1:]}
  return len(color_set)

def smallestCover(G):
  l = lexBFS(G)

  I = set()

  l.reverse()
  for v in l:
    if not I & G[v].out:
      I.add(v)

  vert = {v.idx for v in G[1:]}
  return len(vert - I)


'''zad1. isChordal
for file in os.listdir("graphs/chordal"):
  with open('graphs/chordal/' + file, 'r') as f:
    solution = int(f.readline().split()[3])
    V, L = loadWeightedGraph('graphs/chordal/' + file)
    G = [None] + [Node(i) for i in range(1, V+1)]
    for (u, v, _) in L:
      G[u].connect_to(v)
      G[v].connect_to(u)
    print(file, "test: ", isChordal(G) == solution)
'''

'''zad2. maxclique
for file in os.listdir("graphs/maxclique"):
  with open('graphs/maxclique/' + file, 'r') as f:
    solution = int(f.readline().split()[3])
    V, L = loadWeightedGraph('graphs/maxclique/' + file)
    G = [None] + [Node(i) for i in range(1, V+1)]
    for (u, v, _) in L:
      G[u].connect_to(v)
      G[v].connect_to(u)
    print(file, "Cliquetest: ", largestClique(G) == solution)
'''

for file in os.listdir("graphs/coloring"):
  with open('graphs/coloring/' + file, 'r') as f:
    solution = int(f.readline().split()[3])
    V, L = loadWeightedGraph('graphs/coloring/' + file)
    G = [None] + [Node(i) for i in range(1, V+1)]
    for (u, v, _) in L:
      G[u].connect_to(v)
      G[v].connect_to(u)
    print(file, "ColorTest: ", optimal_coloring(G) == solution)

#zad4 vcover
'''for file in os.listdir("graphs/vcover"):
  with open('graphs/vcover/' + file, 'r') as f:
    solution = int(f.readline().split()[3])
    V, L = loadWeightedGraph('graphs/vcover/' + file)
    G = [None] + [Node(i) for i in range(1, V+1)]
    for (u, v, _) in L:
      G[u].connect_to(v)
      G[v].connect_to(u)
    print(file, "CoverTest: ", smallestCover(G) == solution)
'''









