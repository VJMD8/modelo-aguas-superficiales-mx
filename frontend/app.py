import streamlit as st
import requests


# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="Aguas Superficiales de México",
    page_icon="💧",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predecir"


# --------------------------------------------------
# ESTILO BÁSICO
# --------------------------------------------------

st.markdown(
    """
    <style>
        .titulo-principal {
            font-size: 34px;
            font-weight: 700;
            color: #0D2B45;
            margin-bottom: 0px;
        }

        .subtitulo {
            font-size: 18px;
            color: #1D6FA3;
            margin-bottom: 25px;
        }

        .resultado-verde {
            background-color: #E8F5E9;
            border-left: 8px solid #2E8B57;
            padding: 22px;
            border-radius: 12px;
        }

        .resultado-amarillo {
            background-color: #FFF6D8;
            border-left: 8px solid #F4C430;
            padding: 22px;
            border-radius: 12px;
        }

        .resultado-rojo {
            background-color: #FDECEC;
            border-left: 8px solid #E23B3B;
            padding: 22px;
            border-radius: 12px;
        }

        .resultado-titulo {
            font-size: 30px;
            font-weight: 700;
        }

        .nota {
            font-size: 13px;
            color: #5D6D7E;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.markdown(
    '<div class="titulo-principal">💧 Aguas Superficiales de México</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Evaluación predictiva de la calidad del agua</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# PASO 1 - TIPO DE CUERPO DE AGUA
# --------------------------------------------------

st.subheader("1. Selecciona el tipo de cuerpo de agua")

col1, col2 = st.columns(2)

with col1:
    tipo = st.selectbox(
        "Tipo",
        [
            "LÓTICO",
            "LÉNTICO",
            "COSTERO"
        ]
    )

with col2:
    subtipo = st.selectbox(
        "Subtipo",
        [
            "RÍO",
            "ARROYO",
            "PRESA",
            "LAGO",
            "LAGUNA",
            "OCÉANO-MAR",
            "ESTERO",
            "OTRO"
        ]
    )


# --------------------------------------------------
# PASO 2 - INDICADORES
# --------------------------------------------------

st.subheader("2. Ingresa los indicadores ambientales")

st.caption(
    "Versión provisional para validar el flujo completo "
    "Interfaz → API → Predicción."
)

col1, col2, col3 = st.columns(3)

with col1:
    dbo = st.number_input(
        "DBO (mg/L)",
        min_value=0.0,
        value=2.5,
        step=0.1
    )

    dqo = st.number_input(
        "DQO (mg/L)",
        min_value=0.0,
        value=18.0,
        step=0.1
    )

with col2:
    sst = st.number_input(
        "SST (mg/L)",
        min_value=0.0,
        value=12.0,
        step=0.1
    )

    coli_fec = st.number_input(
        "Coliformes fecales (NMP/100 mL)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

with col3:
    e_coli = st.number_input(
        "E. coli (NMP/100 mL)",
        min_value=0.0,
        value=20.0,
        step=1.0
    )

    od = st.number_input(
        "Oxígeno disuelto (%)",
        min_value=0.0,
        value=6.0,
        step=0.1
    )


# --------------------------------------------------
# PASO 3 - ENVIAR A LA API
# --------------------------------------------------

st.divider()

if st.button(
    "Evaluar calidad del agua",
    type="primary",
    use_container_width=True
):

    datos = {
        "tipo": tipo,
        "subtipo": subtipo,
        "dbo": dbo,
        "dqo": dqo,
        "sst": sst,
        "coli_fec": coli_fec,
        "e_coli": e_coli,
        "od": od
    }

    try:

        respuesta = requests.post(
            API_URL,
            json=datos,
            timeout=10
        )

        respuesta.raise_for_status()

        resultado = respuesta.json()

        prediccion = resultado["prediccion"]

        st.subheader("3. Resultado de la evaluación")

        if prediccion == "VERDE":

            st.markdown(
                """
                <div class="resultado-verde">
                    <div class="resultado-titulo">
                        🟢 VERDE
                    </div>
                    Condición estimada favorable.
                </div>
                """,
                unsafe_allow_html=True
            )

        elif prediccion == "AMARILLO":

            st.markdown(
                """
                <div class="resultado-amarillo">
                    <div class="resultado-titulo">
                        🟡 AMARILLO
                    </div>
                    Condición estimada que requiere atención.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="resultado-rojo">
                    <div class="resultado-titulo">
                        🔴 ROJO
                    </div>
                    Condición estimada desfavorable.
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        st.markdown(
            f"""
            **Tipo:** {resultado["tipo"]}  
            **Subtipo:** {resultado["subtipo"]}  
            **Motor actual:** `{resultado["modelo"]}`
            """
        )

        if resultado["modelo"].startswith("mock"):

            st.info(
                "Esta predicción corresponde al motor provisional "
                "utilizado únicamente para validar la integración. "
                "Será sustituido por el modelo final del equipo "
                "de Ciencia de Datos."
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "No fue posible conectar con la API. "
            "Verifica que Uvicorn siga ejecutándose "
            "en http://127.0.0.1:8000."
        )

    except requests.exceptions.RequestException as error:

        st.error(
            f"Ocurrió un error al consultar la API: {error}"
        )


# --------------------------------------------------
# PIE
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="nota">
    Prototipo de Ingeniería de Machine Learning ·
    Datos de Aguas Superficiales de México
    </div>
    """,
    unsafe_allow_html=True
)