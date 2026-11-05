# 07_portafolio/PF01_consolidacion.py
# Consolidación y depuración de candidatos a proyecto · COOPAC Frontera Sur
# Fuentes admisibles: Sección 3.5 (FODA), 4.1.5 (normativa), 4.3.5 (capacidades),
# 5.4.2 (brechas de arquitectura), 6.1.5 / 6.1.7 (línea base y servicios digitales).
import pandas as pd

# Objetivos de la Sección 6.2 del PETI
OBJETIVOS_62 = {
    "OD-01": "Ampliar la inclusión financiera con servicios digitales para los socios",
    "OD-02": "Decidir con información confiable de socios y cartera",
    "OD-03": "Integrar el sistema central con los canales y las áreas",
    "OD-04": "Asegurar la continuidad y disponibilidad de los servicios financieros",
    "OD-05": "Cumplir la normativa de prevención de lavado de activos y de datos personales",
    "OD-06": "Proteger la información de los socios y de la cooperativa",
}

CANDIDATOS = pd.DataFrame([
 # codigo, nombre, fuente, seccion_origen, objetivo, categoria
 ("C-01","Gobierno del dato maestro de socios","Brecha de arquitectura","Sección 5.4.2 PT-01","OD-02, OD-03","Transformar"),
 ("C-02","Capa de integración con el sistema central y los canales","Brecha de arquitectura","Sección 5.4.2 PT-02","OD-01, OD-03","Transformar"),
 ("C-03","Banca móvil y web para socios","Brecha de servicio digital","Sección 6.1.7 S-01","OD-01","Crecer"),
 ("C-04","Consulta de saldos y estado de crédito en autoservicio","Brecha de servicio digital","Sección 6.1.7 S-02","OD-01","Crecer"),
 ("C-05","Evaluación y scoring crediticio automatizado","Estrategia FODA","Sección 3.5 E-03","OD-02","Crecer"),
 ("C-06","Tablero de gestión de cartera y morosidad","Brecha de arquitectura","Sección 5.4.2 PT-04","OD-02","Crecer"),
 ("C-07","Mesa de servicio de TI","Brecha de capacidad","Sección 4.3.5 DSS02","OD-04","Operar"),
 ("C-08","Continuidad de infraestructura y respaldo inmutable","Brecha de capacidad","Sección 4.3.5 DSS04","OD-04","Operar"),
 ("C-09","Modernización del sistema central cooperativo","Estrategia FODA","Sección 3.5 E-04","OD-04","Operar"),
 ("C-10","Prevención de lavado de activos y monitoreo de operaciones","Obligación normativa","Sección 4.1.5","OD-05","Operar"),
 ("C-11","Programa de cumplimiento de datos personales","Obligación normativa","Sección 4.1.5","OD-05","Operar"),
 ("C-12","Registro de actividades de tratamiento","Obligación normativa","Sección 4.1.5","OD-05","Operar"),
 ("C-13","Seguridad de la información y ciberseguridad","Obligación normativa","Sección 4.1.5","OD-06","Operar"),
 ("C-14","Comité de gobierno de TI","Brecha de capacidad","Sección 4.3.5 EDM01","OD-02, OD-04","Operar"),
 ("C-15","Instrumentación de monitoreo y disponibilidad","Brecha de línea base","Sección 6.1.5","OD-04","Operar"),
 # Candidatos recibidos fuera de las cinco fuentes: el control de admisión debe retirarlos
 ("C-16","Renovación de laptops de gerencia","Pedido de área usuaria","Correo de Gerencia",None,"Operar"),
 ("C-17","Plataforma de criptoactivos para socios","Iniciativa del proveedor","Propuesta comercial no solicitada",None,"Transformar"),
], columns=["codigo","nombre","fuente","seccion_origen","objetivo","categoria"])

FUENTES_VALIDAS = {"Obligación normativa","Brecha de arquitectura","Brecha de capacidad",
                   "Estrategia FODA","Brecha de servicio digital","Brecha de línea base"}

