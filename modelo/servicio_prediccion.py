# --------------------------------------------------
# SERVICIO DE PREDICCIÓN
# --------------------------------------------------
# Hoy utiliza una lógica provisional (mock).
# Posteriormente Sergio sustituirá esta función
# por la carga y ejecución del modelo real.
# --------------------------------------------------


def predecir_calidad(datos):

    dqo = datos.dqo

    # --------------------------------------------------
    # MODELO PROVISIONAL
    # --------------------------------------------------

    if dqo is not None and dqo > 40:
        prediccion = "ROJO"

    elif dqo is not None and dqo > 20:
        prediccion = "AMARILLO"

    else:
        prediccion = "VERDE"

    return {
        "prediccion": prediccion,
        "modelo": "mock_v0.1"
    }