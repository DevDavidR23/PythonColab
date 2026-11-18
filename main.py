import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Crear el grafo no dirigido
G = nx.Graph()

# ==========================================
# 1. DEFINICIÓN DE LOS 25 NODOS CON ATRIBUTOS
# ==========================================
nodes_data = [
    # Universidades (4 nodos)
    ("Univ_Cundinamarca_Fusa", {"type": "Universidad", "region": "Sumapaz"}),
    ("Univ_Minuto_Soacha", {"type": "Universidad", "region": "Soacha"}),
    ("Univ_Piloto_Girardot", {"type": "Universidad", "region": "Alto Magdalena"}),
    ("Univ_Central_Chía", {"type": "Universidad", "region": "Sabana Centro"}),

    # Grupos de Investigación (8 nodos)
    ("Grupo_GICUNDI", {"type": "Investigación", "parent": "Univ_Cundinamarca_Fusa"}),
    ("Grupo_SINTESIS", {"type": "Investigación", "parent": "Univ_Cundinamarca_Fusa"}),
    ("Grupo_INNOVA_Soacha", {"type": "Investigación", "parent": "Univ_Minuto_Soacha"}),
    ("Grupo_BIO_Magdalena", {"type": "Investigación", "parent": "Univ_Piloto_Girardot"}),
    ("Grupo_TECNOSABANA", {"type": "Investigación", "parent": "Univ_Central_Chía"}),
    ("Grupo_CYBER_Cundi", {"type": "Investigación", "parent": "Univ_Cundinamarca_Fusa"}),
    ("Grupo_AGROINNOVA", {"type": "Investigación", "parent": "Univ_Cundinamarca_Fusa"}),
    ("Grupo_PEDAGOGIA_Red", {"type": "Investigación", "parent": "Univ_Minuto_Soacha"}),

    # Laboratorios de Innovación Juvenil (5 nodos)
    ("Lab_Juvenil_Fusagasugá", {"type": "Lab Juvenil", "region": "Sumapaz"}),
    ("Lab_Juvenil_Soacha", {"type": "Lab Juvenil", "region": "Soacha"}),
    ("Lab_Juvenil_Zipaquirá", {"type": "Lab Juvenil", "region": "Sabana Centro"}),
    ("Lab_Juvenil_Facatativá", {"type": "Lab Juvenil", "region": "Sabana Occidente"}),
    ("Lab_Juvenil_Girardot", {"type": "Lab Juvenil", "region": "Alto Magdalena"}),

    # Colegios Locales (8 nodos)
    ("Colegio_Guillermo_Leon_Fusa", {"type": "Colegio", "region": "Sumapaz"}),
    ("Colegio_Ricaurte_Soacha", {"type": "Colegio", "region": "Soacha"}),
    ("Colegio_La_Salle_Zipa", {"type": "Colegio", "region": "Sabana Centro"}),
    ("Colegio_Agricola_Facatativa", {"type": "Colegio", "region": "Sabana Occidente"}),
    ("Colegio_Industrial_Girardot", {"type": "Colegio", "region": "Alto Magdalena"}),
    ("Colegio_Campestre_Chia", {"type": "Colegio", "region": "Sabana Centro"}),
    ("Colegio_Integrado_Villeta", {"type": "Colegio", "region": "Gualivá"}),
    ("Colegio_Normal_Ubaté", {"type": "Colegio", "region": "Ubaté"})
]

for node, attrs in nodes_data:
    G.add_node(node, **attrs)

