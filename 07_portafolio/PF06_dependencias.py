# 07_portafolio/PF06_dependencias.py
# Mapa de dependencias entre proyectos, orden topológico y proyectos habilitadores · COOPAC Frontera Sur
import os
import pandas as pd, networkx as nx, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DEP = [  # (proyecto, depende_de)
 ("PR-01","PR-12"),                       # los dueños del dato los designa el comité de gobierno
 ("PR-03","PR-02"), ("PR-03","PR-01"),    # banca digital: integración con el central y socio único
 ("PR-04","PR-01"), ("PR-04","PR-02"),    # scoring: datos confiables y acceso al historial de crédito
 ("PR-05","PR-01"), ("PR-05","PR-02"),    # tablero de cartera: datos confiables e integrados
 ("PR-08","PR-02"), ("PR-08","PR-07"),    # sistema central: desacoplado por la integración, con respaldo previo
 ("PR-09","PR-01"), ("PR-09","PR-02"),    # monitoreo de operaciones: socio único y transacciones integradas
 ("PR-10","PR-01"),                       # datos personales: inventario sobre el dato maestro
 ("PR-11","PR-06"),                       # incidentes de seguridad se gestionan en la mesa de servicio
 ("PR-13","PR-06"),                       # las alertas de monitoreo generan incidentes en la mesa
]
p = pd.read_csv("PF01_portafolio_candidatos.csv")
G = nx.DiGraph()
G.add_nodes_from(p.codigo)
G.add_edges_from([(b,a) for a,b in DEP])     # arista habilitador → dependiente

desconocidos = {n for e in DEP for n in e} - set(p.codigo)
if desconocidos:
    print(f"⚠ Dependencias con proyectos que no están en el portafolio: {desconocidos}")

print("=== ORDEN TOPOLÓGICO (secuencia obligada) ===")
try:
    orden = list(nx.lexicographical_topological_sort(G))
    print(" → ".join(orden))
    print("\nOleadas (proyectos que pueden ejecutarse en paralelo):")
    for i, gen in enumerate(nx.topological_generations(G), 1):
        print(f"  Oleada {i}: {', '.join(sorted(gen))}")
except nx.NetworkXUnfeasible:
    print("⚠ Existe un ciclo de dependencias: revisar el modelo")

print("\n=== PROYECTOS HABILITADORES (mayor grado de salida) ===")
for n, g in sorted(G.out_degree(), key=lambda x: (-x[1], x[0])):
    if g:
        hab = sorted(nx.descendants(G, n))
        print(f"  {n}: habilita directamente {g} proyecto(s); en cadena {len(hab)}: {', '.join(hab)}")

print("\n=== PROYECTOS SIN DEPENDENCIAS (pueden iniciar de inmediato) ===")
print("  " + ", ".join(n for n in G.nodes if G.in_degree(n) == 0))

os.makedirs("../graficos", exist_ok=True)
cat = dict(zip(p.codigo, p.categoria))
COL = {"Operar":"#16285C","Crecer":"#0EA5E9","Transformar":"#F59E0B"}
for layer, nodes in enumerate(nx.topological_generations(G)):
    for n in nodes:
        G.nodes[n]["layer"] = layer
pos = nx.multipartite_layout(G, subset_key="layer", align="vertical")
plt.figure(figsize=(13,8))
nx.draw(G, pos, with_labels=True, node_color=[COL[cat[n]] for n in G.nodes],
        font_color="white", node_size=2000, font_size=9, arrows=True, arrowsize=18,
        edge_color="#94A3B8")
for c, col in COL.items():
    plt.scatter([], [], c=col, s=150, label=c)
plt.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False)   # fuera del área de nodos
plt.title("Mapa de dependencias del portafolio (izquierda → derecha: habilitador → dependiente)")
plt.savefig("../graficos/PF_dependencias.png", dpi=140, bbox_inches="tight")
print("\nGráfico: graficos/PF_dependencias.png")
