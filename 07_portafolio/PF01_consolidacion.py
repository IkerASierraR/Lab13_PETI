# 07_portafolio/PF01_consolidacion.py
# Consolidación y depuración de candidatos a proyecto · Distribuidora Andina del Sur S.A.C.
# Fuentes admisibles: Sección 3.5 (FODA), 4.1.5 (normativa), 4.3.5 (capacidades),
# 5.4.2 (brechas de arquitectura), 6.1.5 / 6.1.7 (línea base y servicios digitales).
import pandas as pd

# Objetivos declarados en la Sección 6.2 del PETI
OBJETIVOS_62 = {
    "OD-01": "Digitalizar los servicios a clientes y trabajadores",
    "OD-02": "Decidir con datos confiables y oportunos",
    "OD-03": "Integrar la cadena pedido-almacén-despacho",
    "OD-04": "Asegurar la continuidad y disponibilidad de los servicios de TI",
    "OD-05": "Cumplir la Ley 29733 de protección de datos personales",
    "OD-06": "Profesionalizar la gestión de TI y su conocimiento",
}

CANDIDATOS = pd.DataFrame([
 # codigo, nombre, fuente, seccion_origen, objetivo, categoria
 ("C-01","Gobierno del dato maestro","Brecha de arquitectura","Sección 5.4.2 PT-01","OD-02, OD-03","Transformar"),
 ("C-02","Registro de actividades de tratamiento","Obligación normativa","Sección 4.1.5","OD-05","Operar"),
 ("C-03","Capa de integración de servicios","Brecha de arquitectura","Sección 5.4.2 PT-02","OD-01, OD-03","Transformar"),
 ("C-04","Rediseño y adopción del canal digital B2B","Brecha de servicio digital","Sección 6.1.7 S-01","OD-01","Crecer"),
 ("C-05","Consulta de estado de pedido en autoservicio","Brecha de servicio digital","Sección 6.1.7 S-02","OD-01","Crecer"),
 ("C-06","Planificación de rutas y trazabilidad de despacho","Estrategia FODA","Sección 3.5 E-02","OD-03","Crecer"),
 ("C-07","Tablero de gestión comercial","Brecha de arquitectura","Sección 5.4.2 PT-05","OD-02","Crecer"),
 ("C-08","Mesa de servicio de TI","Brecha de capacidad","Sección 4.3.5 DSS02","OD-04","Operar"),
 ("C-09","Continuidad de infraestructura y respaldo inmutable","Brecha de capacidad","Sección 4.3.5 DSS04","OD-04","Operar"),
 ("C-10","Renovación de la plataforma del ERP","Estrategia FODA","Sección 3.5 E-04","OD-04","Operar"),
 ("C-11","Programa de cumplimiento de datos personales","Obligación normativa","Sección 4.1.5","OD-05","Operar"),
 ("C-12","Gestión del conocimiento y de la configuración","Estrategia FODA","Sección 3.5 E-07","OD-06","Operar"),
 ("C-13","Comité de gobierno de TI","Brecha de capacidad","Sección 4.3.5 EDM01","OD-02, OD-04","Operar"),
 ("C-14","Instrumentación de monitoreo y disponibilidad","Brecha de línea base","Sección 6.1.5","OD-04","Operar"),
 ("C-15","Autoservicio de trabajadores (boletas y vacaciones)","Brecha de servicio digital","Sección 6.1.7 S-06, S-07","OD-01","Crecer"),
 # Candidatos recibidos fuera de las cinco fuentes: el control de admisión debe retirarlos
 ("C-16","Renovación de laptops de gerencia","Pedido de área usuaria","Correo de Gerencia Comercial",None,"Operar"),
 ("C-17","Asistente conversacional con IA generativa","Iniciativa del proveedor","Propuesta comercial no solicitada",None,"Transformar"),
], columns=["codigo","nombre","fuente","seccion_origen","objetivo","categoria"])

FUENTES_VALIDAS = {"Obligación normativa","Brecha de arquitectura","Brecha de capacidad",
                   "Estrategia FODA","Brecha de servicio digital","Brecha de línea base"}

# Depuración: candidato absorbido -> (candidato que lo absorbe, razón)
FUSIONES = {
    "C-05": ("C-04", "La consulta de estado de pedido es un entregable del canal B2B: mismo usuario "
                     "(cliente mayorista), misma plataforma y misma integración con el ERP."),
    "C-02": ("C-11", "El registro de actividades de tratamiento es el primer entregable del programa "
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

print("\n=== DEPURACIÓN · FUSIÓN DE DUPLICADOS ===")
for absorbido, (destino, razon) in FUSIONES.items():
    a = adm[adm.codigo == absorbido].iloc[0]
    i = adm.index[adm.codigo == destino][0]
    # El proyecto resultante conserva el alcance y las fuentes de ambos
    adm.at[i, "nombre"] = f"{adm.at[i,'nombre']} (incluye {a.nombre.lower()})"
    if a.seccion_origen not in adm.at[i, "seccion_origen"]:
        adm.at[i, "seccion_origen"] = f"{adm.at[i,'seccion_origen']}; {a.seccion_origen}"
    objs = sorted(set(adm.at[i,"objetivo"].split(", ")) | set(a.objetivo.split(", ")))
    adm.at[i, "objetivo"] = ", ".join(objs)
    adm.at[i, "fusiona"] = absorbido
    print(f"  {absorbido} → {destino}: {razon}")
adm = adm[~adm.codigo.isin(FUSIONES)].copy()

adm.insert(0, "candidato", adm.codigo)
adm["codigo"] = ["PR-%02d" % (i+1) for i in range(len(adm))]
adm["fusiona"] = adm["fusiona"].fillna("")
adm.to_csv("PF01_portafolio_candidatos.csv", index=False, encoding="utf-8")

print(f"\nCandidatos recibidos: {len(CANDIDATOS)} · retirados: {len(sin_fuente)} · "
      f"fusionados: {len(FUSIONES)} · proyectos admitidos: {len(adm)}")
print("\n" + adm[["codigo","candidato","nombre","seccion_origen","objetivo","categoria"]].to_string(index=False))
print("\nPor fuente:\n", adm.fuente.value_counts().to_string())
print("\nPor categoría:\n", adm.categoria.value_counts().to_string())

print("\n=== COBERTURA DE OBJETIVOS (Sección 6.2) ===")
obj = adm.objetivo.str.split(", ").explode()
cob = obj.value_counts()
for od, desc in OBJETIVOS_62.items():
    proys = ", ".join(adm[adm.objetivo.str.contains(od)].codigo)
    print(f"  {od} {desc:62s} {cob.get(od,0)} proyecto(s): {proys or '— SIN COBERTURA'}")
faltan = [od for od in OBJETIVOS_62 if od not in cob]
print("→ Todos los objetivos de la sección 6.2 tienen al menos un proyecto." if not faltan
      else f"⚠ Objetivos sin proyecto: {faltan}")
huerfanos = adm[~adm.objetivo.str.split(", ").apply(lambda l: all(o in OBJETIVOS_62 for o in l))]
print(f"→ Proyectos que citan un objetivo inexistente: {len(huerfanos)}")
