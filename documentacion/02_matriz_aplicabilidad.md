# Matriz de Aplicabilidad de Indicadores
## Prototipo 2 – Aguas Superficiales de México

**Proyecto:** Sistema de exploración, comprensión y evaluación de la calidad del agua superficial  
**Fuente metodológica:** CONAGUA  
**Dataset de trabajo:** aguas_superficiales_2025.xlsx  
**Registros del dataset:** 1,043  
**Variables:** 46  

---

## 1. Propósito

Esta matriz documenta qué indicadores de calidad del agua superficial
corresponden a los diferentes tipos de cuerpos de agua y contrasta
la metodología de CONAGUA con la disponibilidad observada en el
dataset utilizado por el proyecto.

Su finalidad es evitar que los valores ausentes sean tratados
automáticamente como datos faltantes sin determinar previamente
si el indicador aplica metodológicamente al tipo de cuerpo de agua.

---

## 2. Principio metodológico

Un valor NaN indica ausencia de un valor en el dataset, pero no
explica la causa de dicha ausencia.

Antes de eliminar o imputar un valor se debe distinguir entre:

- NO APLICA: el indicador no corresponde metodológicamente al caso.
- FALTANTE REAL: el indicador corresponde, pero el valor no está disponible.
- REQUIERE REVISIÓN: la evidencia disponible no permite determinar
  todavía la causa de la ausencia.

Principio del proyecto:

> Antes de transformar un dato, comprender qué representa
> metodológicamente su presencia o ausencia.

---

## 3. Ocho familias de indicadores CONAGUA

Los indicadores considerados para aguas superficiales son:

1. Demanda Bioquímica de Oxígeno (DBO5)
2. Demanda Química de Oxígeno (DQO)
3. Sólidos Suspendidos Totales (SST)
4. Coliformes fecales (CF)
5. Escherichia coli (E. coli)
6. Enterococos fecales
7. Porcentaje de saturación de Oxígeno Disuelto (OD%)
8. Toxicidad aguda

Algunas familias presentan diferentes mediciones según el tipo
de cuerpo de agua, profundidad o ensayo utilizado.

---

## 4. Aplicabilidad metodológica por tipo de cuerpo

| Indicador | Lótico | Léntico | Costero |
|---|:---:|:---:|:---:|
| DBO5 | Sí | Sí | No |
| DQO | Sí | Sí | No |
| SST | Sí | Sí | Sí |
| Coliformes fecales | Sí | Sí | Sí |
| E. coli | Sí | Sí | No |
| Enterococos fecales | No | No | Sí |
| OD % general | Sí | No | No |
| OD % superficie | No | Sí | Sí |
| OD % medio | No | Sí | Sí |
| OD % fondo | No | Sí | Sí |
| Toxicidad Daphnia 48 h | Sí | No | No |
| Toxicidad Daphnia 48 h superficie | No | Sí | No |
| Toxicidad Daphnia 48 h fondo | No | Sí | No |
| Toxicidad Vibrio fischeri 15 min | Sí | No | No |
| Toxicidad V. fischeri superficie | No | Sí | Sí |
| Toxicidad V. fischeri fondo | No | Sí | Sí |

---

## 5. Disponibilidad observada en el dataset

Para realizar una primera comparación se analizaron tres grupos
representativos:

- LÓTICO – RÍO: 667 registros
- LÉNTICO – PRESA: 84 registros
- COSTERO – OCÉANO/MAR: 12 registros

| Variable | Lótico-Río | Léntico-Presa | Costero-Océano/Mar |
|---|---:|---:|---:|
| DBO | 70.0% | 77.4% | 0.0% |
| DQO | 81.7% | 85.7% | 0.0% |
| SST | 84.7% | 94.0% | 8.3% |
| Coliformes fecales | 50.8% | 38.1% | 91.7% |
| E. coli | 31.0% | 17.9% | 0.0% |
| Enterococos | 0.0% | 0.0% | 0.0% |
| OD % general | 26.7% | 0.0% | 0.0% |
| OD % superficie | 0.0% | 20.2% | 8.3% |
| OD % medio | 0.0% | 1.2% | 0.0% |
| OD % fondo | 0.0% | 1.2% | 0.0% |
| TOX Daphnia 48 h | 2.7% | 0.0% | 0.0% |
| TOX Vibrio fischeri 15 min | 14.1% | 0.0% | 0.0% |
| TOX Daphnia superficie | 0.0% | 0.0% | 0.0% |
| TOX Daphnia fondo | 0.0% | 0.0% | 0.0% |
| TOX V. fischeri superficie | 0.0% | 15.5% | 0.0% |
| TOX V. fischeri fondo | 0.0% | 0.0% | 0.0% |

---

## 6. Hallazgos preliminares

### Hallazgo 1 – Los NaN presentan estructura

