# Matriz Maestra de Variables
## Prototipo 2 – Aguas Superficiales de México

**Dataset:** aguas_superficiales_2025.xlsx  
**Registros:** 1,043  
**Variables originales:** 46  
**Variable objetivo:** SEMAFORO

---

## 1. Propósito

Esta matriz clasifica las variables del dataset según su función
dentro del Prototipo 2.

El objetivo es diferenciar las variables utilizadas para:

- entrenar el modelo;
- contextualizar los resultados;
- explorar territorialmente la información;
- comprender la calidad del agua;
- validar las predicciones;
- construir la experiencia del usuario.

Principio:

> Una variable excluida del entrenamiento no es necesariamente
> una variable inútil. Puede aportar contexto, explicación,
> validación o experiencia de usuario.

---

## 2. Clasificación utilizada

| Rol | Significado |
|---|---|
| CONTEXTO | Identificación, ubicación, mapas, filtros o explicación |
| X CANDIDATA | Medición original potencialmente utilizable por el modelo |
| X CONDICIONADA | Medición cuya aplicabilidad depende del tipo, profundidad o ensayo |
| DERIVADA | Variable que ya contiene interpretación de otra medición |
| Y | Variable objetivo que se desea predecir |
| EXCLUIR | No se utilizará inicialmente para entrenar |
| VALIDAR | Requiere confirmación metodológica |

---

# 3. Matriz Maestra

| # | Variable | Rol | Modelo | Uso principal | Decisión preliminar |
|---:|---|---|:---:|---|---|
| 1 | CLAVE SITIO | CONTEXTO | No | Explorar | Identificador |
| 2 | NOMBRE DEL SITIO | CONTEXTO | No | Explorar | Identificación para usuario |
| 3 | ORGANISMO_DE_CUENCA | CONTEXTO | No* | Explorar | Contexto territorial |
| 4 | ESTADO | CONTEXTO | No* | Explorar | Filtro y mapa |
| 5 | MUNICIPIO | CONTEXTO | No* | Explorar | Localización |
| 6 | CUENCA | CONTEXTO | No* | Explorar | Contexto hidrográfico |
| 7 | CUERPO DE AGUA | CONTEXTO | No* | Explorar | Identificación |
| 8 | TIPO | VALIDAR | Por definir | Evaluar | Determina aplicabilidad |
| 9 | SUBTIPO | VALIDAR | Por definir | Evaluar | Puede modificar aplicabilidad |
| 10 | LATITUD | CONTEXTO | No* | Explorar | Georreferenciación |
| 11 | LONGITUD | CONTEXTO | No* | Explorar | Georreferenciación |
| 12 | AÑO | EXCLUIR | No | Contexto | Valor constante 2025 |
| 13 | DBO_mg/L | X CANDIDATA | Sí | Evaluar | Medición original |
| 14 | CALIDAD_DBO | DERIVADA | No | Comprender / Validar | Interpretación de DBO |
| 15 | DQO_mg/L | X CANDIDATA | Sí | Evaluar | Medición original |
| 16 | CALIDAD_DQO | DERIVADA | No | Comprender / Validar | Interpretación de DQO |
| 17 | SST_mg/L | X CANDIDATA | Sí | Evaluar | Medición original |
| 18 | CALIDAD_SST | DERIVADA | No | Comprender / Validar | Interpretación de SST |
| 19 | COLI_FEC_NMP_100mL | X CANDIDATA | Sí | Evaluar | Medición microbiológica |
| 20 | CALIDAD_COLI_FEC | DERIVADA | No | Comprender / Validar | Interpretación de CF |
| 21 | E_COLI_NMP_100mL | X CANDIDATA | Sí | Evaluar | Medición microbiológica |
| 22 | CALIDAD_E_COLI | DERIVADA | No | Comprender / Validar | Interpretación de E. coli |
| 23 | ENTEROC_NMP_100mL | X CONDICIONADA | Sí* | Evaluar | Depende del tipo |
| 24 | CALIDAD_ENTEROC | DERIVADA | No | Comprender / Validar | Interpretación de enterococos |
| 25 | OD_PORC | X CONDICIONADA | Sí* | Evaluar | OD según tipo |
| 26 | CALIDAD_OD_PORC | DERIVADA | No | Comprender / Validar | Interpretación de OD |
| 27 | OD_PORC_SUP | X CONDICIONADA | Sí* | Evaluar | OD superficie |
| 28 | CALIDAD_OD_PORC_SUP | DERIVADA | No | Comprender / Validar | Interpretación OD superficie |
| 29 | OD_PORC_MED | X CONDICIONADA | Sí* | Evaluar | OD profundidad media |
| 30 | CALIDAD_OD_PORC_MED | DERIVADA | No | Comprender / Validar | Interpretación OD medio |
| 31 | OD_PORC_FON | X CONDICIONADA | Sí* | Evaluar | OD fondo |
| 32 | CALIDAD_OD_PORC_FON | DERIVADA | No | Comprender / Validar | Interpretación OD fondo |
| 33 | TOX_D_48_UT | X CONDICIONADA | Sí* | Evaluar | Toxicidad según ensayo/tipo |
| 34 | CALIDAD_TOX_D_48 | DERIVADA | No | Comprender / Validar | Interpretación toxicidad |
| 35 | TOX_V_15_UT | X CONDICIONADA | Sí* | Evaluar | Toxicidad según ensayo |
| 36 | CALIDAD_TOX_V_15 | DERIVADA | No | Comprender / Validar | Interpretación toxicidad |
| 37 | TOX_D_48_SUP_UT | X CONDICIONADA | Sí* | Evaluar | Toxicidad superficie |
| 38 | CALIDAD TOX_D_48_SUP | DERIVADA | No | Comprender / Validar | Interpretación |
| 39 | TOX_D_48_FON_UT | X CONDICIONADA | Sí* | Evaluar | Toxicidad fondo |
| 40 | CALIDAD_TOX_D_48_FON | DERIVADA | No | Comprender / Validar | Interpretación |
| 41 | TOX_FIS_SUP_15_UT | X CONDICIONADA | Sí* | Evaluar | Toxicidad superficie |
| 42 | CALIDAD_TOX_FIS_SUP_15 | DERIVADA | No | Comprender / Validar | Interpretación |
| 43 | TOX_FIS_FON_15_UT | X CONDICIONADA | Sí* | Evaluar | Toxicidad fondo |
| 44 | CALIDAD_TOX_FIS_FON_15 | DERIVADA | No | Comprender / Validar | Interpretación |
| 45 | SEMAFORO | Y | Objetivo | Evaluar / Validar | Variable a predecir |
| 46 | CONTAMINANTES | DERIVADA | No | Comprender / Validar | Información posterior a evaluación |

