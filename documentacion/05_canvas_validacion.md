# Canvas de Validación con el Equipo de Ciencia de Datos
## Prototipo 2 – Aguas Superficiales de México

### Propósito

Validar decisiones metodológicas que pueden afectar el modelo,
la API y la experiencia final del usuario.

Este documento no busca cuestionar el trabajo realizado por
Ciencia de Datos, sino asegurar que el modelo y la aplicación
utilicen la misma lógica metodológica.

---

# 1. VALORES AUSENTES: NaN

## Lo que encontramos

Los NaN presentan patrones diferentes según el tipo de cuerpo
de agua.

Existen indicadores con 0% de disponibilidad precisamente en
tipos donde metodológicamente no corresponden.

## Riesgo

Tratar todos los NaN como faltantes podría introducir valores
artificiales.

## Necesitamos validar

¿Cómo distinguieron entre:

- indicador que NO APLICA;
- indicador aplicable pero no medido;
- dato realmente faltante?

## Decisión requerida

Definir qué tipos de ausencia pueden imputarse y cuáles deben
mantenerse como "no aplica".

---

# 2. IMPUTACIÓN POR MEDIANA

## Lo que encontramos

CONAGUA utiliza la mediana para calcular determinados indicadores,
pero esto no constituye por sí mismo una regla para imputar valores
ausentes en Machine Learning.

## Riesgo

Confundir:

mediana para calcular un indicador

con:

mediana para sustituir un NaN.

## Necesitamos validar

¿Sobre cuáles variables y registros se realizó imputación por
mediana?

¿Qué criterio justificó esa decisión?

## Decisión requerida

Documentar la estrategia definitiva de imputación.

---

# 3. VARIABLES DERIVADAS Y DATA LEAKAGE

## Lo que encontramos

El dataset contiene:

- mediciones originales;
- variables CALIDAD_*;
- CONTAMINANTES;
- SEMAFORO.

Las variables CALIDAD_* interpretan las mediciones originales
y CONTAMINANTES contiene información vinculada con la evaluación.

## Riesgo

Utilizarlas como X podría permitir que el modelo conozca
indirectamente la respuesta que debe predecir.

## Necesitamos validar

¿CALIDAD_* y CONTAMINANTES fueron excluidas del entrenamiento?

## Decisión requerida

Confirmar la lista definitiva de variables X.

---

# 4. TIPO Y SUBTIPO

## Lo que encontramos

Existen categorías principales:

- LÓTICO
- LÉNTICO
- COSTERO

Pero también aparecen:

- humedales;
- combinaciones lótico-costeras;
- estudios especiales;
- variantes de categorías;
- diferencias de escritura.

## Riesgo

Normalizar categorías automáticamente puede mezclar casos
metodológicamente distintos.

No normalizarlas cuando son equivalentes también puede crear
categorías artificiales para el modelo.

## Necesitamos validar

¿Cuáles categorías fueron normalizadas y bajo qué criterio?

## Decisión requerida

Definir catálogo final de TIPO y SUBTIPO.

---

# 5. PROFUNDIDAD Y TIPO DE ENSAYO

## Lo que encontramos

Existen mediciones diferenciadas para:

- OD general;
- OD superficie;
- OD medio;
- OD fondo;
- diferentes pruebas de toxicidad;
- diferentes profundidades.

## Riesgo

Agruparlas como una única variable puede eliminar significado
metodológico.

## Necesitamos validar

¿Cómo fueron tratadas estas variables durante el entrenamiento?

## Decisión requerida

Definir qué medición debe solicitar la interfaz según el caso.

---

# 6. TOXICIDAD

## Lo que encontramos

Algunas variables de toxicidad presentan porcentajes muy altos
de ausencia, pero forman parte de la metodología de evaluación.

## Riesgo

Eliminar una variable únicamente porque tiene muchos NaN puede
eliminar un indicador metodológicamente relevante.

## Necesitamos validar

¿Cómo se decidió conservar, transformar o excluir cada variable
de toxicidad?

## Decisión requerida

Definir tratamiento definitivo de toxicidad.

---

# 7. VARIABLE OBJETIVO: SEMAFORO

## Lo que encontramos

Dataset total:

1,043 registros.

Distribución:

- ROJO: 507
- VERDE: 171
- AMARILLO: 130
- SIN SEMAFORO: 235

El 22.5% de los registros no tiene variable objetivo.

Entre los 808 registros con SEMAFORO:

- ROJO: 62.7%
- VERDE: 21.2%
- AMARILLO: 16.1%

## Riesgo

Los 235 registros sin Y no pueden utilizarse directamente
como ejemplos etiquetados en aprendizaje supervisado.

Además existe desbalance entre las tres clases.

## Necesitamos validar

¿Por qué existen 235 registros sin SEMAFORO?

¿Fueron excluidos del entrenamiento?

¿Cómo se consideró el desbalance de clases?

## Decisión requerida

Definir población definitiva de entrenamiento y estrategia
de evaluación.

---

# 8. COHERENCIA ENTRE MODELO, API Y FRONTEND

## Principio

El usuario no debería ingresar información que metodológicamente
no corresponde al cuerpo de agua que está evaluando.

La lógica esperada es:

TIPO / SUBTIPO
        ↓
INDICADORES APLICABLES
        ↓
FORMULARIO DINÁMICO
        ↓
JSON
        ↓
API
        ↓
MISMO PREPROCESAMIENTO DEL ENTRENAMIENTO
        ↓
MODELO
        ↓
SEMAFORO
        ↓
EXPLICACIÓN PARA EL USUARIO

## Necesitamos validar

¿Qué variables exactas espera recibir el modelo final?

¿Qué transformaciones deben reproducirse en producción?

## Decisión requerida

Definir el contrato definitivo:

FRONTEND → API → PIPELINE → MODELO.

---

# RESULTADO DE LA VALIDACIÓN

## Confirmado por Ciencia de Datos

Pendiente.

## Ajustes requeridos

Pendiente.

## Variables X definitivas

Pendiente.

## Tratamiento de NaN

Pendiente.

## Pipeline definitivo

Pendiente.

## Modelo seleccionado

Pendiente.