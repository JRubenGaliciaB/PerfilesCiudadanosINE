# GENERACIONES DEL VOTO
#Ciencia de datos para descubrir la participación electoral de las juventudes en México.

**[EXPLORA EL PROYECTO](explorador_generaciones_rev1.html)** · **[ABRE EL MAPA](mapa_perfiles_municipales.html)** · **[CONSULTA LOS PERFILES](explorador_generaciones_rev1.html)** · **[EXPLORA EL CÓDIGO](experimentos/)**

**¿Qué oculta un promedio de participación electoral?**

Detrás de una cifra nacional existen generaciones y territorios con recorridos distintos. Una participación baja en una elección puede preceder a una recuperación; una tasa elevada puede formar parte de una trayectoria descendente; municipios alejados pueden compartir una evolución semejante.

**Generaciones del voto** explora esa diversidad mediante el seguimiento de cohortes inicialmente jóvenes durante las elecciones ordinarias de **2009, 2012, 2015, 2018, 2021 y 2024**.

El proyecto combina análisis estadístico, aprendizaje automático no supervisado y visualización interactiva para organizar **19,270 trayectorias completas** en **41 variantes por cohorte y sexo**, sintetizadas posteriormente en **cinco perfiles descriptivos**.

Desarrollado por el equipo **Gen Zivic-IA** para el Reto 1, *Perfiles ciudadanos de participación*, del concurso **“Hackea la participación: Datos que construyen democracia”**.

## Explora las visualizaciones

### Una historia interactiva del proyecto

Abre [`explorador_generaciones_rev1.html`](explorador_generaciones_rev1.html) para recorrer la pregunta de investigación, el seguimiento de generaciones y los resultados.

- **Desplázate** para descubrir las distintas secciones.
- **Mueve el año** para observar cómo cambia la edad de una cohorte.
- **Selecciona un perfil** para consultar su descripción, composición y trayectoria.
- **Alterna entre promedio, ejemplo y excepción** para explorar la diversidad interna.
- **Pasa el cursor o toca los elementos interactivos** para consultar información adicional.

### Mapa municipal

Abre [`mapa_perfiles_municipales.html`](mapa_perfiles_municipales.html).

Cada municipio se colorea según el perfil correspondiente a la **cohorte y el sexo seleccionados**. Un mismo municipio puede presentar perfiles diferentes entre grupos.

Selecciona una entidad, busca un municipio y consulta su trayectoria electoral. Los controles permiten ampliar el mapa y descargar datos y correspondencias municipales.

**Cómo interpretarlo:** el color representa una categoría descriptiva, no una tasa de participación. La superficie coloreada tampoco representa el número de personas. Los municipios sin correspondencia aceptada o sin trayectoria disponible se muestran en gris.

### Explorador de resultados y experimentos

Abre [`explorador_generaciones.html`](explorador_generaciones.html) para consultar:

- El catálogo de los cinco perfiles.
- Las diferencias entre cohortes, sexos y territorios.
- Ejemplos representativos, excepciones y asignaciones débiles.
- La comparación de métodos y los experimentos de respaldo.
- Tablas y exportaciones para examinar los resultados.

Los HTML pueden descargarse y abrirse directamente en un navegador. **GitHub muestra su código al abrirlos desde el repositorio**; para navegarlos en línea es necesario habilitar un servicio de publicación, como GitHub Pages.

## ¿Por qué estudiar generaciones?

Las personas jóvenes de 2009 no son el mismo grupo de edad que las personas jóvenes de 2024. Analizar únicamente “el voto joven” en cada elección deja fuera lo que sucede con una generación conforme avanza en su trayectoria.

El proyecto distingue dos preguntas:

1. **¿Cómo participan quienes son jóvenes en cada elección?**
2. **¿Cómo evoluciona la participación de quienes eran jóvenes en un momento determinado?**

La segunda pregunta constituye el eje central del análisis. Se siguen cuatro cohortes definidas por su edad en 2009:

| Edad en 2009 | Edad correspondiente en 2024 |
|---|---|
| 18–20 años | 33–35 años |
| 21–23 años | 36–38 años |
| 24–26 años | 39–41 años |
| 27–29 años | 42–44 años |

Utilizamos **juventudes**, en plural, para reconocer que compartir un rango de edad no implica tener las mismas condiciones sociales, experiencias políticas o formas de participación.

> El seguimiento es de **grupos agregados**, no de personas identificadas individualmente. No permite comprobar que los mismos individuos votaron o dejaron de votar entre elecciones.

## Los cinco perfiles

Los nombres resumen la forma general de las trayectorias. **No describen personalidades ni permiten inferir emociones o motivaciones individuales.**

