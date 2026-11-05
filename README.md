# PETI · COOPAC Frontera Sur

**SI-886 · Planeamiento Estratégico de TI** · Universidad Privada de Tacna
Laboratorio 13 · Construcción del portafolio de proyectos · Sección 7.1 del PETI

## Integrantes · Ficha 4

| Integrante | Código |
|---|---|
| Jahuira Pilco, Dayan Elvis | 2022075749 |
| Mamani Cori, Cristhian Carlos | 2023077282 |
| Sierra Ruiz, Iker Alberto | 2023077090 |

> Organización asignada: **EMPRESA-04 · COOPAC Frontera Sur**, organización ficticia elaborada para el curso. Información confidencial.

## Flujo de trabajo

Cada taller se desarrolla en su rama (`taller/SNN`) y se fusiona a `develop` mediante Pull Request. Este taller: rama `taller/S13-coopac`.

## Estructura

| Carpeta | Contenido |
|---|---|
| [`07_portafolio/`](07_portafolio/) | Programas PF01 a PF07, archivos CSV, fichas y la [Sección 7.1](07_portafolio/7.1_portafolio_de_proyectos.md) |
| [`07_portafolio/PF03_fichas/`](07_portafolio/PF03_fichas/) | Ficha estandarizada de 20 campos por proyecto (PR-01 a PR-13) |
| [`07_portafolio/insumos/`](07_portafolio/insumos/) | Documentos del caso: expedientes de inversión, presupuesto de TI y pagos |
| [`graficos/`](graficos/) | `PF_balance.png` y `PF_dependencias.png` |
| [`evidencias/S13/`](evidencias/S13/) | Lista de comprobación, validación, problemas y salida de cada programa |

## Cómo reproducir

Se necesita Python 3.11 o posterior con pandas, matplotlib y networkx.

```bash
cd 07_portafolio
python PF01_consolidacion.py   # consolida, depura y verifica la cobertura de objetivos
python PF02_tco.py             # TCO a 5 años con rango y factor TCO/inversión
python PF06_dependencias.py    # orden topológico y habilitadores → ../graficos/PF_dependencias.png
python PF03_fichas.py          # genera las 13 fichas de 20 campos (lee las dependencias de PF06)
python PF04_alternativas.py    # casos de negocio de los 3 proyectos de mayor TCO
python PF05_balance.py         # balance operar/crecer/transformar → ../graficos/PF_balance.png
python PF07_validacion.py      # las tres comprobaciones del paso F
```

## Resumen

- **13 proyectos** admitidos de 17 candidatos: 2 retirados en el control de admisión y 2 fusionados.
- **TCO a 5 años: S/ 4.61 millones** (rango S/ 2.95 – 6.28 millones), **4.9 veces** la inversión inicial de S/ 934 000.
- **Casos de negocio:** PR-08 (sistema central), PR-03 (banca móvil y web) y PR-02 (integración). El costo de la inacción suma S/ 1.93 millones en 5 años.
- **Balance:** el presupuesto actual dedica 92 % a operar. El portafolio propone 56 % operar, 24 % crecer y 20 % transformar.
- **Habilitadores:** PR-01 (dato maestro de socios), PR-02 (integración) y PR-12 (comité de gobierno de TI).
