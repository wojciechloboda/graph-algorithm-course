import networkx as nx   # standardowy sposób importowania biblioteki
from dimacs import loadWeightedGraph
from dimacs import loadDirectedWeightedGraph
from dimacs import loadCNFFormula
from networkx.algorithms.planarity import check_planarity
from networkx.algorithms.flow import maximum_flow
import os
from networkx.algorithms.components import strongly_connected_components
'''
# tworzenie grafu
G = nx.Graph()                   # stwórz pusty graf nieskierowany
G.add_node(1)                    # dodaj wierzchołek 1 (wierzchołkami może być cokolwiek haszowalnego)
G.add_nodes_from([2,3])          # dodaj wierzchołki z listy (dowolnego iterowalnego kontenera)
G.remove_node(1)                 # usuń wierchołek 1
G.remove_nodes_from([2,3])       # usuń wierzchołki z listy
G.add_edge(1,2)                  # dodaj krawędź między wierzchołkami 1 i 2
G.add_edges_from([(1,3),(2,3)])  # dodaj krawędzie z listy (iterowalnego kontenera)
G.remove_edge(1,2)               # usuń krawędź 
G.remove_edges_from([(1,2),(1,3)])  # usuń krawędzie z listy (iterowalnego kontenera)

# odczytywanie podstawowych informacji o grafie
G.number_of_nodes()              # liczba wierzchołkóœ
G.number_of_edges()              # liczba krawędzi
G.nodes                          # wierzchołki grafu
G.edges                          # krawędzie grafu
G.adj[1]                         # sąsiedzi wierzchołka 1
G[1]                             # sąsiedzi wierzchołka 1
G[1][2]                          # dostęp do krawędzi {1,2} (można jej dodawać atrybuty)
G.has_node(1)                    # czy istnieje wierzchołek 1?
G.has_edge(1,2)                  # czy istnieje krawędź {1,2}?
'''

def create_graph(V, L):
    G = nx.Graph()
    for v, u, _ in L:
        G.add_nodes_from((v, u))
        G.add_edge(v, u)
    return G

def create_directed_formula(V, F):
    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(1, V + 1)])
    G.add_nodes_from([-i for i in range(1, V + 1)])
    for v, u in F:
        G.add_edge(v, u)
    return G
    
def create_weighted_digraph(V, L):
    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(1, V + 1)])
    for v, u, c in L:
        G.add_edge(v, u)
        G[v][u]['capacity'] = c 
    return G

def check(G):
    SCC = strongly_connected_components(G)
    for s in SCC:
        for elem in s:
            if -elem in s:
                return False
    return True




'''zad1.planarnosc
for file in os.listdir('flow/'):
  with open('flow/' + file, 'r') as f:
    solution = int(f.readline().split()[3])
    V, L = loadWeightedGraph('flow/' + file)
    G = create_graph(V, L)
    print(check_planarity(G))
'''

'''zad2. 
for file in os.listdir('flow/'):
  with open('flow/' + file, 'r') as f:
    solution = int(f.readline().split()[3])
    V, L = loadDirectedWeightedGraph('flow/' + file)
    G = create_weighted_digraph(V, L)
    print(file, ' :', maximum_flow(G, 1, V)[0] == solution)
'''


for file in os.listdir('sat/'):
  with open('sat/' + file, 'r') as f:
    (V,F) = loadCNFFormula('sat/simple_sat')  
    G = create_directed_formula(V, F)
    print(check(G))



#V, L = loadWeightedGraph('graphs/vcover/clique5')
#G = create_graph(V, L)
#print(check_planarity(G))