| Perfil | Patrón observado | Trayectorias | Porcentaje del catálogo |
|---|---|---:|---:|
| **P1. Participación que repunta** | Descenso en 2015 y recuperación posterior en su promedio. | 3,044 | 15.80% |
| **P2. Participación con altibajos** | Alternancia de aumentos y descensos entre elecciones. | 6,416 | 33.30% |
| **P3. Cada vez más participación** | Tendencia general ascendente, con oscilaciones. | 7,470 | 38.76% |
| **P4. Participación que pierde fuerza** | Tendencia general descendente desde niveles iniciales relativamente elevados. | 1,871 | 9.71% |
| **P5. Un salto y después pocos cambios** | Aumento en 2012 y variaciones posteriores más acotadas en su promedio. | 469 | 2.43% |

Los cinco perfiles son una **consolidación interpretativa de 41 variantes**; no resultan de imponer cinco conglomerados desde el inicio.

Además, **7,057 trayectorias —36.62% del catálogo—** integran un núcleo de mayor respaldo. Esta medida expresa acuerdo entre métodos, no una probabilidad de que una etiqueta sea verdadera.

## Algunos hallazgos

### La forma temporal y el nivel de participación son distintos

Dos grupos pueden compartir aumentos y descensos sin registrar tasas equivalentes.

Un ejemplo son **Tijuana, Baja California, y Coatepec, Veracruz**, para hombres de 27–29 años en 2009. Ambas trayectorias pertenecen al perfil cíclico:

- Distancia RMS entre tasas originales: **12.74 puntos porcentuales**.
- Distancia RMS después de descontar la media de cada trayectoria: **0.47 puntos porcentuales**.

El ejemplo muestra semejanza temporal, pero no demuestra causas compartidas.

### Las diferencias generacionales también varían por sexo

En una base comparable de **2,316 municipios**, el perfil ascendente representa el **81.43% de las trayectorias masculinas** y el **45.29% de las femeninas** de la cohorte de 27–29 años en 2009.

Estos porcentajes describen la distribución de perfiles dentro de cada grupo; **no son tasas de participación electoral**.

### El promedio no representa a todos los integrantes

La revisión de casos identifica ejemplos claros, excepciones dentro del núcleo y asignaciones de menor respaldo. Por eso, las visualizaciones permiten contrastar la curva promedio con trayectorias concretas.

## Datos

La fuente principal son los **Conteos Censales de Participación Ciudadana (CCPC)** del Instituto Nacional Electoral.

- **Periodo del catálogo principal:** elecciones ordinarias de 2009–2024.
- **Unidad de análisis:** municipio × cohorte × sexo.
- **Trayectorias completas:** 19,270.
- **Elección judicial de 2025:** extensión independiente; no forma parte de las seis observaciones utilizadas para construir los cinco perfiles.

Consulta la plataforma y los materiales institucionales en el [micrositio del concurso](https://www.ine.mx/hackathon-2026/).

### Preservación de los originales

Los archivos fuente se conservan sin modificación. El procedimiento:

- Verifica **SHA-256**.
- Registra problemas de cobertura y observaciones no disponibles.
- No imputa datos faltantes.
- Mantiene separados los originales y las salidas del análisis.

### Cartografía

El mapa utiliza geometrías del **Marco Geoestadístico de INEGI de diciembre de 2025**, simplificadas para visualización.

La correspondencia con el catálogo electoral es exploratoria: utiliza clave y nombre o, cuando las claves difieren, entidad y nombre normalizado exacto y único.

La versión disponible representa **19,023 de las 19,270 trayectorias**. Los casos sin correspondencia aceptada permanecen sin asignación.

**Una coincidencia de nombre o clave no demuestra continuidad territorial durante todo el periodo.** Los polígonos sirven como referencia espacial, no como validación de límites históricos.

## Método

El estudio tiene un diseño **cuantitativo, observacional, retrospectivo y longitudinal de grupos agregados**.

La estrategia distingue:

- **Nivel:** magnitud de las tasas de participación.
- **Forma temporal:** secuencia de aumentos y descensos, descontando el promedio de cada trayectoria cuando corresponde.

Se comparan métodos basados en centroides, agrupamiento jerárquico, grafos, modelos probabilísticos y representación profunda. Posteriormente se examinan sus coincidencias, diferencias y estabilidad.

### Experimentos y etapas de síntesis

| Archivo | Propósito principal |
|---|---|

| `experimento_10.py` | Evaluación retrospectiva con información hasta 2021 y observación de 2024. |
| `definir_perfiles.py` | Síntesis de las variantes en cinco perfiles descriptivos. |
| `resultados_perfiles.py` | Comparaciones generacionales, territoriales y entre casos. |
| `cerrar_conclusiones.py` | Integración de resultados y conclusiones. |
| `revisar_casos.py` | Revisión de trayectorias, ejemplos, excepciones y asignaciones débiles. |

Los scripts se encuentran en [`experimentos`](experimentos).


## Límites de interpretación

- Los perfiles describen grupos agregados; no identifican conductas individuales.
- El análisis no separa causalmente los efectos de edad, periodo y generación.
- Los promedios de perfil dan igual peso a las trayectorias; no son tasas nacionales ponderadas por lista nominal.
- La coincidencia territorial o temporal no demuestra causas compartidas.
- Una segmentación descriptiva útil no garantiza capacidad predictiva.


