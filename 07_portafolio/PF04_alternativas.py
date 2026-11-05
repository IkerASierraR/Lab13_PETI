# 07_portafolio/PF04_alternativas.py
# Casos de negocio de los tres proyectos de mayor TCO (PR-08, PR-03, PR-02) · COOPAC Frontera Sur
# La alternativa B de cada caso toma su costo único y su costo anual de PF02_tco.csv,
# de modo que el caso de negocio y el TCO de la ficha no pueden contradecirse.
import pandas as pd
AÑOS = 5

tco = pd.read_csv("PF02_tco.csv").set_index("codigo")
def b(p):  # (inversión única, costo anual) de la alternativa B = TCO de PF02
    return float(tco.loc[p, "costo_unico"]), float(tco.loc[p, "costo_anual"])

# Gasto operativo anual: el presupuesto de TI (S/ 1 240 000) es el 2.9 % de los gastos operativos
GASTO_OP = 1240000 / 0.029          # ≈ S/ 42.8 millones
DIA_OP   = GASTO_OP / 365           # ≈ S/ 117 000 por día de operación

ALT = pd.DataFrame([
 # proyecto, alternativa, inv_inicial, costo_anual, beneficio_anual, descripcion
 ("PR-08","A. No hacer nada", 0, 0, -190000,
  "El sistema central pierde soporte del fabricante y opera al límite de su capacidad (expediente de servidores 2024). "
  "Se estiman 2 días/año de interrupción × S/ 117 000 de gasto operativo diario × 50 % no recuperable (≈ S/ 117 000), "
  "S/ 45 000/año de soporte extendido y correcciones de emergencia y S/ 28 000/año de reprocesos."),
 ("PR-08","B. Migrar a la versión soportada del mismo proveedor", *b("PR-08"), 260000,
  "Evita el costo de la inacción (S/ 190 000/año) y aporta S/ 70 000/año por reportes regulatorios y cierres más rápidos. "
  "Menor riesgo de migración de datos; mantiene la dependencia del proveedor actual."),
 ("PR-08","C. Reemplazar por otro sistema central cooperativo", 480000, 170000, 290000,
  "Elimina la dependencia y habilita integración nativa; mayor costo, 20 meses de implantación y "
  "riesgo alto de migración de los saldos de los socios (incertidumbre superior a ±60 %)."),

 ("PR-03","A. No hacer nada", 0, 0, -110000,
  "Se mantienen ≈ 96 000 operaciones al año en ventanilla (consulta de saldo y pago de cuotas): costo de atención "
  "≈ S/ 75 000/año y margen perdido por socios que migran a entidades con canal digital ≈ S/ 35 000/año."),
 ("PR-03","B. Banca móvil y web propias, con consulta de saldos y crédito", *b("PR-03"), 170000,
  "Migra el 60 % de las operaciones de ventanilla al canal digital y capta socios nuevos. "
  "Requiere la capa de integración (PR-02) y el dato maestro de socios (PR-01)."),
 ("PR-03","C. Plataforma de banca digital contratada como servicio", 290000, 110000, 200000,
  "Salida a producción más rápida y menor deuda técnica; mayor costo anual y dependencia de un proveedor."),

 ("PR-02","A. No hacer nada", 0, 0, -85000,
  "Las integraciones punto a punto entre el sistema central, cajas y canales se mantienen: conciliación manual "
  "diaria (2 personas a medio tiempo ≈ S/ 48 000/año), reprocesos (≈ S/ 22 000/año) y reportes armados a mano (≈ S/ 15 000/año)."),
 ("PR-02","B. Plataforma de integración (iPaaS) en la nube", *b("PR-02"), 125000,
  "Elimina la conciliación manual y los reprocesos (S/ 85 000/año) y aporta S/ 40 000/año de beneficio propio. "
  "Es habilitador: PR-03, PR-04, PR-05, PR-08 y PR-09 dependen de él (su beneficio no se cuenta aquí)."),
 ("PR-02","C. Desarrollo de APIs a medida sin plataforma", 160000, 62000, 105000,
  "Menor costo anual, pero cada integración nueva se desarrolla desde cero, depende de un solo desarrollador y "
  "no tiene monitoreo centralizado."),
], columns=["proyecto","alternativa","inv_inicial","costo_anual","beneficio_anual","descripcion"])

ALT["costo_5"]     = ALT.inv_inicial + ALT.costo_anual * AÑOS
ALT["beneficio_5"] = ALT.beneficio_anual * AÑOS
ALT["neto_5"]      = ALT.beneficio_5 - ALT.costo_5
ALT["retorno_pct"] = (ALT.neto_5 / ALT.costo_5.where(ALT.costo_5 > 0) * 100).round(1)  # A: sin costo → vacío

print(f"Supuesto: gasto operativo anual ≈ S/ {GASTO_OP:,.0f} · día de operación ≈ S/ {DIA_OP:,.0f}")
for p, g in ALT.groupby("proyecto", sort=False):
    print(f"\n{'='*95}\n{p}")
    print(g[["alternativa","inv_inicial","costo_5","beneficio_5","neto_5","retorno_pct"]].to_string(index=False))
    mejor = g.loc[g.neto_5.idxmax()]
    print(f"→ Mayor beneficio neto a 5 años: {mejor.alternativa} (S/ {mejor.neto_5:,.0f})")
    base = g[g.alternativa.str.startswith("A.")].iloc[0]
    print(f"→ Costo de la inacción a 5 años: S/ {abs(base.beneficio_5):,.0f}")
ALT.to_csv("PF04_alternativas.csv", index=False, encoding="utf-8")
