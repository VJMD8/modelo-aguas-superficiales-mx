# Aguas Superficiales de México

Prototipo para la evaluación de la calidad de aguas superficiales mediante una interfaz ciudadana conectada a una API de predicción.

## Estado actual

La aplicación integra el modelo final de Machine Learning mediante un flujo funcional de punta a punta:

Usuario → Streamlit → FastAPI → servicio de predicción → modelo ML → resultado

El modelo implementado utiliza Gradient Boosting Classifier y genera una estimación de semáforo en tres categorías: Verde, Amarillo y Rojo.

La experiencia de usuario se organiza en tres etapas: Explorar → Comprender → Evaluar.

## Estructura principal

- `frontend/app.py` — interfaz de usuario en Streamlit.
- `api/main.py` — API desarrollada con FastAPI.
- `modelo/servicio_prediccion.py` — servicio encargado de conectar la API con el modelo.
- `modelo/modelo_calidad_agua.pkl` — modelo final de Machine Learning utilizado para generar la predicción.
- `modelo/mapa_clusters.csv` — información utilizada para la exploración y visualización de los sitios.
- `assets/` — recursos visuales de la interfaz.
- `datos/` — datos utilizados durante el desarrollo.
- `documentacion/` — análisis y documentación técnica del proyecto.
- `requirements.txt` — dependencias necesarias para ejecutar la solución.

## Ejecutar el proyecto

### 1. Activar el entorno virtual

En Windows:

```powershell
.venv\Scripts\Activate.ps1

### 2. Iniciar la API

Desde la raíz del proyecto:

python -m uvicorn api.main:app --reload

### 3. Iniciar la interfaz

Abre una segunda terminal, activa también el entorno virtual y ejecuta:

streamlit run frontend/app.py

*Consideraciones:*
- La salida corresponde a una estimación generada por el modelo de Machine Learning y no sustituye una clasificación oficial de CONAGUA.
- El modelo utiliza 8 indicadores ambientales como variables predictoras.
- La disponibilidad de estos indicadores no es uniforme en todos los registros; el pipeline utiliza imputación por mediana para gestionar valores faltantes.
- El tipo y subtipo del cuerpo de agua aportan contexto, pero no forman parte de las variables predictoras del modelo implementado.
- El análisis mediante K-Means tiene una función exploratoria y no determina la predicción del semáforo.