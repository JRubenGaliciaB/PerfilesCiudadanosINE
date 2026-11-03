# GENERACIONES DEL VOTO
#Ciencia de datos para descubrir la participación electoral de las juventudes en México.

**[EXPLORA EL PROYECTO](generaciones_del_voto.html)** · **[ABRE EL MAPA](mapa_perfiles_municipales.html)** · **[CONSULTA LOS PERFILES](explorador_generaciones.html)** · **[EXPLORA EL CÓDIGO](experimentos/)**

**¿Qué oculta un promedio de participación electoral?**

Detrás de una cifra nacional existen generaciones y territorios con recorridos distintos. Una participación baja en una elección puede preceder a una recuperación; una tasa elevada puede formar parte de una trayectoria descendente; municipios alejados pueden compartir una evolución semejante.

**Generaciones del voto** explora esa diversidad mediante el seguimiento de cohortes inicialmente jóvenes durante las elecciones ordinarias de **2009, 2012, 2015, 2018, 2021 y 2024**.

El proyecto combina análisis estadístico, aprendizaje automático no supervisado y visualización interactiva para organizar **19,270 trayectorias completas** en **41 variantes por cohorte y sexo**, sintetizadas posteriormente en **cinco perfiles descriptivos**.

Desarrollado por el equipo **Gen Zivic-IA** para el Reto 1, *Perfiles ciudadanos de participación*, del concurso **“Hackea la participación: Datos que construyen democracia”**.

## Explora las visualizaciones

### Una historia interactiva del proyecto

Abre [`generaciones_del_voto.html`](generaciones_del_voto.html) para recorrer la pregunta de investigación, el seguimiento de generaciones y los resultados.

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

- Verifica sus huellas **SHA-256**.
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
| `experimento_01.py` | Agrupamiento de trayectorias por nivel de participación. |
| `experimento_02.py` | Comparación de agrupamientos por nivel y forma temporal. |
| `experimento_03.py` | Agrupamiento basado en grafos. |
| `experimento_04.py` | Modelos probabilísticos y comparación entre familias de métodos. |
| `experimento_05.py` | Análisis temporal descriptivo. |
| `experimento_06.py` | Exploración de representación profunda y DEC. |
| `experimento_07.py` | Construcción del catálogo y análisis del respaldo de pertenencia. |
| `experimento_08.py` | Comparación de familias entre cohortes. |
| `experimento_09.py` | Exploración de coincidencias territoriales. |
| `experimento_10.py` | Evaluación retrospectiva con información hasta 2021 y observación de 2024. |
| `definir_perfiles.py` | Síntesis de las variantes en cinco perfiles descriptivos. |
| `resultados_perfiles.py` | Comparaciones generacionales, territoriales y entre casos. |
| `cerrar_conclusiones.py` | Integración de resultados y conclusiones. |
| `revisar_casos.py` | Revisión de trayectorias, ejemplos, excepciones y asignaciones débiles. |

Los scripts se encuentran en [`generaciones/scripts/`](generaciones/scripts/).

## Reproducir el análisis

### 1. Preparar el entorno

El paquete indica **Python 3.11 o posterior**. Para reproducir los resultados se recomienda utilizar el entorno registrado en `validacion.json` y las versiones fijadas en `requirements.txt`.

Desde la carpeta `generaciones/`:

```bash
python -m venv .venv
```

Activa el entorno.

**Windows:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS o Linux:**

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

### 2. Preparar los archivos fuente

Coloca los seis ZIP originales en una carpeta independiente de la carpeta de resultados. Las carpetas **no deben estar anidadas entre sí**.

El ejecutor busca exactamente un archivo de Conteos Censales para cada año y comprueba que su huella coincide con la versión auditada.

### 3. Verificar entradas y dependencias

Este comando verifica los requisitos sin ajustar los modelos:

```bash
python ejecutar.py --input-dir "/ruta/originales" --output-dir "/ruta/resultados" --check
```

### 4. Ejecutar la cadena

```bash
python ejecutar.py --input-dir "/ruta/originales" --output-dir "/ruta/resultados" --resume
```

La salida final es:

```text
/ruta/resultados/explorador_generaciones.html
```

La cadena comienza en la etapa 02, que incorpora los modelos de nivel de la etapa 01 y los de forma de la etapa 02. El script `experimento_01.py` se conserva como antecedente autónomo.

### 5. Reanudar una ejecución

Repite el comando con `--resume`. Una etapa se reutiliza únicamente cuando coinciden las huellas del código, las entradas, el entorno y sus archivos de salida.

Una etapa interrumpida se ejecuta nuevamente; no se reanuda dentro del ajuste de un modelo. Cada etapa conserva un archivo `ejecucion.log`.

Para probar el control de reanudación:

```bash
python -m unittest test_ejecutar.py
```


## Límites de interpretación

- Los perfiles describen grupos agregados; no identifican conductas individuales.
- El análisis no separa causalmente los efectos de edad, periodo y generación.
- Los promedios de perfil dan igual peso a las trayectorias; no son tasas nacionales ponderadas por lista nominal.
- La coincidencia territorial o temporal no demuestra causas compartidas.
- La concordancia con una regla descriptiva no equivale a exactitud de clasificación.
- Una segmentación descriptiva útil no garantiza capacidad predictiva.


