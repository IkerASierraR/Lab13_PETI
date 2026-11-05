# 07_portafolio/PF04_alternativas.py
# Casos de negocio de los tres proyectos de mayor TCO (PR-08, PR-03, PR-02)
# Alternativa B de cada caso = la ficha y el TCO de PF02 (costo único y costo anual).
# beneficio_anual de B y C = costo de la inacción evitado + beneficio incremental.
import pandas as pd
AÑOS = 5

# Facturación anual: presupuesto TI S/ 742 000 = 1.08 % de la facturación (expediente de inversiones)
FACTURACION = 742000 / 0.0108          # ≈ S/ 68.7 millones
VENTA_DIA   = FACTURACION / 365        # ≈ S/ 188 000 por día

ALT = pd.DataFrame([
 # proyecto, alternativa, inv_inicial, costo_anual, beneficio_anual, descripcion
 ("PR-08","A. No hacer nada",                                       0,      0, -180000,
  "La versión actual del ERP pierde soporte del fabricante: sin parches de seguridad. Se estiman 2 días/año de "
  "interrupción × S/ 188 000 de venta diaria × 40 % de venta no recuperada (≈ S/ 150 000) más S/ 30 000/año "
  "de soporte extendido y correcciones de emergencia."),
 ("PR-08","B. Migrar a la versión soportada del mismo proveedor", 230000, 110100, 220000,
  "Evita el costo de la inacción (S/ 180 000) y aporta S/ 40 000/año en cierres contables más rápidos. "
  "Menor riesgo de migración de datos; mantiene la dependencia del proveedor actual."),
 ("PR-08","C. Reemplazar por otra solución ERP",                  380000, 120000, 250000,
  "Elimina la dependencia y habilita integración nativa; mayor costo, 18 meses de implantación y "
  "riesgo alto de migración (la incertidumbre de la estimación supera ±60 %)."),

 ("PR-03","A. No hacer nada",                                       0,      0,  -95000,
  "Se mantienen 74 400 pedidos anuales tomados por teléfono: tiempo de la fuerza de ventas en toma de "
  "pedidos (≈ S/ 70 000/año) y errores de transcripción con notas de crédito (≈ S/ 25 000/año)."),
 ("PR-03","B. Rediseño móvil del portal existente + consulta de pedido", 151000, 67500, 145000,
  "Aprovecha el desarrollo existente; migra el 50 % de los pedidos telefónicos al canal y elimina las "
  "llamadas de consulta de estado. Requiere la capa de integración (PR-02) y el dato maestro (PR-01)."),
 ("PR-03","C. Nueva plataforma de comercio B2B",                  260000,  90000, 175000,
  "Mayor capacidad y menor deuda técnica; mayor costo y 14 meses de implantación."),

 ("PR-02","A. No hacer nada",                                       0,      0,  -70000,
  "Las integraciones punto a punto entre ERP, almacén y portal se mantienen: conciliación manual diaria "
  "(2 personas a medio tiempo ≈ S/ 45 000/año) y reprocesos por pedidos duplicados (≈ S/ 25 000/año)."),
 ("PR-02","B. Plataforma de integración (iPaaS) en la nube",      101000,  71640, 100000,
  "Elimina la conciliación manual y los reprocesos; aporta S/ 30 000/año de beneficio propio. Es "
  "habilitador: PR-03, PR-04, PR-05, PR-08 y PR-13 dependen de él (su beneficio no se cuenta aquí)."),
 ("PR-02","C. Desarrollo de APIs a medida sin plataforma",        140000,  55000,  85000,
  "Menor costo anual, pero cada nueva integración se desarrolla desde cero y depende de un solo "
  "desarrollador; sin monitoreo centralizado."),
], columns=["proyecto","alternativa","inv_inicial","costo_anual","beneficio_anual","descripcion"])

ALT["costo_5"]     = ALT.inv_inicial + ALT.costo_anual * AÑOS
ALT["beneficio_5"] = ALT.beneficio_anual * AÑOS
ALT["neto_5"]      = ALT.beneficio_5 - ALT.costo_5
ALT["retorno_pct"] = (ALT.neto_5 / ALT.costo_5.where(ALT.costo_5 > 0) * 100).round(1)  # A: sin costo → vacío

print(f"Supuesto: facturación anual ≈ S/ {FACTURACION:,.0f} · venta diaria ≈ S/ {VENTA_DIA:,.0f}")
for p, g in ALT.groupby("proyecto", sort=False):
    print(f"\n{'='*95}\n{p}")
    print(g[["alternativa","inv_inicial","costo_5","beneficio_5","neto_5","retorno_pct"]].to_string(index=False))
    mejor = g.loc[g.neto_5.idxmax()]
    print(f"→ Mayor beneficio neto a 5 años: {mejor.alternativa} (S/ {mejor.neto_5:,.0f})")
    base = g[g.alternativa.str.startswith("A.")].iloc[0]
    print(f"→ Costo de la inacción a 5 años: S/ {abs(base.beneficio_5):,.0f}")
ALT.to_csv("PF04_alternativas.csv", index=False, encoding="utf-8")