La ausencia de valores no parece distribuirse aleatoriamente.
Existen patrones claros asociados al tipo de cuerpo de agua.

Ejemplos:

- DBO y DQO no presentan valores en el grupo Costero-Océano/Mar.
- Enterococos no presenta valores en Lótico-Río ni Léntico-Presa.
- OD % general aparece en Lótico-Río, pero no en Léntico-Presa.
- OD % superficie aparece en Léntico-Presa y no en Lótico-Río.

Estos patrones son consistentes con diferencias metodológicas
entre tipos de cuerpos de agua.

### Hallazgo 2 – "No aplica" no debe convertirse automáticamente en mediana

Si una variable no corresponde metodológicamente a determinado
tipo de cuerpo de agua, imputar un valor produciría una medición
artificial que no representa la realidad del caso.

### Hallazgo 3 – Existen también posibles faltantes reales

Hay indicadores metodológicamente aplicables que no están presentes
en todos los registros.

Ejemplos:

- DBO en Lótico-Río: 70.0%
- DQO en Léntico-Presa: 85.7%
- Coliformes fecales en Lótico-Río: 50.8%

Estos casos requieren investigación antes de definir una estrategia
de imputación.

### Hallazgo 4 – Baja disponibilidad no significa baja importancia

Las variables de toxicidad presentan porcentajes bajos de
disponibilidad, pero forman parte de la metodología del semáforo.

Por tanto, no deben eliminarse únicamente por presentar una
proporción elevada de valores ausentes.

### Hallazgo 5 – Existen inconsistencias de categorización

Se observaron variantes como:

- OCÉANO-MAR / OCEANO-MAR
- posibles espacios adicionales en categorías
- tipos especiales y combinados
- humedales
- estudios especiales

Estas categorías deben revisarse y normalizarse únicamente cuando
exista justificación metodológica.

---

## 7. Diferencia crítica: cálculo del indicador vs. imputación

CONAGUA utiliza diferentes estadísticos para calcular indicadores:

- Mediana: DBO, DQO, SST y OD%.
- Media geométrica: Coliformes fecales, E. coli y Enterococos.
- Máximo de las toxicidades determinadas: indicadores de toxicidad.

Esto NO implica automáticamente que un valor NaN deba ser sustituido
mediante la mediana.

Son dos procesos conceptualmente diferentes:

MEDICIONES REALES
→ estadístico definido por CONAGUA
→ INDICADOR

VALOR AUSENTE
→ determinar causa
→ decidir si no aplica o si es faltante real
→ evaluar tratamiento

---

## 8. Implicaciones para Machine Learning

Antes de entrenar el modelo se debe validar:

- Variables predictoras finales (X).
- Variable objetivo: SEMAFORO (Y).
- Exclusión de variables que puedan producir fuga de información.
- Tratamiento diferenciado entre "no aplica" y "faltante real".
- Normalización de TIPO y SUBTIPO.
- Tratamiento de indicadores de toxicidad.
- Manejo de mediciones de superficie, medio y fondo.
- Estrategia de imputación utilizada cuando corresponda.

Las variables CALIDAD_* y CONTAMINANTES requieren especial atención,
ya que contienen información derivada de las mediciones y/o del
resultado de evaluación y podrían producir fuga de información.

---

## 9. Implicaciones para API y frontend

La interfaz no debe solicitar automáticamente todos los indicadores.

La lógica deseada es:

TIPO / SUBTIPO
→ determinar indicadores aplicables
→ mostrar únicamente campos correspondientes
→ validar entradas
→ generar JSON
→ API
→ preprocesamiento
→ modelo
→ predicción
→ resultado para el usuario

Esto permite que la experiencia del usuario respete la misma lógica
metodológica utilizada durante el entrenamiento del modelo.

---

## 10. Aspectos pendientes de validación con Ciencia de Datos

1. ¿Cómo se distinguieron los valores "no aplica" de los faltantes reales?
2. ¿Sobre cuáles valores se realizó imputación?
3. ¿Qué criterio se utilizó para la imputación?
4. ¿Las variables CALIDAD_* fueron excluidas como predictoras?
5. ¿CONTAMINANTES fue excluida como predictor?
6. ¿Cómo se trataron TIPO y SUBTIPO?
7. ¿Cómo se trataron las diferentes mediciones de OD?
8. ¿Cómo se trataron las diferentes pruebas de toxicidad?
9. ¿Qué variables X quedaron finalmente en el modelo?
10. ¿El pipeline conserva exactamente estas transformaciones al realizar una nueva predicción?

---

## 11. Estado

DOCUMENTO DE TRABAJO – PENDIENTE DE VALIDACIÓN

Esta matriz no sustituye el criterio metodológico de CONAGUA ni las
decisiones finales del equipo de Ciencia de Datos.

Su función es documentar evidencia, identificar riesgos y facilitar
la validación antes de integrar el modelo definitivo con la API y
la interfaz.