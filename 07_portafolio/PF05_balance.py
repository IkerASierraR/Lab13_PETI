# 07_portafolio/PF05_balance.py
# Balance operar/crecer/transformar del portafolio y contraste con el presupuesto actual
import os
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

p   = pd.read_csv("PF01_portafolio_candidatos.csv")
tco = pd.read_csv("PF02_tco.csv")
d   = p.merge(tco, on="codigo")

bal = d.groupby("categoria").agg(
    proyectos=("codigo","count"),
    inversion=("inv_inicial","sum"),
    tco=("tco_5","sum")).reset_index()
bal["pct_inv"] = (bal.inversion/bal.inversion.sum()*100).round(1)
bal["pct_tco"] = (bal.tco/bal.tco.sum()*100).round(1)

REF = {"Operar":(50,70), "Crecer":(20,30), "Transformar":(10,20)}
print("=== BALANCE DEL PORTAFOLIO PROPUESTO ===")
print(bal.to_string(index=False))
print("\nContraste con las proporciones de referencia:")
for _, r in bal.iterrows():
    lo, hi = REF.get(r.categoria, (0,100))
    est = "dentro del rango" if lo <= r.pct_tco <= hi else ("POR DEBAJO" if r.pct_tco < lo else "POR ENCIMA")
    print(f"  {r.categoria:12s}: {r.pct_tco:5.1f} % del TCO  (referencia {lo}–{hi} %)  → {est}")

# Balance ACTUAL del presupuesto de TI (Sección 3.1): presupuesto_ti.csv
pre = pd.read_csv("insumos/presupuesto_ti.csv")
# «Proyectos nuevos» es la única partida de inversión; no distingue crecer de transformar
pre["categoria"] = pre.tipo.map({"Operación":"Operar", "Inversión":"Crecer / Transformar"})
act = pre.groupby("categoria")[["planificado","ejecutado"]].sum()
act["pct_plan"] = (act.planificado/act.planificado.sum()*100).round(1)
act["pct_ejec"] = (act.ejecutado/act.ejecutado.sum()*100).round(1)
print("\n=== BALANCE ACTUAL DE LA ORGANIZACIÓN (presupuesto de TI, Sección 3.1) ===")
print(act.to_string())
inv_plan, inv_ejec = pre[pre.tipo=="Inversión"][["planificado","ejecutado"]].sum()
print(f"  Partida «Proyectos nuevos»: planificado S/ {inv_plan:,.0f}, ejecutado S/ {inv_ejec:,.0f} "
      f"({(inv_ejec/inv_plan-1)*100:+.1f} %)")
op = bal.set_index("categoria").pct_tco.get("Operar", 0)
print("\n=== CAMBIO DE BALANCE QUE PROPONE EL PLAN ===")
print(f"  Hoy     : Operar {act.loc['Operar','pct_ejec']:.1f} % · Crecer + Transformar {100-act.loc['Operar','pct_ejec']:.1f} % (ejecutado)")
print(f"  Propuesto: Operar {op:.1f} % · Crecer + Transformar {100-op:.1f} % (TCO del portafolio)")
print("→ El portafolio pasa de un presupuesto casi íntegramente operativo a dedicar cerca de la mitad")
print("  del TCO a crecer y transformar. El PETI debe justificar ese cambio y su financiamiento.")

os.makedirs("../graficos", exist_ok=True)
fig, ax = plt.subplots(1, 3, figsize=(18,5.5))
COL = {"Operar":"#16285C","Crecer":"#0EA5E9","Transformar":"#F59E0B","Crecer / Transformar":"#0EA5E9"}
ax[0].pie(act.planificado, labels=act.index, autopct="%1.1f%%",
          colors=[COL[c] for c in act.index], startangle=90)
ax[0].set_title("Balance ACTUAL · presupuesto TI 2025")
ax[1].pie(bal.tco, labels=bal.categoria, autopct="%1.1f%%",
          colors=[COL[c] for c in bal.categoria], startangle=90)
ax[1].set_title("Balance PROPUESTO · TCO a 5 años")
s = d.sort_values("tco_5")
ax[2].barh(s.codigo, s.tco_5, color=[COL[c] for c in s.categoria],
           xerr=[s.tco_5-s.tco_min, s.tco_max-s.tco_5], ecolor="#94A3B8", capsize=3)
ax[2].set_xlabel("TCO a 5 años (S/) · barra de error = margen de incertidumbre")
ax[2].set_title("TCO por proyecto")
plt.tight_layout(); plt.savefig("../graficos/PF_balance.png", dpi=140)
print("\nGráfico: graficos/PF_balance.png")
