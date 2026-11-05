# 07_portafolio/PF07_validacion.py
# Paso F · Las tres comprobaciones del taller, ejecutadas sobre los archivos producidos.
import glob
import pandas as pd

p   = pd.read_csv("PF01_portafolio_candidatos.csv")
tco = pd.read_csv("PF02_tco.csv")
alt = pd.read_csv("PF04_alternativas.csv")
ok = True

print("=== 1. Cada proyecto cita el objetivo al que responde ===")
sin = p[p.objetivo.isna() | (p.objetivo.astype(str).str.strip() == "")]
fichas = sorted(glob.glob("PF03_fichas/PR-*.md"))
sin_ficha_obj = [f for f in fichas if "**Objetivo al que contribuye** | OD-" not in open(f, encoding="utf-8").read()]
print(f"  Proyectos sin objetivo en PF01: {len(sin)} · fichas sin objetivo: {len(sin_ficha_obj)} de {len(fichas)}")
ok &= sin.empty and not sin_ficha_obj and len(fichas) == len(p)

print("\n=== 2. Los duplicados fusionados no perdieron alcance ===")
CLAVE = {"C-04": "consulta de saldos", "C-12": "registro de actividades de tratamiento"}
for _, r in p[p.fusiona.notna() & (p.fusiona.astype(str) != "")].iterrows():
    ficha = open(f"PF03_fichas/{r.codigo}.md", encoding="utf-8").read().lower()
    clave = CLAVE[r.fusiona]
    en_alcance = clave in ficha.split("| 7 | alcance incluido")[1].split("| 8 |")[0] or \
                 clave in ficha.split("| 9 | entregables")[1].split("| 10 |")[0]
    print(f"  {r.codigo} absorbe {r.fusiona}: «{clave}» en alcance o entregables → {'sí' if en_alcance else 'NO'}")
    ok &= en_alcance

print("\n=== 3. El TCO a 5 años incluye el costo operativo, no solo la inversión ===")
sin_op = tco[(tco.costo_anual <= 0) | (tco.tco_5 <= tco.costo_unico)]
print(f"  Proyectos con TCO = solo inversión: {len(sin_op)} de {len(tco)}")
ok &= sin_op.empty
for proy, g in alt.groupby("proyecto"):
    b = g[g.alternativa.str.startswith("B.")].iloc[0]
    t = tco[tco.codigo == proy].iloc[0]
    coincide = abs(b.costo_5 - t.tco_5) < 1
    print(f"  {proy}: costo 5 años de la alternativa B = TCO de la ficha → {'sí' if coincide else 'NO'}")
    ok &= coincide

print("\n=== Otras comprobaciones de la lista 3.2 ===")
print(f"  Proyectos en el portafolio: {len(p)} (mínimo 12) → {'sí' if len(p) >= 12 else 'NO'}")
n_casos = alt.proyecto.nunique()
inaccion = alt[alt.alternativa.str.startswith("A.")]
tres_mayores = list(tco.nlargest(3, "tco_5").codigo)
print(f"  Casos de negocio: {n_casos} · con «no hacer nada» cuantificado: {(inaccion.beneficio_anual < 0).sum()}")
print(f"  Los casos corresponden a los 3 proyectos de mayor TCO {tres_mayores} → {'sí' if set(alt.proyecto) == set(tres_mayores) else 'NO'}")
ok &= len(p) >= 12 and n_casos == 3 and (inaccion.beneficio_anual < 0).all() and set(alt.proyecto) == set(tres_mayores)

print("\nRESULTADO:", "todas las comprobaciones pasan" if ok else "HAY COMPROBACIONES QUE FALLAN")
