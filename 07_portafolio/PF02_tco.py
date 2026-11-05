# 07_portafolio/PF02_tco.py
# Costo total de propiedad (TCO) a 5 años · COOPAC Frontera Sur
# Cifras en soles (S/): estimaciones de orden de magnitud con su margen de incertidumbre.
import pandas as pd

AÑOS = 5

# --- 1. Línea base del costo operativo: gasto real en servicios informáticos (pagos.csv) ---
pagos = pd.read_csv("insumos/pagos.csv")
ti = pagos[pagos.concepto.str.contains("inform", case=False)]
presup = pd.read_csv("insumos/presupuesto_ti.csv")
print("=== LÍNEA BASE · GASTO REAL EN PROVEEDORES DE TI (pagos 2025) ===")
print(f"Pagos por «Servicio informático»: {len(ti):,} comprobantes · {ti.codigo_proveedor.nunique()} proveedores")
print(f"Monto pagado                     : S/ {ti.monto.sum():,.0f}  (promedio S/ {ti.monto.mean():,.0f} por pago)")
print(f"Presupuesto de TI aprobado       : S/ {presup.planificado.sum():,.0f}")
print(f"→ El gasto en servicios informáticos es {ti.monto.sum()/presup.planificado.sum():.1f}× el presupuesto de TI:"
      " parte del gasto de TI ocurre fuera del presupuesto del área. El costo operativo del TCO"
      " no puede estimarse solo con el presupuesto aprobado.")

# --- 2. Costos por proyecto ---
PROYECTOS = pd.DataFrame([
 # codigo, inversion_inicial, licencias_anual, infraestructura_anual, soporte_pct,
 # personal_anual, capacitacion_inicial, migracion, integracion, meses, incertidumbre_pct
 ("PR-01",  70000,  8000,  4800, .15, 30000,  8000, 15000, 10000,  7, 30),
 ("PR-02",  95000, 15000, 12000, .18, 42000, 10000,     0, 20000,  8, 40),
 ("PR-03", 130000, 14400, 12000, .15, 36000, 15000,  8000, 25000, 10, 35),
 ("PR-04",  85000, 12000,  6000, .15, 24000,  8000, 10000, 12000,  7, 40),
 ("PR-05",  22000,  4800,  2400, .12,  9000,  4000,     0,  3000,  3, 20),
 ("PR-06",  30000,  4200,  2400, .15, 12000,  5000,  3000,  6000,  4, 25),
 ("PR-07",  78000,  9000,  9600, .12, 15000,  5000,     0,     0,  5, 25),
 ("PR-08", 210000, 36000, 18000, .18, 60000, 25000, 45000, 35000, 14, 50),
 ("PR-09",  65000, 12000,  3600, .15, 24000,  8000,  6000, 10000,  6, 30),
 ("PR-10",  28000,     0,     0, .10, 14000,  6000,     0,     0,  4, 20),
 ("PR-11",  90000, 14400,  6000, .15, 36000, 10000,     0,  8000,  8, 30),
 ("PR-12",   7000,     0,     0, .00,  3500,  2000,     0,     0,  2, 15),
 ("PR-13",  24000,  3600,  2400, .12,  9000,  4000,     0,  3000,  3, 25),
], columns=["codigo","inv_inicial","licencias","infra","soporte_pct","personal",
            "capacitacion","migracion","integracion","meses","incertidumbre_pct"])

P = PROYECTOS.copy()
P["soporte_anual"] = (P.inv_inicial * P.soporte_pct).round(0)
P["costo_anual"]   = P.licencias + P.infra + P.soporte_anual + P.personal
P["costo_unico"]   = P.inv_inicial + P.capacitacion + P.migracion + P.integracion
P["tco_5"]         = P.costo_unico + P.costo_anual * AÑOS
P["tco_min"]       = (P.tco_5 * (1 - P.incertidumbre_pct/100)).round(-2)
P["tco_max"]       = (P.tco_5 * (1 + P.incertidumbre_pct/100)).round(-2)
P["pct_operativo"] = ((P.costo_anual * AÑOS) / P.tco_5 * 100).round(1)
P["factor_tco_inv"]= (P.tco_5 / P.inv_inicial).round(2)
P["incertidumbre"] = "±" + P.incertidumbre_pct.astype(str) + " %"

P = P.sort_values("tco_5", ascending=False)
P.to_csv("PF02_tco.csv", index=False, encoding="utf-8")

print("\n=== COSTO TOTAL DE PROPIEDAD A 5 AÑOS ===")
print(P[["codigo","inv_inicial","costo_unico","costo_anual","tco_5","tco_min","tco_max",
         "factor_tco_inv","pct_operativo","incertidumbre"]].to_string(index=False))
f = P.tco_5.sum()/P.inv_inicial.sum()
print(f"\nInversión inicial total : S/ {P.inv_inicial.sum():,.0f}")
print(f"TCO total a 5 años      : S/ {P.tco_5.sum():,.0f}  (rango S/ {P.tco_min.sum():,.0f} – S/ {P.tco_max.sum():,.0f})")
print(f"Factor TCO/inversión    : {f:.2f}×")
print(f"\n→ El TCO es {f:.1f} veces la inversión inicial. Presentar solo la inversión inicial ante la")
print(f"  gerencia subestima el compromiso en S/ {P.tco_5.sum()-P.inv_inicial.sum():,.0f}, que se pagaría")
print(f"  como gasto recurrente que nadie aprobó explícitamente.")
print(f"→ Costo operativo anual del portafolio en régimen: S/ {P.costo_anual.sum():,.0f}, "
      f"{P.costo_anual.sum()/presup.planificado.sum()*100:.0f} % del presupuesto de TI actual.")

print("\n=== PROYECTOS CON MAYOR PROPORCIÓN DE COSTO OPERATIVO ===")
print(P.nlargest(4,"pct_operativo")[["codigo","tco_5","factor_tco_inv","pct_operativo"]].to_string(index=False))
print("→ Estos comprometen el presupuesto recurrente durante años: exigen mayor escrutinio.")

print("\n=== VERIFICACIÓN: el TCO incluye costo operativo ===")
sin_op = P[P.costo_anual <= 0]
print("→ Todos los proyectos incluyen costo operativo anual." if sin_op.empty
      else f"⚠ Proyectos sin costo operativo: {list(sin_op.codigo)}")
print("\nTres proyectos de mayor TCO (casos de negocio, PF04):", ", ".join(P.head(3).codigo))