# Depuración: candidato absorbido -> (candidato que lo absorbe, razón)
FUSIONES = {
    "C-04": ("C-03", "La consulta de saldos y del estado de crédito es un entregable de la banca "
                     "móvil y web: mismo usuario (socio), misma plataforma y misma integración con el sistema central."),
    "C-12": ("C-11", "El registro de actividades de tratamiento es el primer entregable del programa "
                     "de cumplimiento de la Ley 29733; separarlo duplicaría responsable y presupuesto."),
}

print("=== CONTROL DE ADMISIÓN ===")
sin_fuente = CANDIDATOS[~CANDIDATOS.fuente.isin(FUENTES_VALIDAS)]
print(f"Candidatos sin fuente admisible: {len(sin_fuente)} → se retiran: {list(sin_fuente.codigo)}")
for _, r in sin_fuente.iterrows():
    print(f"  {r.codigo} {r.nombre} · fuente «{r.fuente}» no es una de las cinco admisibles")
sin_obj = CANDIDATOS[CANDIDATOS.objetivo.isna() | (CANDIDATOS.objetivo.astype(str).str.strip()=="")]
print(f"Candidatos sin objetivo asociado: {len(sin_obj)} → se retiran: {list(sin_obj.codigo)}")

adm = CANDIDATOS[CANDIDATOS.fuente.isin(FUENTES_VALIDAS) & CANDIDATOS.objetivo.notna()].copy()
adm["fusiona"] = ""

print("\n=== DEPURACIÓN · FUSIÓN DE DUPLICADOS ===")
for absorbido, (destino, razon) in FUSIONES.items():
    a = adm[adm.codigo == absorbido].iloc[0]
    i = adm.index[adm.codigo == destino][0]
    # El proyecto resultante conserva el alcance, la sección de origen y los objetivos de ambos
    adm.at[i, "nombre"] = f"{adm.at[i,'nombre']} (incluye {a.nombre[0].lower() + a.nombre[1:]})"
    if a.seccion_origen not in adm.at[i, "seccion_origen"]:
        adm.at[i, "seccion_origen"] = f"{adm.at[i,'seccion_origen']}; {a.seccion_origen}"
    adm.at[i, "objetivo"] = ", ".join(sorted(set(adm.at[i,"objetivo"].split(", ")) | set(a.objetivo.split(", "))))
    adm.at[i, "fusiona"] = absorbido
    print(f"  {absorbido} → {destino}: {razon}")
adm = adm[~adm.codigo.isin(FUSIONES)].copy()

adm.insert(0, "candidato", adm.codigo)
adm["codigo"] = ["PR-%02d" % (i+1) for i in range(len(adm))]
adm.to_csv("PF01_portafolio_candidatos.csv", index=False, encoding="utf-8")

print(f"\nCandidatos recibidos: {len(CANDIDATOS)} · retirados: {len(sin_fuente)} · "
      f"fusionados: {len(FUSIONES)} · proyectos admitidos: {len(adm)}")
print("\n" + adm[["codigo","candidato","nombre","seccion_origen","objetivo","categoria"]].to_string(index=False))
print("\nPor fuente:\n", adm.fuente.value_counts().to_string())
print("\nPor categoría:\n", adm.categoria.value_counts().to_string())

print("\n=== COBERTURA DE OBJETIVOS (Sección 6.2) ===")
cob = adm.objetivo.str.split(", ").explode().value_counts()
for od, desc in OBJETIVOS_62.items():
    proys = ", ".join(adm[adm.objetivo.str.contains(od)].codigo)
    print(f"  {od} {desc:75s} {cob.get(od,0)} proyecto(s): {proys or '— SIN COBERTURA'}")
faltan = [od for od in OBJETIVOS_62 if od not in cob]
print("→ Todos los objetivos de la sección 6.2 tienen al menos un proyecto." if not faltan
      else f"⚠ Objetivos sin proyecto: {faltan}")
huerfanos = adm[~adm.objetivo.str.split(", ").apply(lambda l: all(o in OBJETIVOS_62 for o in l))]
print(f"→ Proyectos que citan un objetivo inexistente: {len(huerfanos)}")
