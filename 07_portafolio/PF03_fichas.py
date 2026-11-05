# 07_portafolio/PF03_fichas.py
# Genera la ficha estandarizada de 20 campos de cada proyecto en PF03_fichas/PR-NN.md.
# Los campos cuantitativos salen de PF01, PF02 y PF06; los cualitativos se escriben aquí.
import os
import pandas as pd

p   = pd.read_csv("PF01_portafolio_candidatos.csv")
tco = pd.read_csv("PF02_tco.csv")
d   = p.merge(tco, on="codigo").set_index("codigo")

# Mismo modelo de dependencias que PF06 (proyecto, depende_de)
DEP = [("PR-01","PR-11"),("PR-03","PR-02"),("PR-03","PR-01"),("PR-04","PR-02"),("PR-04","PR-01"),
       ("PR-05","PR-01"),("PR-05","PR-02"),("PR-08","PR-02"),("PR-08","PR-07"),("PR-09","PR-01"),
       ("PR-10","PR-06"),("PR-12","PR-06"),("PR-13","PR-02")]

# problema, incluido, excluido, entregables, esfuerzo_pm, beneficio, riesgos, responsable, area, exito
F = {
"PR-01": ("Clientes y productos duplicados entre ERP, almacén y portal: el diagnóstico (Sección 5.4.2) "
          "encontró ≈ 18 % de clientes duplicados, que generan despachos a direcciones erróneas.",
          "Maestros de cliente, producto y proveedor; dueños del dato; reglas de calidad; depuración inicial.",
          "Datos de RR. HH. y contables; herramienta MDM comercial.",
          "Política de datos maestros · matriz de dueños · maestros depurados · tablero de calidad del dato.",
          14, "Duplicidad de clientes de 18 % a < 2 %; −30 % de despachos fallidos por dirección.",
          "Resistencia de las áreas a asumir la propiedad del dato; depuración más larga de lo estimado.",
          "Jefe de TI con Analista de datos", "Comercial, Logística, Finanzas",
          "Duplicidad < 2 % medida por el tablero de calidad a los 6 meses del cierre."),
"PR-02": ("Integraciones punto a punto entre ERP, almacén y portal: conciliación manual diaria y pedidos duplicados.",
          "Plataforma de integración, APIs de pedido, stock, cliente y precio; monitoreo de integraciones.",
          "Reescritura de sistemas existentes; integración con proveedores externos.",
          "Plataforma operativa · 8 APIs publicadas · catálogo de APIs · tablero de monitoreo.",
          22, "Elimina S/ 45 000/año de conciliación manual y S/ 25 000/año de reprocesos; habilita 5 proyectos.",
          "Dependencia de un proveedor de iPaaS; falta de habilidades internas en integración.",
          "Jefe de TI", "Todas las áreas operativas",
          "0 conciliaciones manuales diarias y 99.5 % de mensajes procesados sin error en 3 meses."),
"PR-03": ("74 400 pedidos anuales se toman por teléfono; el portal B2B actual no se usa en móvil y no muestra el estado del pedido.",
          "Rediseño móvil del portal, catálogo con precio por cliente, pedido en línea, consulta de estado.",
          "Pagos en línea; venta a consumidor final (B2C).",
          "Portal B2B móvil · módulo de consulta de pedido · plan de adopción con la fuerza de ventas.",
          30, "50 % de los pedidos por el canal digital; −S/ 95 000/año de costo de toma de pedidos.",
          "Baja adopción de clientes mayoristas; dependencia de PR-01 y PR-02.",
          "Gerente Comercial (patrocinador) y Jefe de TI", "Comercial y clientes mayoristas",
          "≥ 50 % de los pedidos ingresados por el canal digital a los 12 meses."),
"PR-04": ("Rutas armadas a mano y sin trazabilidad: el cliente llama para saber dónde está su pedido.",
          "Planificación de rutas, app de despacho con prueba de entrega, seguimiento en línea.",
          "Gestión de flota (mantenimiento de vehículos, combustible).",
          "Herramienta de ruteo · app móvil de despacho · indicador de entregas a tiempo.",
          10, "−10 % de kilómetros recorridos; entregas a tiempo de 82 % a 95 %.",
          "Conectividad móvil en rutas alejadas; adopción de los conductores.",
          "Jefe de Logística", "Logística y Despacho",
          "Entregas a tiempo ≥ 95 % durante 3 meses consecutivos."),
"PR-05": ("La gerencia comercial recibe reportes en Excel con 10 días de retraso y cifras que no cuadran.",
          "Tablero de ventas, margen y cartera por vendedor, zona y cliente, sobre datos integrados.",
          "Modelos predictivos; reportes financieros regulatorios.",
          "Modelo de datos comercial · tablero publicado · manual de indicadores.",
          5, "Reporte disponible en D+1 en lugar de D+10.",
          "Calidad del dato insuficiente si PR-01 se retrasa.",
          "Analista de datos", "Gerencia Comercial",
          "Tablero actualizado diariamente y usado por el 100 % de los jefes de zona."),
"PR-06": ("Los incidentes se reportan por WhatsApp y llamada; no hay registro, prioridad ni tiempo de respuesta medido.",
          "Herramienta de mesa de servicio, catálogo de servicios, acuerdos de nivel de servicio, proceso de incidentes.",
          "Soporte a clientes externos.",
          "Mesa de servicio operativa · catálogo de servicios · ANS publicados · reporte mensual.",
          8, "100 % de incidentes registrados; tiempo de atención medido por primera vez.",
          "Usuarios que siguen pidiendo soporte por canales informales.",
          "Jefe de TI", "Todas las áreas",
          "≥ 95 % de incidentes registrados en la herramienta y 90 % atendidos dentro del ANS."),
"PR-07": ("El sistema de respaldo de 2025 (expediente 1, +30.4 % de desviación) nunca se probó con una restauración.",
          "Respaldo inmutable fuera del sitio, plan de continuidad, pruebas semestrales de restauración.",
          "Sitio alterno completo (DRP en caliente).",
          "Política de respaldo · respaldo inmutable · plan de continuidad · actas de prueba de restauración.",
          9, "Tiempo de recuperación objetivo ≤ 8 h, verificado por prueba.",
          "Repetir el error del expediente 1: comprar sin probar la restauración.",
          "Jefe de TI", "Toda la organización",
          "Dos pruebas de restauración exitosas en 12 meses dentro de 8 h."),
"PR-08": ("La versión del ERP pierde soporte del fabricante: sin parches de seguridad y con riesgo de interrupción.",
          "Migración a la versión soportada, depuración de personalizaciones, pruebas y capacitación.",
          "Reemplazo por otro ERP (alternativa C del caso de negocio); nuevos módulos.",
          "ERP migrado · personalizaciones documentadas · plan de pruebas aprobado · acta de aceptación.",
          40, "Evita S/ 180 000/año de costo de inacción; −3 días en el cierre contable mensual.",
          "Personalizaciones no documentadas; migración de datos; incertidumbre ±50 %.",
          "Gerente de Administración y Finanzas (patrocinador) y Jefe de TI", "Toda la organización",
          "ERP en versión soportada, con 0 incidentes críticos en el primer mes y acta de aceptación firmada."),
"PR-09": ("La organización trata datos personales de clientes y trabajadores sin bancos inscritos ni registro de tratamiento (Ley 29733).",
          "Inventario y registro de actividades de tratamiento, inscripción de bancos de datos, políticas y consentimientos.",
          "Certificaciones internacionales (ISO 27701).",
          "Registro de tratamiento · bancos inscritos en la ANPD · política de privacidad · capacitación.",
          6, "Evita multas de hasta 100 UIT por infracción muy grave; no tiene retorno financiero directo.",
          "Que se postergue por no tener retorno; cambios en la normativa.",
          "Oficial de datos personales (por designar) con Asesoría Legal", "Legal, RR. HH., Comercial",
          "100 % de bancos de datos inscritos y registro de tratamiento aprobado."),
"PR-10": ("El conocimiento técnico depende de dos personas; no hay inventario de configuración.",
          "Base de conocimiento, base de datos de configuración (CMDB) y procedimientos documentados.",
          "Gestión documental de toda la organización.",
          "Base de conocimiento con ≥ 60 artículos · CMDB de servicios críticos · procedimientos.",
          5, "−20 % en el tiempo de resolución de incidentes repetitivos.",
          "Falta de tiempo del equipo para documentar.",
          "Jefe de TI", "Tecnologías de la Información",
          "≥ 60 artículos publicados y 100 % de servicios críticos en la CMDB."),
"PR-11": ("Las inversiones de TI se aprueban sin caso de negocio ni medición posterior: los tres expedientes de 2025 "
          "suman +19.9 % de desviación y ninguno midió su beneficio.",
          "Comité de gobierno de TI, reglamento, criterios de aprobación de inversiones y seguimiento de beneficios.",
          "Gobierno corporativo fuera de TI.",
          "Reglamento del comité · plantilla de caso de negocio · actas trimestrales · informe de beneficios.",
          2, "Toda inversión con caso de negocio y medición posterior; desviación presupuestal ≤ 10 %.",
          "Comité que se reúne una vez y no vuelve a hacerlo.",
          "Gerente General (preside)", "Gerencia",
          "4 sesiones al año con acta y 100 % de inversiones aprobadas con caso de negocio."),
"PR-12": ("La disponibilidad de los servicios no se mide (Sección 6.1.5): las caídas se conocen cuando el usuario reclama.",
          "Monitoreo de servidores, enlaces y aplicaciones críticas; alertas a la mesa de servicio.",
          "Monitoreo de seguridad (SOC).",
          "Plataforma de monitoreo · tablero de disponibilidad · reporte mensual de disponibilidad.",
          5, "Línea base de disponibilidad medida; detección de caídas antes que el usuario.",
          "Ruido de alertas que el equipo deja de atender.",
          "Jefe de TI", "Tecnologías de la Información",
          "Disponibilidad medida de 100 % de servicios críticos y ≥ 99.5 % mensual."),
"PR-13": ("Las boletas y solicitudes de vacaciones se gestionan en papel: ≈ 3 000 trámites al año en RR. HH.",
          "Portal de autoservicio de boletas, vacaciones y constancias, integrado con planillas.",
          "Selección de personal y evaluación de desempeño.",
          "Portal de autoservicio · integración con planillas · firma digital de boletas.",
          6, "−80 % de trámites presenciales en RR. HH.",
          "Trabajadores de almacén sin acceso a correo o dispositivo.",
          "Jefe de Recursos Humanos", "Recursos Humanos y todos los trabajadores",
          "≥ 80 % de boletas y vacaciones gestionadas por el portal a los 6 meses."),
}

