from data import runtests
from queue import Queue

INF = float('inf')

def my_solve(N, M, K, base, wages, eq_cost):
    G = create_graph(N, M, K, base, wages, eq_cost)

    edges = []
    for v in range(1, len(G)):
        for u, lim, cost in G[v]:
            edges.append((v, u, lim, cost))
    res = min_cost_flow(len(G), edges, 1, len(G) - 1, K)
    return res

def create_graph(N, M, K, base, wages, eq_cost):
    G = [[], []]

    bases_graph = [None for _ in range(K)]
    guys_graph = [None  for _ in range(N)]
    shows_graph = [None for _ in range(M)]

    current = 2

    for i in range(0, K):
        G.append([])
        if i == 0:
            bases_graph[i] = current
            G[1].append((current, K - i, 0)) 
        else:
            bases_graph[i] = current
            G[bases_graph[i - 1]].append((current, K - 1, 0))
        current += 1

    for i in range(0, N):
        G.append([])
        guys_graph[i] = current
        for j in range(len(base[i])):
            if j > 0:
                G[bases_graph[j]].append((current, 1, base[i][j] - base[i][j - 1]))
            else:
                G[bases_graph[j]].append((current, 1, base[i][j]))
        current += 1

    for i in range(0, M):
        G.append([])
        shows_graph[i] = current
        current += 1

    for i in range(0, N):
        for show_idx, bonus in wages[i]:
            G[guys_graph[i]].append((shows_graph[show_idx - 1], 1, bonus))

    G.append([])
    for i in range(0, M):
        G[shows_graph[i]].append((current, K, eq_cost[i]))
    current += 1

    return G

def min_cost_flow(L, V, s, t, K):
    G = [[[] for _ in range(L)] for _ in range(L)]
    G_list = [[] for _ in range(L)]

    for v, u, weight, cost in V:
        edge_idx = len(G[v][u])
        G[v][u].append([weight, cost])
        G[u][v].append([0, -cost])
        G_list[v].append((u, edge_idx))
        G_list[u].append((v, edge_idx)) 

    flow = 0
    res_cost = 0
    while flow < K:
        d, parent = shortest_path(L, 1, G_list, G)
        if parent[t] == None:
            break

        current = t
        current_min = INF
        while current != s:
            p, edge_idx = parent[current]            
            current_min = min(current_min, G[p][current][edge_idx][0])
            current = p
        flow += current_min
        res_cost += current_min * d[t]
        current = t
        while current != s:
            p, edge_idx = parent[current]
            G[current][p][edge_idx][0] += current_min
            G[p][current][edge_idx][0] -= current_min
            current = p
    if flow < K:
        return -1
    else:
        return res_cost

def shortest_path(n, s, G_list, G):
    d = [INF for _ in range(n)]
    d[s] = 0
    inq = [False for _ in range(n)]
    Q = Queue()
    Q.put(s)
    p = [None for _ in  range(n)]

    while not Q.empty():
        u = Q.get()
        inq[u] = False
        for v, edge_idx in G_list[u]:
            if G[u][v][edge_idx][0] > 0 and d[v] > d[u] + G[u][v][edge_idx][1]:
                d[v] = d[u] + G[u][v][edge_idx][1]
                p[v] = (u, edge_idx)
                if not inq[v]:
                    inq[v] = True
                    Q.put(v)
    return (d, p)

runtests(my_solve)