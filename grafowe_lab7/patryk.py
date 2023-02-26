import networkx as nx
from networkx.algorithms.flow import maximum_flow
from dimacs import loadDirectedWeightedGraph, loadWeightedGraph
import os
from time import process_time


def test_program(graph_directory, f):
    """
    Test given function.

    :param graph_directory: directory with graphs saved in files
    :param f: reference to tested function
    :returns: None
    """
    print(f"Testujemy funkcję {f.__name__}")
    file_counter = 0
    errors = 0
    for path in os.listdir(graph_directory):
        # Check if current path is a file
        file_path = os.path.join(graph_directory, path)
        if os.path.isfile(file_path):
            file_counter += 1
            # Load answer
            result = "OK"
            try:
                with open(file_path, 'r') as file:
                    line = file.readline()
                    expected_ans = int(line.split()[-1])

                    # Test function
                    start_time = process_time()
                    ans = int(f(file_path))
                    end_time = process_time() - start_time

                    result += "\nCzas: " + str(end_time) + 's'

                    if ans != expected_ans:
                        result = f"ERROR"
                        errors += 1
                print(
                    f"-------------------\nGraf {path}\nOdpowiedź wymagana: {expected_ans}\nOdpowiedź otrzymana: {ans} -> {result}")

            except Exception as e:
                print(e.with_traceback())
                print(
                    f"Graf {path}\nBłąd wywołania lub brak odpowiedzi w pliku z grafem!")
                errors += 1

    print(
        f"----------------------\n\nWynik: {file_counter-errors}/{file_counter}")


def convert_graph_to_networkx_graph(filepath):
    (V, L) = loadDirectedWeightedGraph(filepath)

    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(1, V+1)])

    for (u, v, w) in L:
        G.add_edge(u, v)
        G[u][v]['capacity'] = w

    return G


def sat_2cnf(filepath):
    G = convert_graph_to_networkx_graph(filepath)
    return maximum_flow(G, 1, len(G))[0]


# czy graf jest planarny? zwraca parę, której pierwszy element to odpowiedź
test_program("./flow", sat_2cnf)