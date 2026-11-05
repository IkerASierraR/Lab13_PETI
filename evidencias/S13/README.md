# Evidencia · Taller Semana 13 · Portafolio de proyectos

Equipo: Jahuira Pilco, Dayan Elvis (2022075749) · Mamani Cori, Cristhian Carlos (2023077282) · Sierra Ruiz, Iker Alberto (2023077090)

Repositorio: <https://github.com/IkerASierraR/Lab13_PETI> · rama del taller: `taller/S13`, fusionada a `develop` por Pull Request · etiqueta del taller: [`taller-13`](https://github.com/IkerASierraR/Lab13_PETI/tree/taller-13) · versión del PETI: `v0.13`

Base de las rutas que siguen: `https://github.com/IkerASierraR/Lab13_PETI/blob/taller-13/`

## Lista de comprobación 3.2

| # | Resultado esperado | Evidencia |
|---|---|---|
| 1 | Candidatos consolidados desde las cinco fuentes admisibles | [`07_portafolio/PF01_portafolio_candidatos.csv`](../../07_portafolio/PF01_portafolio_candidatos.csv) |
| 2 | Control de admisión ejecutado: candidatos sin fuente o sin objetivo retirados (C-16, C-17) | [`salidas/PF01_salida.txt`](salidas/PF01_salida.txt) |
| 3 | Portafolio con 13 proyectos (mínimo 12), cada uno con su sección de origen | [`PF01_portafolio_candidatos.csv`](../../07_portafolio/PF01_portafolio_candidatos.csv) |
| 4 | Ficha estandarizada de 20 campos por proyecto | [`07_portafolio/PF03_fichas/`](../../07_portafolio/PF03_fichas/) |
| 5 | TCO a 5 años por proyecto, con su margen de incertidumbre | [`07_portafolio/PF02_tco.csv`](../../07_portafolio/PF02_tco.csv) |
| 6 | Factor TCO/inversión (5.01×) calculado e interpretado | [`salidas/PF02_salida.txt`](salidas/PF02_salida.txt) |
| 7 | Tres casos de negocio (PR-08, PR-03, PR-02) con tres alternativas, incluida «no hacer nada» | [`07_portafolio/PF04_alternativas.csv`](../../07_portafolio/PF04_alternativas.csv) |
| 8 | Costo de la inacción cuantificado en cada caso (S/ 900 000 · 475 000 · 350 000) | [`salidas/PF04_salida.txt`](salidas/PF04_salida.txt) |
| 9 | Balance operar/crecer/transformar contrastado con el presupuesto actual | [`salidas/PF05_salida.txt`](salidas/PF05_salida.txt) |
| 10 | Gráficos de balance y de TCO por proyecto | [`graficos/PF_balance.png`](../../graficos/PF_balance.png) |
| 11 | Mapa de dependencias con orden topológico y habilitadores | [`graficos/PF_dependencias.png`](../../graficos/PF_dependencias.png) · [`salidas/PF06_salida.txt`](salidas/PF06_salida.txt) |
| 12 | Cobertura: los 6 objetivos de la sección 6.2 tienen al menos un proyecto | [`salidas/PF01_salida.txt`](salidas/PF01_salida.txt) |
| 13 | Sección 7.1 redactada · etiqueta v0.13 | [`07_portafolio/7.1_portafolio_de_proyectos.md`](../../07_portafolio/7.1_portafolio_de_proyectos.md) |

## Paso F · Validación

Las tres comprobaciones las ejecuta [`PF07_validacion.py`](../../07_portafolio/PF07_validacion.py) y su resultado está en [`salidas/PF07_salida.txt`](salidas/PF07_salida.txt). Las tres pasan:

1. Cada uno de los 13 proyectos cita su objetivo, tanto en PF01 como en su ficha.
2. Los dos duplicados fusionados conservan su alcance. La consulta de estado de pedido sigue en PR-03 y el registro de actividades de tratamiento sigue en PR-09.
3. El TCO de los 13 proyectos incluye costo operativo, y el costo a 5 años de la alternativa B de cada caso de negocio coincide con el TCO de la ficha.

Durante la validación se detectaron y corrigieron tres errores:

- La sección de origen de PR-09 aparecía duplicada tras la fusión.
- El objetivo OD-01 se describía solo como venta B2B, aunque PR-13 (autoservicio de trabajadores) también lo cita. Se redefinió como «Digitalizar los servicios a clientes y trabajadores».
- La desviación total de los expedientes estaba mal calculada; se corrigió a +19.9 %.

## Problemas y mejoras

| Problema | Qué falta y por qué |
|---|---|
| Algunas cifras del diagnóstico no vienen en los documentos del caso: 18 % de clientes duplicados, 82 % de entregas a tiempo, 1 800 clientes mayoristas y ≈ 3 000 trámites de RR. HH. | Son supuestos del equipo, consistentes con el caso. Deben confirmarse en la entrevista simulada con el docente y reemplazarse en PF03 si cambian. |
| Los costos unitarios del TCO son referencias de mercado, no cotizaciones | La guía prohíbe pedir cotizaciones formales sin autorización. Por eso cada cifra lleva su margen (±15 % a ±50 %). |
| El gasto real en «servicio informático» (S/ 2.24 millones) es 3 veces el presupuesto de TI | Hace falta conciliar con Administración qué parte es TI en sentido estricto. Mientras tanto, el costo operativo del TCO se trata como un piso. |
| El balance actual no separa crecer de transformar | El presupuesto tiene una sola partida, «Proyectos nuevos». Se contrasta Operar frente a Crecer + Transformar. |

## Pregunta de transferencia

¿Qué riesgo correría una organización real si este portafolio se hiciera mal?

Si se aprueba con la inversión inicial (S/ 624 000) y no con el TCO (S/ 3.1 millones), la organización asume S/ 2.5 millones de gasto recurrente sin aprobarlo, igual que en los expedientes de 2025, que se desviaron un +19.9 % sin que nadie midiera el beneficio. Y si se priorizara solo por retorno, quedarían fuera PR-02 y PR-11, que no tienen retorno propio pero sostienen más de la mitad del portafolio, de modo que los proyectos rentables tampoco podrían ejecutarse.