def s(x): return f"S/ {x:,.0f}".replace(",", " ")

os.makedirs("PF03_fichas", exist_ok=True)
for cod, (prob, inc, exc, ent, pm, ben, rie, resp, area, exito) in F.items():
    r = d.loc[cod]
    dep_de  = [b for a, b in DEP if a == cod]
    habilita = [a for a, b in DEP if b == cod]
    md = f"""# {cod} · {r.nombre}

> Ficha estandarizada de proyecto · PETI Distribuidora Andina del Sur S.A.C. · Sección 7.1.3
> Información confidencial. Cifras en soles, estimaciones de orden de magnitud con su margen.

| # | Campo | Contenido |
|---|---|---|
| 1 | Código | {cod} (candidato {r.candidato}{', fusiona ' + r.fusiona if isinstance(r.fusiona, str) and r.fusiona else ''}) |
| 2 | Nombre | {r.nombre} |
| 3 | **Fuente** | {r.fuente} · {r.seccion_origen} |
| 4 | **Objetivo al que contribuye** | {r.objetivo} |
| 5 | Categoría | {r.categoria} |
| 6 | Problema que resuelve | {prob} |
| 7 | Alcance incluido | {inc} |
| 8 | **Alcance excluido** | {exc} |
| 9 | Entregables | {ent} |
| 10 | Duración estimada | {int(r.meses)} meses |
| 11 | Esfuerzo estimado | {pm} persona-mes |
| 12 | **Inversión inicial** | {s(r.inv_inicial)} (costo único con capacitación, migración e integración: {s(r.costo_unico)}) |
| 13 | **Costo operativo anual** | {s(r.costo_anual)} |
| 14 | **TCO a 5 años** | {s(r.tco_5)} · rango {s(r.tco_min)} – {s(r.tco_max)} ({r.incertidumbre}) · factor TCO/inversión {r.factor_tco_inv:.2f}× |
| 15 | Beneficio cuantificado | {ben} |
| 16 | **Dependencias** | Depende de: {', '.join(dep_de) or 'ninguno'} · Habilita: {', '.join(habilita) or 'ninguno'} |
| 17 | Riesgos principales | {rie} |
| 18 | Responsable propuesto | {resp} |
| 19 | Área usuaria | {area} |
| 20 | Criterio de éxito | {exito} |

Fuente de las cifras: [`PF02_tco.csv`](../PF02_tco.csv) · dependencias: [`PF06_dependencias.py`](../PF06_dependencias.py)
"""
    with open(f"PF03_fichas/{cod}.md", "w", encoding="utf-8") as fh:
        fh.write(md)

faltan = set(d.index) - set(F)
print(f"Fichas generadas: {len(F)} de {len(d)} proyectos" + (f" · ⚠ faltan {sorted(faltan)}" if faltan else ""))
print("Campos por ficha: 20")