# ==========================================
# 2. DEFINICIÓN DE LAS ARISTAS (RELACIONES)
# ==========================================
edges = [
    # Vínculos institucionales (Universidad -> Grupos)
    ("Univ_Cundinamarca_Fusa", "Grupo_GICUNDI", {"relation": "pertenece"}),
    ("Univ_Cundinamarca_Fusa", "Grupo_SINTESIS", {"relation": "pertenece"}),
    ("Univ_Cundinamarca_Fusa", "Grupo_CYBER_Cundi", {"relation": "pertenece"}),
    ("Univ_Cundinamarca_Fusa", "Grupo_AGROINNOVA", {"relation": "pertenece"}),
    ("Univ_Minuto_Soacha", "Grupo_INNOVA_Soacha", {"relation": "pertenece"}),
    ("Univ_Minuto_Soacha", "Grupo_PEDAGOGIA_Red", {"relation": "pertenece"}),
    ("Univ_Piloto_Girardot", "Grupo_BIO_Magdalena", {"relation": "pertenece"}),
    ("Univ_Central_Chía", "Grupo_TECNOSABANA", {"relation": "pertenece"}),

    # Proyectos conjuntos e interinstitucionales
    ("Grupo_GICUNDI", "Grupo_AGROINNOVA", {"relation": "proyecto_conjunto"}),
    ("Grupo_SINTESIS", "Grupo_TECNOSABANA", {"relation": "proyecto_conjunto"}),
    ("Univ_Cundinamarca_Fusa", "Univ_Minuto_Soacha", {"relation": "convenio_marco"}),
    # OJO: sin esta arista, Girardot queda desconectado del resto de la red.
    # Descomenta la línea si quieres un grafo conexo:
    # ("Univ_Piloto_Girardot", "Univ_Cundinamarca_Fusa", {"relation": "convenio_marco"}),

    # Mentorías activas (Grupos / Universidades -> Labs Juveniles)
    ("Grupo_GICUNDI", "Lab_Juvenil_Fusagasugá", {"relation": "mentoría"}),
    ("Grupo_INNOVA_Soacha", "Lab_Juvenil_Soacha", {"relation": "mentoría"}),
    ("Grupo_TECNOSABANA", "Lab_Juvenil_Zipaquirá", {"relation": "mentoría"}),
    ("Grupo_BIO_Magdalena", "Lab_Juvenil_Girardot", {"relation": "mentoría"}),
    ("Univ_Cundinamarca_Fusa", "Lab_Juvenil_Facatativá", {"relation": "convenio"}),

    # Transferencia de conocimiento / Proyectos con colegios locales
    ("Lab_Juvenil_Fusagasugá", "Colegio_Guillermo_Leon_Fusa", {"relation": "formacion"}),
    ("Lab_Juvenil_Soacha", "Colegio_Ricaurte_Soacha", {"relation": "formacion"}),
    ("Lab_Juvenil_Zipaquirá", "Colegio_La_Salle_Zipa", {"relation": "formacion"}),
    ("Lab_Juvenil_Girardot", "Colegio_Industrial_Girardot", {"relation": "formacion"}),
    ("Grupo_CYBER_Cundi", "Colegio_Campestre_Chia", {"relation": "transferencia"}),
    ("Grupo_PEDAGOGIA_Red", "Colegio_Normal_Ubaté", {"relation": "transferencia"}),
    ("Univ_Central_Chía", "Colegio_Integrado_Villeta", {"relation": "extension"}),
    ("Grupo_AGROINNOVA", "Colegio_Agricola_Facatativa", {"relation": "transferencia"})
]

G.add_edges_from([(u, v, d) for u, v, d in edges])

# ==========================================
# 3. ALGORITMOS DE RECORRIDO (BFS y DFS)
# ==========================================
def bfs(grafo, inicio):
    """Recorrido en anchura. Devuelve orden de visita, nivel y padre de cada nodo."""
    visitado = {inicio}
    cola = deque([inicio])
    orden = []
    nivel = {inicio: 0}
    padre = {inicio: None}

    while cola:
        actual = cola.popleft()
        orden.append(actual)
        for vecino in sorted(grafo.neighbors(actual)):  # sorted -> resultado reproducible
            if vecino not in visitado:
                visitado.add(vecino)
                nivel[vecino] = nivel[actual] + 1
                padre[vecino] = actual
                cola.append(vecino)
    return orden, nivel, padre


def dfs(grafo, inicio):
    """Recorrido en profundidad (iterativo con pila). Devuelve el orden de visita."""
    visitado = set()
    pila = [inicio]
    orden = []

    while pila:
        actual = pila.pop()
        if actual in visitado:
            continue
        visitado.add(actual)
        orden.append(actual)
        # reversed(sorted) para que se visite primero el vecino alfabéticamente menor
        for vecino in reversed(sorted(grafo.neighbors(actual))):
            if vecino not in visitado:
                pila.append(vecino)
    return orden


