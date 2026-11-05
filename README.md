# PETI · Distribuidora Andina del Sur S.A.C.

**SI-886 · Planeamiento Estratégico de TI** · Universidad Privada de Tacna
Laboratorio 13 · Construcción del portafolio de proyectos · Sección 7.1 del PETI

## Integrantes

| Integrante | Código |
|---|---|
| Jahuira Pilco, Dayan Elvis | 2022075749 |
| Mamani Cori, Cristhian Carlos | 2023077282 |
| Sierra Ruiz, Iker Alberto | 2023077090 |

> Caso trabajado: **EMPRESA-06 · Distribuidora Andina del Sur S.A.C.**, el caso de respaldo del curso. Es una organización ficticia. Información confidencial.

## Flujo de trabajo

Cada taller se desarrolla en su rama (`taller/SNN`) y se fusiona a `develop` mediante Pull Request. Este taller: rama `taller/S13`.

## Estructura

| Carpeta | Contenido |
|---|---|
| [`07_portafolio/`](07_portafolio/) | Programas PF01 a PF07, archivos CSV, fichas y la [Sección 7.1](07_portafolio/7.1_portafolio_de_proyectos.md) |
| [`07_portafolio/PF03_fichas/`](07_portafolio/PF03_fichas/) | Ficha estandarizada de 20 campos por proyecto (PR-01 a PR-13) |
| [`07_portafolio/insumos/`](07_portafolio/insumos/) | Documentos del caso: expedientes de inversión, presupuesto de TI y pagos |
| [`graficos/`](graficos/) | `PF_balance.png` y `PF_dependencias.png` |
| [`evidencias/S13/`](evidencias/S13/) | Lista de comprobación, validación y salida de cada programa |

## Cómo reproducir

Se necesita Python 3.11 o posterior con pandas, matplotlib y networkx.

```bash
cd 07_portafolio
python PF01_consolidacion.py   # consolida, depura y verifica la cobertura de objetivos
python PF02_tco.py             # TCO a 5 años con rango y factor TCO/inversión
python PF03_fichas.py          # genera las 13 fichas de 20 campos
python PF04_alternativas.py    # casos de negocio de los 3 proyectos de mayor TCO
python PF05_balance.py         # balance operar/crecer/transformar → ../graficos/PF_balance.png
python PF06_dependencias.py    # orden topológico y habilitadores → ../graficos/PF_dependencias.png
python PF07_validacion.py      # las tres comprobaciones del paso F
```

## Resumen

- **13 proyectos** admitidos de 17 candidatos: 2 retirados en el control de admisión y 2 fusionados.
- **TCO a 5 años: S/ 3.13 millones** (rango S/ 2.01 – 4.24 millones), **5.0 veces** la inversión inicial de S/ 624 000.
- **Casos de negocio:** PR-08 (ERP), PR-03 (canal B2B) y PR-02 (integración). El costo de la inacción suma S/ 1.73 millones en 5 años.
- **Balance:** el presupuesto actual dedica 92 % a operar. El portafolio propone 48 % operar, 28 % crecer y 24 % transformar.
- **Habilitadores:** PR-02 (integración), PR-01 (dato maestro) y PR-11 (comité de gobierno de TI).
