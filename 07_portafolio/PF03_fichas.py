# 07_portafolio/PF03_fichas.py
# Genera la ficha estandarizada de 20 campos de cada proyecto en PF03_fichas/PR-NN.md · COOPAC Frontera Sur.
# Los campos cuantitativos salen de PF01 y PF02; las dependencias, de PF06 (una sola fuente);
# los cualitativos se escriben aquí. Las cifras marcadas «supuesto» se confirman en la entrevista con el docente.
import ast, os
import pandas as pd

p   = pd.read_csv("PF01_portafolio_candidatos.csv")
tco = pd.read_csv("PF02_tco.csv")
d   = p.merge(tco, on="codigo").set_index("codigo")

# Dependencias: se leen del propio PF06 para que ficha y mapa no puedan contradecirse
SRC_PF06 = open("PF06_dependencias.py", encoding="utf-8").read()
DEP = next(ast.literal_eval(n.value) for n in ast.parse(SRC_PF06).body
           if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "DEP")

# problema, incluido, excluido, entregables, esfuerzo_pm, beneficio, riesgos, responsable, area, exito
F = {
"PR-01": ("Un mismo socio puede figurar con datos distintos en el sistema central, en caja y en créditos "
          "(supuesto: ≈ 12 % de registros duplicados o incompletos); esto frena el scoring, el monitoreo de operaciones y la banca digital.",
          "Maestro único de socios, dueños del dato, reglas de calidad, depuración inicial y tablero de calidad.",
          "Datos contables y de proveedores; compra de una herramienta MDM completa.",
          "Política de datos maestros · matriz de dueños del dato · padrón de socios depurado · tablero de calidad.",
          14, "Registros duplicados o incompletos de ≈ 12 % a < 2 %; habilita 5 proyectos.",
          "Resistencia de las áreas a asumir la propiedad del dato; depuración más larga de lo estimado.",
          "Jefe de TI con el Jefe de Operaciones", "Operaciones, Créditos, Captaciones y Cumplimiento",
          "Registros duplicados < 2 % medidos por el tablero de calidad a los 6 meses del cierre."),
"PR-02": ("El sistema central, las cajas y los canales se comunican con interfaces punto a punto: conciliación manual diaria, "
          "reprocesos y reportes armados a mano (≈ S/ 85 000 al año, supuesto de dos personas a medio tiempo).",
          "Plataforma de integración, APIs de socio, saldo, crédito y movimiento; monitoreo de integraciones.",
          "Reescritura del sistema central; integración con terceros fuera de la cooperativa.",
          "Plataforma operativa · 8 APIs publicadas · catálogo de APIs · tablero de monitoreo.",
          22, "Elimina ≈ S/ 85 000 al año de conciliación y reprocesos; habilita 5 proyectos.",
          "Dependencia de un proveedor de iPaaS; falta de habilidades internas en integración.",
          "Jefe de TI", "Operaciones y Contabilidad",
          "0 conciliaciones manuales diarias y 99.5 % de mensajes procesados sin error en 3 meses."),
"PR-03": ("Las consultas de saldo y los pagos de cuotas se hacen en ventanilla (supuesto: ≈ 96 000 operaciones al año); "
          "la cooperativa no ofrece banca móvil ni web, y no muestra al socio el estado de su crédito.",
          "App móvil y portal web: consulta de saldos y de estado de crédito, historial de movimientos, pago de cuotas.",
          "Apertura de cuentas 100 % en línea; operaciones interbancarias nuevas.",
          "App móvil y portal web · módulo de consulta de saldos y crédito · plan de adopción por agencia.",
          32, "60 % de las operaciones de ventanilla en el canal digital; −S/ 110 000 al año de costo de atención y de fuga de socios.",
          "Baja adopción de socios con poca conectividad; dependencia de PR-01 y PR-02.",
          "Gerente de Operaciones (patrocinador) y Jefe de TI", "Socios y Agencias",
          "≥ 60 % de las consultas de saldo y pagos de cuota en el canal digital a los 12 meses."),
"PR-04": ("La evaluación de créditos se hace con revisión manual del expediente y del historial "
          "(supuesto: 5 días hábiles de plazo promedio), con criterios que varían entre analistas.",
          "Modelo de scoring, reglas de política crediticia, flujo de evaluación y alertas de sobreendeudamiento.",
          "Cobranza judicial; ajuste de tasas.",
          "Modelo de scoring validado · flujo de evaluación automatizado · manual de política de crédito.",
          18, "Plazo de evaluación de 5 a 1 día hábil (supuesto); criterios homogéneos entre analistas.",
          "Modelo con sesgos o mal calibrado; datos insuficientes si PR-01 se retrasa.",
          "Jefe de Créditos con el Jefe de Riesgos", "Créditos y Riesgos",
          "Plazo de evaluación ≤ 1 día hábil en el 80 % de los créditos de consumo a los 6 meses."),
"PR-05": ("Los reportes de cartera y morosidad se arman en hojas de cálculo y llegan al comité "
          "con ≈ 10 días de retraso (supuesto) y cifras que no siempre cuadran.",
          "Tablero de cartera, morosidad, provisiones y colocaciones por agencia y por analista, sobre datos integrados.",
          "Modelos predictivos de morosidad; reportes regulatorios.",
          "Modelo de datos de cartera · tablero publicado · manual de indicadores.",
          6, "Reporte disponible en D+1 en lugar de D+10.",
          "Calidad del dato insuficiente si PR-01 se retrasa.",
          "Jefe de Riesgos", "Gerencia, Créditos y Riesgos",
          "Tablero actualizado cada día y usado por el 100 % de los jefes de agencia."),
"PR-06": ("Los incidentes se reportan por teléfono y mensajería: no hay registro, prioridad ni tiempo de respuesta medido.",
          "Herramienta de mesa de servicio, catálogo de servicios, acuerdos de nivel de servicio, proceso de incidentes.",
          "Soporte a los socios.",
          "Mesa de servicio operativa · catálogo de servicios · ANS publicados · reporte mensual.",
          9, "100 % de incidentes registrados; tiempo de atención medido por primera vez.",
          "Usuarios que siguen pidiendo soporte por canales informales.",
          "Jefe de TI", "Todas las áreas y agencias",
          "≥ 95 % de incidentes registrados en la herramienta y 90 % atendidos dentro del ANS."),
"PR-07": ("El sistema de respaldo de 2025 costó S/ 254 712 frente a S/ 193 410 aprobados (+31.7 %), se compró al proveedor "
          "habitual sin alternativas y no consta una prueba de restauración.",
          "Respaldo inmutable fuera del sitio, plan de continuidad, pruebas semestrales de restauración.",
          "Sitio alterno completo en caliente.",
          "Política de respaldo · respaldo inmutable · plan de continuidad · actas de prueba de restauración.",
          10, "Tiempo de recuperación objetivo ≤ 8 h, verificado por prueba.",
          "Repetir el error del expediente: comprar sin probar la restauración.",
          "Jefe de TI", "Toda la cooperativa",
          "Dos pruebas de restauración exitosas en 12 meses dentro de 8 h."),
"PR-08": ("El equipo que sostiene el sistema central está al límite de su capacidad (justificación de la renovación de "
          "servidores 2024, que costó +46.6 % sobre lo aprobado) y la versión actual pierde soporte del fabricante.",
          "Migración a la versión soportada, depuración de personalizaciones, pruebas, capacitación y paso a producción.",
          "Reemplazo por otro sistema central (alternativa C del caso de negocio); módulos nuevos.",
          "Sistema central migrado · personalizaciones documentadas · plan de pruebas aprobado · acta de aceptación.",
          44, "Evita ≈ S/ 190 000 al año de costo de inacción y aporta ≈ S/ 70 000 al año por reportes más rápidos.",
          "Migración de los saldos de los socios; personalizaciones sin documentar; incertidumbre de ±50 %.",
          "Gerente General (patrocinador) y Jefe de TI", "Toda la cooperativa",
          "Sistema central en versión soportada, 0 incidentes críticos el primer mes y acta de aceptación firmada."),
"PR-09": ("El monitoreo de operaciones inusuales se hace en hojas de cálculo y por revisión manual de listados, "
          "con riesgo de no reportar a tiempo a la UIF y de sanciones del supervisor.",
          "Perfil de socio, reglas de alerta, bandeja de casos, registro de operaciones y reportes a la UIF.",
          "Auditoría externa del sistema; capacitación general del personal (ya incluida en el plan anual).",
          "Motor de alertas · bandeja de casos · matriz de riesgo de socios · reportes automatizados.",
          12, "Evita sanciones del supervisor por incumplimiento; no tiene retorno financiero directo.",
          "Exceso de falsos positivos; datos de socios incompletos si PR-01 se retrasa.",
          "Oficial de Cumplimiento", "Cumplimiento, Operaciones y Captaciones",
          "100 % de las alertas atendidas dentro del plazo interno y 0 observaciones del supervisor sobre el monitoreo."),
"PR-10": ("La cooperativa trata datos personales de socios sin inventario de bancos de datos ni registro de tratamiento (Ley 29733).",
          "Inventario y registro de actividades de tratamiento, bancos de datos, políticas, consentimientos y derechos ARCO.",
          "Certificaciones internacionales (ISO 27701).",
          "Registro de tratamiento · bancos inscritos ante la autoridad · política de privacidad · capacitación.",
          7, "Evita multas por infracción a la Ley 29733; no tiene retorno financiero directo.",
          "Que se postergue por no tener retorno; cambios en la normativa.",
          "Oficial de datos personales (por designar) con Asesoría Legal", "Legal, Operaciones y Captaciones",
          "100 % de bancos de datos inscritos y registro de tratamiento aprobado."),
"PR-11": ("No hay un sistema de gestión de seguridad de la información: la información financiera de los socios se protege "
          "con controles dispersos y sin pruebas, y la normativa del supervisor exige un marco formal.",
          "Política y sistema de gestión de seguridad, gestión de vulnerabilidades, control de accesos y monitoreo de eventos.",
          "Centro de operaciones de seguridad propio las 24 horas.",
          "Política y SGSI aprobados · análisis de riesgos · control de accesos · informe trimestral de vulnerabilidades.",
          16, "Reduce la probabilidad y el impacto de un incidente de seguridad con datos de socios; no tiene retorno financiero directo.",
          "Falta de personal especializado; controles que los usuarios eluden.",
          "Oficial de Seguridad de la Información", "Toda la cooperativa",
          "0 vulnerabilidades críticas abiertas más de 30 días y 100 % de accesos privilegiados revisados cada trimestre."),
"PR-12": ("Las inversiones de TI se aprueban sin caso de negocio ni medición posterior: los tres expedientes cerrados "
          "suman +22.8 % de desviación y ninguno midió su beneficio.",
          "Comité de gobierno de TI, reglamento, criterios de aprobación de inversiones y seguimiento de beneficios.",
          "Gobierno corporativo fuera de TI.",
          "Reglamento del comité · plantilla de caso de negocio · actas trimestrales · informe de beneficios.",
          2, "Toda inversión con caso de negocio y medición posterior; desviación presupuestal ≤ 10 %.",
          "Comité que se reúne una vez y no vuelve a hacerlo.",
          "Gerente General (preside)", "Gerencia y Consejo de Administración",
          "4 sesiones al año con acta y 100 % de inversiones aprobadas con caso de negocio."),
"PR-13": ("La disponibilidad de los servicios no se mide (Sección 6.1.5): las caídas se conocen cuando el socio o la agencia reclaman.",
          "Monitoreo de servidores, enlaces y aplicaciones críticas; alertas a la mesa de servicio.",
          "Monitoreo de seguridad (cubierto por PR-11).",
          "Plataforma de monitoreo · tablero de disponibilidad · reporte mensual de disponibilidad.",
          5, "Línea base de disponibilidad medida; detección de caídas antes que el usuario.",
          "Ruido de alertas que el equipo deja de atender.",
          "Jefe de TI", "Tecnologías de la Información y Agencias",
          "Disponibilidad medida de 100 % de servicios críticos y ≥ 99.5 % mensual."),
}

def s(x): return f"S/ {x:,.0f}".replace(",", " ")

os.makedirs("PF03_fichas", exist_ok=True)
for cod, (prob, inc, exc, ent, pm, ben, rie, resp, area, exito) in F.items():
    r = d.loc[cod]
    dep_de   = [b for a, b in DEP if a == cod]
    habilita = [a for a, b in DEP if b == cod]
    fus = f", fusiona {r.fusiona}" if isinstance(r.fusiona, str) and r.fusiona else ""
    md = f"""# {cod} · {r.nombre}

> Ficha estandarizada de proyecto · PETI COOPAC Frontera Sur · Sección 7.1.3
> Información confidencial. Cifras en soles, estimaciones de orden de magnitud con su margen.

| # | Campo | Contenido |
|---|---|---|
| 1 | Código | {cod} (candidato {r.candidato}{fus}) |
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