def camino_mas_corto(grafo, origen, destino):
    """Camino con menos aristas entre dos nodos (usa BFS). None si no hay camino."""
    _, _, padre = bfs(grafo, origen)
    if destino not in padre:
        return None
    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = padre[nodo]
    return camino[::-1]


def recorrido_completo(grafo, metodo):
    """Aplica BFS o DFS a cada componente conexa, para cubrir TODOS los nodos."""
    visitados, resultado = set(), []
    for nodo in sorted(grafo.nodes()):
        if nodo not in visitados:
            orden = metodo(grafo, nodo) if metodo is dfs else metodo(grafo, nodo)[0]
            resultado.append(orden)
            visitados.update(orden)
    return resultado

# ==========================================
# 4. VISUALIZACIÓN DEL GRAFO
# ==========================================
def dibujar(grafo, pos, titulo, camino=None):
    plt.figure(figsize=(14, 10))
    colores = {"Universidad": "#ff7f0e", "Investigación": "#1f77b4",
               "Lab Juvenil": "#2ca02c", "Colegio": "#d62728"}
    color_map = [colores[grafo.nodes[n]["type"]] for n in grafo.nodes()]

    nx.draw_networkx_nodes(grafo, pos, node_color=color_map, node_size=700, alpha=0.9)
    nx.draw_networkx_edges(grafo, pos, width=1.5, alpha=0.5, edge_color="gray")
    nx.draw_networkx_labels(grafo, pos, font_size=8, font_family="sans-serif")

    if camino:  # resaltar el camino encontrado
        aristas_camino = list(zip(camino, camino[1:]))
        nx.draw_networkx_edges(grafo, pos, edgelist=aristas_camino, width=4, edge_color="black")

    plt.title(titulo, fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

pos = nx.spring_layout(G, seed=42, k=0.3)
dibujar(G, pos, "Ecosistema de Investigación e Innovación en Cundinamarca (25 Nodos)")

# ==========================================
# 5. MÉTRICAS BÁSICAS
# ==========================================
print(f"Número total de nodos: {G.number_of_nodes()}")
print(f"Número total de aristas (conexiones): {G.number_of_edges()}")
print(f"Densidad de la red: {nx.density(G):.4f}")
print(f"¿Grafo conexo?: {nx.is_connected(G)}")
print(f"Componentes conexas: {nx.number_connected_components(G)}")

# ==========================================
# 6. RECORRIDOS Y PRUEBAS
# ==========================================
inicio = "Univ_Cundinamarca_Fusa"

orden_bfs, niveles, _ = bfs(G, inicio)
print(f"\n--- BFS desde {inicio} ({len(orden_bfs)} nodos alcanzados) ---")
for i, n in enumerate(orden_bfs, 1):
    print(f"{i:2d}. {n}  (nivel {niveles[n]})")

orden_dfs = dfs(G, inicio)
print(f"\n--- DFS desde {inicio} ({len(orden_dfs)} nodos alcanzados) ---")
for i, n in enumerate(orden_dfs, 1):
    print(f"{i:2d}. {n}")

# Nodos que NO se alcanzan desde el inicio (si el grafo no es conexo)
no_alcanzados = set(G.nodes()) - set(orden_bfs)
if no_alcanzados:
    print(f"\nNodos no alcanzables desde {inicio}: {sorted(no_alcanzados)}")

# Camino más corto entre una universidad y un colegio
origen, destino = "Univ_Cundinamarca_Fusa", "Colegio_Normal_Ubaté"
camino = camino_mas_corto(G, origen, destino)
print(f"\n--- Camino más corto: {origen} -> {destino} ---")
print(" -> ".join(camino) if camino else "No existe camino")
print(f"Aristas en el camino: {len(camino) - 1}" if camino else "")

# Verificación contra la implementación de NetworkX
assert set(orden_bfs) == set(nx.node_connected_component(G, inicio))
assert len(camino) - 1 == nx.shortest_path_length(G, origen, destino)
print("\nVerificación con NetworkX: OK")

if camino:
    dibujar(G, pos, f"Camino más corto: {origen} → {destino}", camino)