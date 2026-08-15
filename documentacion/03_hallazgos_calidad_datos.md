# Hallazgos de Calidad de Datos
## Prototipo 2 – Aguas Superficiales de México

**Objetivo:** registrar hallazgos que puedan afectar el entrenamiento del modelo, la API o la experiencia del usuario.

La lógica de documentación será:

**Hallazgo → Evidencia → Riesgo → Validación necesaria → Decisión**

---

## Hallazgo 1 – NaN no significa automáticamente dato faltante

### Evidencia
La disponibilidad de los indicadores cambia fuertemente según el tipo de cuerpo de agua.

Ejemplos observados:

- DBO en Costero–Océano/Mar: 0.0%
- DQO en Costero–Océano/Mar: 0.0%
- Enterococos en Lótico–Río: 0.0%
- OD general en Léntico–Presa: 0.0%

Estos patrones coinciden con diferencias metodológicas entre cuerpos lóticos, lénticos y costeros.

### Riesgo
Imputar automáticamente todos los NaN podría generar valores artificiales en variables que metodológicamente no aplican.

### Validación necesaria
Determinar cuáles NaN corresponden a:

- No aplica.
- Faltante real.
- Caso especial pendiente de revisión.

### Decisión
**Pendiente de validación con Ciencia de Datos.**

---

## Hallazgo 2 – Existen indicadores aplicables con ausencia parcial

### Evidencia

Entre los casos principales analizados:

- DBO en Lótico–Río: 70.0% disponible.
- DQO en Léntico–Presa: 85.7% disponible.
- Coliformes fecales en Lótico–Río: 50.8% disponible.
- E. coli en Léntico–Presa: 17.9% disponible.

### Riesgo
Estos casos no pueden clasificarse simplemente como “no aplica”.

Existe la posibilidad de faltantes reales que requieren una estrategia específica de tratamiento.

### Validación necesaria
Identificar la razón de ausencia y determinar si corresponde aplicar imputación.

### Decisión
**No imputar hasta conocer la causa del faltante.**

---

## Hallazgo 3 – La mediana de CONAGUA no equivale a imputación por mediana

### Evidencia

La metodología de CONAGUA utiliza:

- Mediana para DBO, DQO, SST y OD%.
- Media geométrica para CF, E. coli y Enterococos.
- Máximo para determinadas mediciones de toxicidad.

Estos estadísticos forman parte del cálculo de los indicadores.

### Riesgo
Interpretar la utilización de la mediana por CONAGUA como justificación automática para:

`SimpleImputer(strategy="median")`

podría confundir dos procesos distintos.

### Validación necesaria
Documentar por separado:

1. Cómo CONAGUA calcula cada indicador.
2. Cómo Ciencia de Datos trata los valores realmente faltantes.

### Decisión
**Mantener ambos procesos conceptualmente separados.**

---

## Hallazgo 4 – Posible fuga de información

### Evidencia

El dataset contiene:

- Mediciones originales.
- Variables `CALIDAD_*`.
- `CONTAMINANTES`.
- `SEMAFORO`.

Las variables `CALIDAD_*` ya contienen una interpretación de las mediciones originales y `CONTAMINANTES` incorpora información vinculada al resultado del semáforo.

### Riesgo
Utilizar estas variables como predictoras podría provocar data leakage y producir métricas artificialmente altas.

### Validación necesaria
Confirmar las variables X finales utilizadas por el equipo científico.

### Decisión
Para el modelo piloto, considerar principalmente mediciones originales y excluir variables derivadas hasta su validación.

---

## Hallazgo 5 – Tipo y subtipo requieren normalización

### Evidencia

Se encontraron categorías como:

- OCÉANO-MAR
- OCEANO-MAR
- Variantes con posibles espacios
- LÓTICO (HUMEDAL)
- LÉNTICO (HUMEDAL)
- COSTERO (HUMEDAL)
- LÓTICO - COSTERO
- Estudios especiales

### Riesgo
El modelo podría interpretar categorías equivalentes como diferentes o mezclar categorías metodológicamente distintas.

### Validación necesaria
Determinar cuáles diferencias son únicamente de escritura y cuáles representan categorías reales.

### Decisión
**No normalizar automáticamente sin criterio metodológico.**

---

## Hallazgo 6 – Profundidad de medición tiene significado

### Evidencia

Existen variables diferenciadas para:

- OD general.
- OD superficie.
- OD medio.
- OD fondo.

También existen diferentes mediciones de toxicidad según profundidad y ensayo.

### Riesgo
Combinar estas columnas como si representaran la misma medición podría eliminar información metodológica relevante.

