from fastapi import FastAPI
from pydantic import BaseModel

from modelo.servicio_prediccion import predecir_calidad


app = FastAPI(
    title="API Aguas Superficiales de México",
    version="1.0.0"
)


class DatosAgua(BaseModel):
    # Información contextual
    tipo: str
    subtipo: str | None = None

    # Variables utilizadas por el modelo
    dbo: float | None = None
    dqo: float | None = None
    sst: float | None = None
    coli_fec: float | None = None
    e_coli: float | None = None
    tox_v_15: float | None = None
    tox_d_48: float | None = None
    od_porc: float | None = None


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
        "modelo": resultado_modelo["modelo"],
        "version": resultado_modelo["version"]
    }