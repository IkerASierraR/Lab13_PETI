# Evidencia · Taller Semana 13 · Portafolio de proyectos

**Equipo (Ficha 4 · EMPRESA-04 · COOPAC Frontera Sur)**
- Jahuira Pilco, Dayan Elvis (2022075749)
- Mamani Cori, Cristhian Carlos (2023077282)
- Sierra Ruiz, Iker Alberto (2023077090)

Repositorio: <https://github.com/IkerASierraR/Lab13_PETI> · rama del taller: `taller/S13-coopac`, fusionada a `develop` por Pull Request · etiquetas: [`taller-13`](https://github.com/IkerASierraR/Lab13_PETI/tree/taller-13) y `v0.13`

## Lista de comprobación 3.2

| # | Resultado esperado | Evidencia |
|---|---|---|
| 1 | Candidatos consolidados desde las cinco fuentes admisibles | [`07_portafolio/PF01_portafolio_candidatos.csv`](../../07_portafolio/PF01_portafolio_candidatos.csv) |
| 2 | Control de admisión ejecutado: candidatos sin fuente o sin objetivo retirados (C-16, C-17) | [`salidas/PF01_salida.txt`](salidas/PF01_salida.txt) |
| 3 | Portafolio con 13 proyectos (mínimo 12), cada uno con su sección de origen | [`PF01_portafolio_candidatos.csv`](../../07_portafolio/PF01_portafolio_candidatos.csv) |
| 4 | Ficha estandarizada de 20 campos por proyecto | [`07_portafolio/PF03_fichas/`](../../07_portafolio/PF03_fichas/) |
| 5 | TCO a 5 años por proyecto, con su margen de incertidumbre | [`07_portafolio/PF02_tco.csv`](../../07_portafolio/PF02_tco.csv) |
| 6 | Factor TCO/inversión (4.94×) calculado e interpretado | [`salidas/PF02_salida.txt`](salidas/PF02_salida.txt) |
| 7 | Tres casos de negocio (PR-08, PR-03, PR-02) con tres alternativas, incluida «no hacer nada» | [`07_portafolio/PF04_alternativas.csv`](../../07_portafolio/PF04_alternativas.csv) |
| 8 | Costo de la inacción cuantificado en cada caso (S/ 950 000 · 550 000 · 425 000) | [`salidas/PF04_salida.txt`](salidas/PF04_salida.txt) |
| 9 | Balance operar/crecer/transformar contrastado con el presupuesto actual | [`salidas/PF05_salida.txt`](salidas/PF05_salida.txt) |
| 10 | Gráficos de balance y de TCO por proyecto | [`graficos/PF_balance.png`](../../graficos/PF_balance.png) |
| 11 | Mapa de dependencias con orden topológico y habilitadores | [`graficos/PF_dependencias.png`](../../graficos/PF_dependencias.png) · [`salidas/PF06_salida.txt`](salidas/PF06_salida.txt) |
| 12 | Cobertura: los 6 objetivos de la sección 6.2 tienen al menos un proyecto | [`salidas/PF01_salida.txt`](salidas/PF01_salida.txt) |
| 13 | Sección 7.1 redactada · etiqueta v0.13 | [`07_portafolio/7.1_portafolio_de_proyectos.md`](../../07_portafolio/7.1_portafolio_de_proyectos.md) |

## Paso F · Validación

Las tres comprobaciones las ejecuta [`PF07_validacion.py`](../../07_portafolio/PF07_validacion.py) y su resultado está en [`salidas/PF07_salida.txt`](salidas/PF07_salida.txt). Las tres pasan:

1. Cada uno de los 13 proyectos cita su objetivo, tanto en PF01 como en su ficha.
2. Los dos duplicados fusionados conservan su alcance. La consulta de saldos y de estado de crédito sigue en PR-03 y el registro de actividades de tratamiento sigue en PR-10.
3. El TCO de los 13 proyectos incluye costo operativo, y el costo a 5 años de la alternativa B de cada caso de negocio coincide con el TCO de la ficha.

Además, PF07 comprueba que los tres casos de negocio corresponden a los tres proyectos de mayor TCO.

Durante la validación se corrigieron estos defectos:

- La leyenda del mapa de dependencias tapaba el nodo PR-10; se movió fuera del área del grafo.
- La ficha y el mapa de dependencias podían divergir porque cada uno tenía su propia lista; ahora PF03 lee las dependencias directamente de PF06.
- Las alternativas B de los casos de negocio tenían las cifras escritas a mano; ahora PF04 las lee de PF02 para que no puedan contradecir al TCO.

## Problemas y mejoras

| Problema | Qué falta y por qué |
|---|---|
| **Los candidatos y sus secciones de origen** (3.5, 4.1.5, 4.3.5, 5.4.2, 6.1.5, 6.1.7) y los **objetivos OD-01 a OD-06** de la sección 6.2 están propuestos por el equipo a partir del perfil de una COOPAC. Los documentos de la carpeta del caso solo traen expedientes, presupuesto y pagos. | Deben alinearse con el PETI real del equipo (secciones de las semanas anteriores). Si los códigos o textos difieren, se ajustan en PF01 y se vuelve a ejecutar la cadena PF01 → PF07. |
| Supuestos cuantitativos que no vienen en los documentos del caso: ≈ 12 % de registros de socios duplicados o incompletos (PR-01); ≈ 96 000 operaciones al año en ventanilla (PR-03); 5 días hábiles para evaluar un crédito (PR-04); reportes de cartera con ≈ 10 días de retraso (PR-05); 2 días al año de interrupción del sistema central (PR-08); dos personas a medio tiempo en conciliación manual (PR-02). | Se confirman en la entrevista simulada con el docente y se reemplazan en PF03 y PF04 si cambian. |
| Las referencias normativas son generales (Ley 29733, Ley 29571 y «normas del supervisor» sobre riesgo operacional, seguridad de la información y prevención de lavado de activos) | No se citaron resoluciones concretas porque el nivel modular de la COOPAC determina cuáles le aplican. Hay que confirmarlas con Cumplimiento o Asesoría Legal antes de usar el documento. |
| Los costos unitarios del TCO son referencias de mercado, no cotizaciones | La guía prohíbe pedir cotizaciones formales sin autorización. Por eso cada cifra lleva su margen (±15 % a ±50 %). |
| El gasto real en «servicio informático» (S/ 3.71 millones) es 3 veces el presupuesto de TI (S/ 1.24 millones) | Hace falta conciliar con Administración qué parte es TI en sentido estricto. Mientras tanto, el costo operativo del TCO se trata como un piso. |
| El balance actual no separa crecer de transformar | El presupuesto tiene una sola partida, «Proyectos nuevos». Se contrasta Operar frente a Crecer + Transformar. |
| El caso de negocio parte del gasto operativo estimado (S/ 42.8 millones) | Se deduce del dato «el presupuesto de TI es el 2.9 % de los gastos operativos»; es una aproximación del costo de un día de operación y no una cifra contable. |

## Pregunta de transferencia

¿Qué riesgo correría una organización real si este portafolio se hiciera mal?

Si se aprueba con la inversión inicial (S/ 934 000) y no con el TCO (S/ 4.6 millones), la cooperativa asume S/ 3.7 millones de gasto recurrente sin aprobarlo, igual que en los expedientes cerrados, que se desviaron un +22.8 % sin que nadie midiera el beneficio. Y si se priorizara solo por retorno, quedarían fuera PR-01, PR-02 y PR-12, que casi no tienen retorno propio pero sostienen casi dos tercios del portafolio, de modo que los proyectos rentables tampoco podrían ejecutarse.
