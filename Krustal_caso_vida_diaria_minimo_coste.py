import matplotlib.pyplot as plt
import networkx as nx

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Path compression
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

def kruskal_university_paths(graph_edges, buildings):
    graph_edges = sorted(graph_edges, key=lambda x: x[2])  # Ordenar por distancia
    uf = UnionFind(len(buildings))
    mst_edges = []
    total_cost = 0
    
    print("\nConstruyendo caminos óptimos entre edificios universitarios:")

    for u, v, distance in graph_edges:
        if uf.find(u) != uf.find(v):  # Verificar si están en componentes diferentes
            uf.union(u, v)
            mst_edges.append((u, v, distance))
            total_cost += distance
            print(f"Construyendo camino entre {buildings[u]} y {buildings[v]} de {distance} metros")

            if len(mst_edges) == len(buildings) - 1:
                break

    print(f"\nDistancia total de caminos construidos: {total_cost} metros")
    return mst_edges, total_cost

def draw_university_map(edges, buildings, title, filename):
    G = nx.Graph()
    G.add_nodes_from(range(len(buildings)))
    G.add_weighted_edges_from(edges)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    
    # Dibujar todos los caminos en gris
    labels = {i: buildings[i] for i in range(len(buildings))}
    nx.draw(G, pos, labels=labels, node_color="lightblue", node_size=500, font_size=10, edge_color="gray")
    
    # Resaltar los caminos óptimos en verde
    optimal_paths = edges  # El MST ya es la red óptima
    nx.draw_networkx_edges(G, pos, edgelist=optimal_paths, edge_color="green", width=2)
    
    # Etiquetas con las distancias
    edge_labels = {(u, v): f"{w} m" for u, v, w in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="blue")
    
    plt.title(title)
    plt.savefig(filename)
    plt.show()

# Simulación de caminos entre edificios universitarios
buildings = ["A", "B", "C", "D", "E", "F"]
edges = [
    (0, 1, 30), (0, 2, 45), (1, 2, 20), (1, 3, 25),
    (2, 3, 35), (3, 4, 15), (4, 5, 40), (3, 5, 22)
]

# Construir la red de caminos óptimos
university_paths, total_distance = kruskal_university_paths(edges, buildings)
draw_university_map(university_paths, buildings, "Red Óptima de Caminos en la Universidad", "universidad_caminos.jpg")