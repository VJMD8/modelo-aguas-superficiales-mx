# Aguas Superficiales de México

Prototipo para la evaluación de la calidad de aguas superficiales mediante una interfaz ciudadana conectada a una API de predicción.

## Estado actual

La aplicación cuenta con un flujo funcional de punta a punta:

Usuario → Streamlit → FastAPI → servicio de predicción → resultado

Actualmente el servicio utiliza un motor provisional (`mock_v0.1`) para validar la integración completa.

El modelo definitivo de Machine Learning será incorporado posteriormente sin modificar la arquitectura principal de la interfaz.

## Estructura principal

- `frontend/app.py` — interfaz de usuario en Streamlit.
- `api/main.py` — API desarrollada con FastAPI.
- `modelo/servicio_prediccion.py` — servicio encargado de realizar la predicción.
- `assets/` — recursos visuales de la interfaz.
- `datos/` — datos utilizados durante el desarrollo.
- `documentacion/` — análisis y documentación técnica del proyecto.

## Ejecutar el proyecto

### 1. Activar el entorno virtual

En Windows:

```powershell
.venv\Scripts\Activate.ps1