---

# 4. Variables candidatas para el modelo piloto

## Mediciones directas

Las primeras X candidatas son:

- DBO_mg/L
- DQO_mg/L
- SST_mg/L
- COLI_FEC_NMP_100mL
- E_COLI_NMP_100mL
- ENTEROC_NMP_100mL
- OD_PORC
- OD_PORC_SUP
- OD_PORC_MED
- OD_PORC_FON
- TOX_D_48_UT
- TOX_V_15_UT
- TOX_D_48_SUP_UT
- TOX_D_48_FON_UT
- TOX_FIS_SUP_15_UT
- TOX_FIS_FON_15_UT

La inclusión definitiva de cada una dependerá de su aplicabilidad
metodológica y de la estrategia final del modelo.

---

# 5. Variables que no entrenarán inicialmente el modelo

## Variables derivadas

Las variables CALIDAD_* no se utilizarán inicialmente como X.

Razón:

Estas variables ya contienen una interpretación de las mediciones
originales y podrían introducir fuga de información.

---

## CONTAMINANTES

CONTAMINANTES tampoco se utilizará como predictor.

Puede contener información estrechamente relacionada con la
evaluación que determina el SEMAFORO.

Sin embargo, será conservada para:

- validar resultados;
- investigar errores del modelo;
- comprender la condición del agua;
- construir mensajes explicativos;
- apoyar la página COMPRENDER.

---

# 6. Variable objetivo

La variable objetivo será:

**Y = SEMAFORO**

Clases:

- VERDE
- AMARILLO
- ROJO

Los registros sin SEMAFORO no deben recibir una clasificación
artificial para incorporarlos al entrenamiento.

Su tratamiento queda pendiente de validación metodológica.

---

# 7. Rol de TIPO y SUBTIPO

TIPO y SUBTIPO requieren un tratamiento especial.

No se consideran todavía variables predictoras convencionales.

Pueden actuar como variables de control metodológico:

TIPO / SUBTIPO
→ determinar indicadores aplicables
→ construir formulario
→ validar entradas
→ enviar mediciones correspondientes al modelo.

Su incorporación definitiva al pipeline deberá validarse con
Ciencia de Datos.

---

# 8. Separación entre entrenamiento y explicación

## Entrenamiento

MEDICIONES ORIGINALES
→ MODELO
→ PREDICCIÓN DE SEMAFORO

## Validación

PREDICCIÓN
↔ SEMAFORO REAL

CALIDAD_* y CONTAMINANTES pueden utilizarse posteriormente
para investigar la coherencia de los resultados.

## Explicación

PREDICCIÓN
+
INDICADORES
+
CALIDAD_*
+
CONTEXTO
→ MENSAJE COMPRENSIBLE PARA EL USUARIO

Las variables explicativas no deben modificar artificialmente
la predicción obtenida por el modelo.

---

# 9. Relación con la experiencia del usuario

## EXPLORAR

Utilizar principalmente:

- CLAVE SITIO
- NOMBRE DEL SITIO
- ORGANISMO_DE_CUENCA
- ESTADO
- MUNICIPIO
- CUENCA
- CUERPO DE AGUA
- TIPO
- SUBTIPO
- LATITUD
- LONGITUD
- SEMAFORO observado

## COMPRENDER

Utilizar:

- mediciones;
- CALIDAD_*;
- CONTAMINANTES;
- contexto metodológico.

Objetivo:

Explicar qué indicadores están relacionados con la condición
observada del agua.

## EVALUAR

Utilizar:

TIPO / SUBTIPO
→ indicadores aplicables
→ mediciones originales
→ API
→ modelo
→ SEMAFORO predicho.

---

# 10. Principio de diseño

El modelo debe aprender principalmente desde las mediciones
originales.

Las variables que ya contienen interpretaciones o resultados
se utilizarán después para validar, comprender y comunicar,
pero no para facilitar artificialmente el aprendizaje.

---

# 11. Aspectos pendientes de validación

Antes del modelo definitivo se debe confirmar con Ciencia de Datos:

1. Variables X utilizadas finalmente.
2. Tratamiento de TIPO y SUBTIPO.
3. Tratamiento de valores no aplicables.
4. Tratamiento de faltantes reales.
5. Estrategia de imputación.
6. Tratamiento de profundidad.
7. Tratamiento de toxicidad.
8. Registros utilizados para entrenamiento.
9. Manejo del desbalance de SEMAFORO.
10. Pipeline completo de preprocesamiento.

---

## Estado

**Matriz preliminar para modelo piloto – pendiente de validación con el equipo de Ciencia de Datos.**