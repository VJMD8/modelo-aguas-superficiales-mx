from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# SERVICIO DE PREDICCIÓN
# --------------------------------------------------
# Carga y ejecuta el modelo final de calidad del agua.
# --------------------------------------------------


RUTA_MODELO = Path(__file__).resolve().parent / "modelo_calidad_agua.pkl"

artefacto = joblib.load(RUTA_MODELO)

pipeline = artefacto["pipeline"]
label_encoder = artefacto["label_encoder"]
variables_modelo = artefacto["variables"]


def predecir_calidad(datos):

    entrada = pd.DataFrame(
        [
            {
                "SST_mg/L": datos.sst,
                "COLI_FEC_NMP_100mL": datos.coli_fec,
                "E_COLI_NMP_100mL": datos.e_coli,
                "DQO_mg/L": datos.dqo,
                "DBO_mg/L": datos.dbo,
                "TOX_V_15_UT": datos.tox_v_15,
                "TOX_D_48_UT": datos.tox_d_48,
                "OD_PORC": datos.od_porc,
            }
        ]
    )

    entrada = entrada[variables_modelo]

    pred_codificada = pipeline.predict(entrada)

    prediccion = label_encoder.inverse_transform(pred_codificada)[0]

    return {
        "prediccion": prediccion.upper(),
        "modelo": artefacto["modelo"],
        "version": artefacto["version"],
    }