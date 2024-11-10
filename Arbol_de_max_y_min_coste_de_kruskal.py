import matplotlib.pyplot as plt
import networkx as nx

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

def kruskal_simulator(graph_edges, num_nodes, max_tree=False):
    graph_edges = sorted(graph_edges, key=lambda x: x[2], reverse=max_tree)
    uf = UnionFind(num_nodes)
    mst_edges = []
    total_cost = 0
    
    print(f"\nConstrucción del Árbol de {'Máximo' if max_tree else 'Mínimo'} Costo usando Kruskal:")

    for u, v, weight in graph_edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_edges.append((u, v, weight))
            total_cost += weight
            print(f"Añadiendo arista ({u}, {v}) con peso {weight}")

            if len(mst_edges) == num_nodes - 1:
                break

    print(f"\nCosto total del Árbol de {'Máximo' if max_tree else 'Mínimo'} Costo: {total_cost}")
    return mst_edges, total_cost

def draw_and_save_graph(edges, num_nodes, title, filename):

    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    G.add_weighted_edges_from(edges)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
    edge_labels = {(u, v): f"{w}" for u, v, w in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    
    plt.title(title)
    plt.savefig(filename)
    plt.show()

# Ejemplo de uso
edges = [
    (0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2),
    (2, 3, 4), (3, 4, 2), (4, 5, 6), (3, 5, 3)
]
num_nodes = 6

# Árbol de Mínimo Costo
mst_min_edges, min_cost = kruskal_simulator(edges, num_nodes, max_tree=False)
draw_and_save_graph(mst_min_edges, num_nodes, "Árbol de Mínimo Costo - Kruskal", "arbol_minimo_costo.jpg")

# Árbol de Máximo Costo
mst_max_edges, max_cost = kruskal_simulator(edges, num_nodes, max_tree=True)
draw_and_save_graph(mst_max_edges, num_nodes, "Árbol de Máximo Costo - Kruskal", "arbol_maximo_costo.jpg")