### Validación necesaria
Confirmar cómo fueron utilizadas en el modelo científico.

### Decisión
Mantenerlas diferenciadas hasta disponer de criterio técnico validado.

---

## Hallazgo 7 – Baja disponibilidad no equivale a baja importancia

### Evidencia

Las variables de toxicidad presentan disponibilidades muy bajas en algunos grupos.

Ejemplos:

- TOX Daphnia 48 h en Lótico–Río: 2.7%.
- TOX Vibrio fischeri 15 min en Lótico–Río: 14.1%.
- TOX V. fischeri superficie en Léntico–Presa: 15.5%.

Sin embargo, toxicidad forma parte de la metodología del semáforo.

### Riesgo
Eliminar variables únicamente por porcentaje elevado de NaN podría excluir indicadores críticos.

### Validación necesaria
Revisar su función metodológica antes de cualquier eliminación.

### Decisión
**No utilizar un umbral automático de NaN como único criterio de eliminación.**

---

# Implicaciones para el Prototipo 2

Los hallazgos anteriores afectan directamente tres componentes:

## EXPLORAR

Variables geográficas y contextuales permitirán:

- mapas;
- filtros por Estado;
- Municipio;
- Cuenca;
- Tipo;
- Subtipo;
- Semáforo observado.

## COMPRENDER

Las variables de calidad, contaminantes y clasificación permitirán explicar:

- por qué un sitio presenta determinado semáforo;
- qué indicadores muestran mayor deterioro;
- diferencias por territorio y tipo de cuerpo de agua.

## EVALUAR

La interfaz deberá:

1. solicitar Tipo/Subtipo;
2. identificar indicadores aplicables;
3. mostrar únicamente los campos necesarios;
4. validar la entrada;
5. enviar un JSON coherente a la API;
6. reproducir exactamente el preprocesamiento utilizado en entrenamiento;
7. presentar la predicción en lenguaje comprensible.

## Hallazgo 8 – "Indicador aplicable" no implica "dato obligatorio en todos los registros"

### Evidencia

Al restringir el análisis únicamente a indicadores que corresponden
metodológicamente a cada tipo de cuerpo de agua, persisten porcentajes
importantes de ausencia.

Ejemplos:

- Lótico – DBO: 32.6% ausente.
- Lótico – Coliformes fecales: 49.2% ausente.
- Lótico – E. coli: 70.6% ausente.
- Léntico – DBO: 39.3% ausente.
- Léntico – OD superficie: 71.4% ausente.
- Costero – SST: 87.5% ausente.
- Costero – Enterococos: 79.2% ausente.

### Interpretación

La aplicabilidad metodológica define qué indicadores pueden formar
parte de la evaluación de un tipo de cuerpo de agua, pero estos
resultados no demuestran por sí solos que todos los indicadores
deban estar disponibles en todos los sitios.

Por tanto, todavía no es posible clasificar toda ausencia como
faltante real.

### Riesgo

Imputar todos estos valores podría introducir mediciones artificiales.

Eliminar registros incompletos también podría reducir fuertemente
la muestra y alterar su representatividad.

### Validación necesaria

Determinar si la disponibilidad depende adicionalmente de:

- subtipo;
- sitio;
- año;
- esquema de monitoreo;
- número de mediciones;
- profundidad;
- ensayo realizado;
- otras condiciones metodológicas.

### Decisión

No realizar todavía imputación ni eliminación automática.

Investigar primero la estructura de la ausencia.

## Hallazgo 9 – La variable objetivo SEMAFORO presenta ausencia y desbalance

### Evidencia

El dataset contiene 1,043 registros.

Distribución general:

- ROJO: 507 registros.
- VERDE: 171 registros.
- AMARILLO: 130 registros.
- SIN SEMAFORO: 235 registros.

Por tanto, 22.5% del dataset no presenta una clasificación
de SEMAFORO.

Entre los 808 registros que sí poseen clasificación:

- ROJO: 62.7%
- VERDE: 21.2%
- AMARILLO: 16.1%

La clase ROJO es claramente predominante.

### Evidencia adicional por tipo principal

LÓTICO:
- Total: 772
- Con SEMAFORO: 632
- Sin SEMAFORO: 140

LÉNTICO:
- Total: 140
- Con SEMAFORO: 104
- Sin SEMAFORO: 36

COSTERO:
- Total: 24
- Con SEMAFORO: 5
- Sin SEMAFORO: 19

Los cinco registros COSTERO con clasificación presentan
SEMAFORO VERDE. Esto no implica que el 100% de los registros
costeros sean verdes, ya que 19 de los 24 no presentan SEMAFORO.

