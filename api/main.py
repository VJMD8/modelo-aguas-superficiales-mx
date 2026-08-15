from fastapi import FastAPI
from pydantic import BaseModel
from modelo.servicio_prediccion import predecir_calidad

app = FastAPI(
    title="API Aguas Superficiales de México",
    version="0.1.0"
)


class DatosAgua(BaseModel):
    tipo: str
    subtipo: str | None = None
    dbo: float | None = None
    dqo: float | None = None
    sst: float | None = None
    coli_fec: float | None = None
    e_coli: float | None = None
    od: float | None = None


@app.get("/")
def inicio():
    return {
        "estado": "ok",
        "mensaje": "API de Aguas Superficiales funcionando"
    }


@app.post("/predecir")
def predecir(datos: DatosAgua):

    resultado_modelo = predecir_calidad(datos)

    return {
        "prediccion": resultado_modelo["prediccion"],
        "tipo": datos.tipo,
        "subtipo": datos.subtipo,
        "modelo": resultado_modelo["modelo"]
    }

    # --------------------------------------------------
    # MODELO PROVISIONAL / MOCK
    # --------------------------------------------------
    # Esta lógica es solo para probar el flujo completo.
    # Luego Sergio sustituirá esta parte por el modelo real.
    # --------------------------------------------------

    if datos.dqo is not None and datos.dqo > 40:
        prediccion = "ROJO"

    elif datos.dqo is not None and datos.dqo > 20:
        prediccion = "AMARILLO"

    else:
        prediccion = "VERDE"

    return {
        "prediccion": prediccion,
        "tipo": datos.tipo,
        "subtipo": datos.subtipo,
        "modelo": "mock_v0.1"
    }