### Riesgo para Machine Learning

Los registros sin variable objetivo no pueden utilizarse
directamente como ejemplos etiquetados para entrenamiento
supervisado.

Adicionalmente, el desbalance entre ROJO, VERDE y AMARILLO
puede producir métricas engañosas si el desempeño se evalúa
únicamente mediante accuracy.

### Riesgo para la interfaz

Los porcentajes mostrados al usuario deben distinguir entre:

- registros totales;
- registros evaluados;
- registros sin clasificación.

De lo contrario, podrían comunicarse conclusiones incorrectas.

### Validación necesaria

Determinar por qué 235 registros no presentan SEMAFORO y si
la ausencia se relaciona con:

- indicadores no disponibles;
- tipo o subtipo de cuerpo de agua;
- imposibilidad metodológica de determinar el semáforo;
- otras condiciones del proceso de evaluación.

### Decisión

No imputar ni generar artificialmente la variable objetivo.

Investigar primero la causa de los registros sin SEMAFORO y
considerar el desbalance de clases en la estrategia de
entrenamiento y evaluación.

## Hallazgo 10 – La completitud de indicadores puede modificar la población de entrenamiento

### Evidencia

Se analizó la presencia simultánea de indicadores únicamente
sobre registros con SEMAFORO conocido.

#### LÓTICO – 632 registros

- DBO + DQO + SST:
  470 registros completos (74.4%)

- DBO + DQO + SST + Coliformes:
  315 registros completos (49.8%)

- DBO + DQO + SST + Coliformes + E. coli:
  136 registros completos (21.5%)

#### LÉNTICO – 104 registros

- DBO + DQO + SST:
  79 registros completos (76.0%)

- DBO + DQO + SST + Coliformes:
  39 registros completos (37.5%)

- DBO + DQO + SST + Coliformes + E. coli:
  9 registros completos (8.7%)

### Hallazgo adicional

La reducción de registros no mantiene necesariamente la misma
distribución de la variable objetivo.

En LÓTICO:

Todos los registros:
- AMARILLO: 102 (16.1%)
- ROJO: 411 (65.0%)
- VERDE: 119 (18.8%)

Con DBO + DQO + SST:
- AMARILLO: 76 (16.2%)
- ROJO: 327 (69.6%)
- VERDE: 67 (14.3%)

Con DBO + DQO + SST + Coliformes + E. coli:
- AMARILLO: 30 (22.1%)
- ROJO: 102 (75.0%)
- VERDE: 4 (2.9%)

### Riesgo

Eliminar automáticamente los registros con valores ausentes
puede reducir considerablemente la muestra y modificar la
distribución de SEMAFORO.

La disponibilidad de algunos indicadores podría no ser aleatoria.

Esto debe validarse metodológicamente antes de decidir una
estrategia de eliminación o imputación.

### Decisión preliminar

No eliminar automáticamente registros incompletos.

No imputar automáticamente todas las variables mediante una
estrategia general.

Distinguir primero entre:

1. Indicador que NO APLICA metodológicamente.
2. Indicador que SÍ APLICA pero NO FUE MEDIDO.
3. Dato realmente faltante por otra causa.

### Validación requerida

Confirmar con Ciencia de Datos:

- cómo identificaron estas situaciones;
- qué estrategia utilizaron para valores ausentes;
- si el tratamiento fue condicionado por TIPO/SUBTIPO;
- si evaluaron el efecto sobre la distribución de SEMAFORO.

## Hallazgo 11 – Existen valores censurados en las mediciones

Durante la preparación del Escenario A se identificaron valores
no numéricos con notación de límite inferior.

Ejemplos:

- DBO: <2, <2.97, <0.99, <1
- DQO: <5, <4, <8, <10, <3
- SST: <10, <5, <16, <4.9, entre otros

Cantidad observada:

- DBO: 61 registros
- DQO: 35 registros
- SST: 59 registros

Estos valores no deben interpretarse automáticamente como NaN,
cero o como el propio límite.

Representan mediciones reportadas por debajo de un determinado
límite y requieren una regla metodológica explícita de
transformación antes del entrenamiento.

### Riesgo

Convertir estas columnas directamente a formato numérico mediante
errors="coerce" transformaría los valores censurados en NaN y
eliminaría información disponible.

### Validación requerida

Confirmar con Ciencia de Datos:

- cómo interpretaron los valores expresados mediante "<";
- qué transformación aplicaron;
- si la transformación forma parte del pipeline;
- cómo debe reproducirla posteriormente la API.