from pathlib import Path

import requests
import streamlit as st


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

st.set_page_config(
    page_title="Aguas Superficiales de México",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = "http://127.0.0.1:8000/predecir"


# ==========================================================
# RUTAS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

ENCABEZADO_IMG = ASSETS_DIR / "encabezado.png"
PIE_IMG = ASSETS_DIR / "pie_pagina.png"

SEMAFOROS = {
    "VERDE": ASSETS_DIR / "semaforo_verde.png",
    "AMARILLO": ASSETS_DIR / "semaforo_amarillo.png",
    "ROJO": ASSETS_DIR / "semaforo_rojo.png",
}


# ==========================================================
# CATÁLOGOS PROVISIONALES
# ==========================================================
# IMPORTANTE:
# Los subtipos y variables definitivos deberán sustituirse
# por los validados por Ciencia de Datos / Fanny.
# Esta estructura permite hacerlo sin rediseñar la interfaz.
# ==========================================================

SUBTIPOS_POR_TIPO = {
    "LÓTICO": [
        "RÍO",
        "ARROYO",
        "CANAL",
        "MANANTIAL",
    ],
    "LÉNTICO": [
        "LAGO",
        "LAGUNA",
        "PRESA",
        "EMBALSE",
    ],
    "COSTERO": [
        "BAHÍA",
        "ESTERO",
        "ESTUARIO",
        "OCÉANO / MAR",
    ],
}


# Por ahora mantenemos las variables que nuestra API provisional acepta.
# Después esta matriz se reemplaza por el contrato real del modelo.

INDICADORES_POR_TIPO = {
    "LÓTICO": [
        "dbo",
        "dqo",
        "sst",
        "coli_fec",
        "e_coli",
        "od",
    ],
    "LÉNTICO": [
        "dbo",
        "dqo",
        "sst",
        "coli_fec",
        "e_coli",
        "od",
    ],
    "COSTERO": [
        "coli_fec",
    ],
}


ETIQUETAS_INDICADORES = {
    "dbo": "DBO (mg/L)",
    "dqo": "DQO (mg/L)",
    "sst": "SST (mg/L)",
    "coli_fec": "Coliformes fecales (NMP/100 mL)",
    "e_coli": "E. coli (NMP/100 mL)",
    "od": "Oxígeno disuelto (%)",
}


VALORES_INICIALES = {
    "dbo": 2.5,
    "dqo": 18.0,
    "sst": 12.0,
    "coli_fec": 100.0,
    "e_coli": 20.0,
    "od": 6.0,
}


PASOS = {
    "dbo": 0.1,
    "dqo": 0.1,
    "sst": 0.1,
    "coli_fec": 1.0,
    "e_coli": 1.0,
    "od": 0.1,
}


# ==========================================================
# ESTILOS
# ==========================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       PÁGINA
    ----------------------------------------------------- */

    .stApp {
        background-color: #F6FAFC !important;
        color: #0D2B45 !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #F6FAFC !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1320px !important;
        padding-top: 0.8rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.6rem !important;
        padding-right: 1.6rem !important;
    }


    /* -----------------------------------------------------
       NAVEGACIÓN
    ----------------------------------------------------- */

    .nav-title {
        color: #0D2B45;
        font-weight: 800;
        font-size: 16px;
    }

    .nav-subtitle {
        color: #607784;
        font-size: 12px;
    }

    div[data-testid="stButton"] > button {
        border-radius: 12px;
        min-height: 62px;
        font-weight: 700;
        border: 1px solid #D5E4EA;
        transition: 0.15s ease;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #FFFFFF;
        color: #0D2B45;
    }

    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        border-color: #2BB3B1;
        color: #0D2B45;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(
            90deg,
            #0D5C8B 0%,
            #2BB3B1 100%
        );
        color: white;
        border: none;
    }


    /* -----------------------------------------------------
       BLOQUES
    ----------------------------------------------------- */

    .page-heading {
        margin-top: 16px;
        margin-bottom: 2px;
        color: #0D2B45;
        font-size: 28px;
        line-height: 1.15;
        font-weight: 850;
    }

    .page-intro {
        color: #607784;
        font-size: 15px;
        margin-bottom: 18px;
    }

    .section-heading {
        color: #0D2B45;
        font-size: 18px;
        font-weight: 800;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .helper {
        color: #687D88;
        font-size: 13px;
        line-height: 1.45;
        margin-bottom: 10px;
    }

    .context-card {
        background: #EDF7FA;
        border: 1px solid #CDE5EC;
        border-radius: 12px;
        padding: 12px 15px;
        color: #294D5B;
        margin-bottom: 12px;
    }

    .waiting-card {
        background: #FFFFFF;
        border: 1px solid #D9E6EB;
        border-radius: 14px;
        padding: 22px;
        color: #607784;
        text-align: center;
        margin-top: 12px;
    }


    /* -----------------------------------------------------
       RESULTADO
    ----------------------------------------------------- */

    .result-card {
        background: #FFFFFF;
        border: 1px solid #D8E6EB;
        border-radius: 16px;
        padding: 20px;
        margin-top: 8px;
    }

    .result-title {
        color: #0D2B45;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 4px;
        text-transform: uppercase;
    }

    .result-state {
        font-size: 34px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 8px;
    }

    .state-good {
        color: #2E8B57;
    }

    .state-medium {
        color: #B78700;
    }

    .state-bad {
        color: #C83A3A;
    }

    .result-copy {
        color: #516A76;
        font-size: 14px;
        line-height: 1.5;
    }

    .interpretation-card {
        background: #F8FBFC;
        border: 1px solid #DDE8ED;
        border-radius: 12px;
        padding: 14px;
        margin-top: 12px;
    }

    .interpretation-title {
        color: #0D2B45;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .interpretation-text {
        color: #58717D;
        font-size: 13px;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# CABECERA MAESTRA
# ==========================================================

if ENCABEZADO_IMG.exists():
    st.image(
        ENCABEZADO_IMG,
        use_container_width=True,
    )
else:
    st.warning(
        f"No se encontró la imagen de encabezado: {ENCABEZADO_IMG}"
    )


# ==========================================================
# NAVEGACIÓN
# ==========================================================

nav1, nav2, nav3 = st.columns(3)

with nav1:
    if st.button(
        "🔎 EXPLORAR\n\n¿Cómo está el agua?",
        use_container_width=True,
    ):
        st.info(
            "La sección Explorar se incorporará en la siguiente etapa."
        )

with nav2:
    if st.button(
        "📖 COMPRENDER\n\n¿Qué significa la información?",
        use_container_width=True,
    ):
        st.info(
            "La sección Comprender se incorporará en la siguiente etapa."
        )

with nav3:
    st.button(
        "💧 EVALUAR\n\nConsulta una condición del agua",
        type="primary",
        use_container_width=True,
        disabled=True,
    )


# ==========================================================
# TÍTULO DE PÁGINA
# ==========================================================

st.markdown(
    """
    <div class="page-heading">
        Evaluar la calidad del agua
    </div>

    <div class="page-intro">
        Selecciona el tipo de cuerpo de agua y registra los
        indicadores disponibles para realizar la consulta.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# DOS COLUMNAS PRINCIPALES
# ==========================================================

col_formulario, col_resultado = st.columns(
    [1.08, 0.92],
    gap="large",
)


# ==========================================================
# COLUMNA IZQUIERDA — FORMULARIO
# ==========================================================

with col_formulario:

    st.markdown(
        '<div class="section-heading">1. Tipo de cuerpo de agua</div>',
        unsafe_allow_html=True,
    )

    tipo = st.selectbox(
        "Selecciona el tipo",
        [
            "Selecciona...",
            "LÓTICO",
            "LÉNTICO",
            "COSTERO",
        ],
    )

    subtipo = None

    if tipo != "Selecciona...":

        subtipo = st.selectbox(
            "Selecciona el subtipo",
            ["Selecciona..."] + SUBTIPOS_POR_TIPO[tipo],
        )

        descripcion_tipo = {
            "LÓTICO":
                "Ríos, arroyos y corrientes con movimiento continuo.",

            "LÉNTICO":
                "Lagos, lagunas, presas y cuerpos de agua con flujo reducido.",

            "COSTERO":
                "Bahías, esteros, estuarios y zonas asociadas al entorno marino.",
        }

        st.markdown(
            f"""
            <div class="context-card">
                <strong>{tipo}</strong><br>
                {descripcion_tipo[tipo]}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ------------------------------------------------------
    # INDICADORES
    # ------------------------------------------------------

    valores = {}

    seleccion_completa = (
        tipo != "Selecciona..."
        and subtipo is not None
        and subtipo != "Selecciona..."
    )

    if seleccion_completa:

        st.markdown(
            """
            <div class="section-heading">
                2. Indicadores de Calidad del Agua
            </div>

            <div class="helper">
                "Ingresa los valores disponibles para realizar la evaluación"
            </div>
            """,
            unsafe_allow_html=True,
        )

        indicadores = INDICADORES_POR_TIPO[tipo]

        # Mostramos hasta 3 columnas
        columnas = st.columns(3)

        for indice, variable in enumerate(indicadores):

            with columnas[indice % 3]:

                valores[variable] = st.number_input(
                    ETIQUETAS_INDICADORES[variable],
                    min_value=0.0,
                    value=float(VALORES_INICIALES[variable]),
                    step=float(PASOS[variable]),
                    key=f"input_{variable}",
                )


        # --------------------------------------------------
        # EVALUAR
        # --------------------------------------------------

        st.write("")

        evaluar = st.button(
            "Evaluar calidad del agua",
            type="primary",
            use_container_width=True,
        )

    else:
        evaluar = False


# ==========================================================
# CONSULTA A API
# ==========================================================

if evaluar:

    # La API provisional todavía espera estas variables.
    # Si alguna no aparece para el tipo seleccionado,
    # se envía None.

    payload = {
        "tipo": tipo,
        "subtipo": subtipo,

        "dbo": valores.get("dbo"),
        "dqo": valores.get("dqo"),
        "sst": valores.get("sst"),

        "coli_fec": valores.get("coli_fec"),
        "e_coli": valores.get("e_coli"),
        "od": valores.get("od"),
    }

    try:

        with st.spinner(
            "Evaluando la información..."
        ):

            respuesta = requests.post(
                API_URL,
                json=payload,
                timeout=10,
            )

            respuesta.raise_for_status()

        st.session_state["resultado"] = respuesta.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "No fue posible realizar la evaluación en este momento."
        )

    except requests.exceptions.RequestException:

        st.error(
            "Se presentó un inconveniente al procesar la consulta."
        )


# ==========================================================
# COLUMNA DERECHA — RESULTADO
# ==========================================================

with col_resultado:

    if "resultado" not in st.session_state:

        st.markdown(
            """
            <div class="waiting-card">
                <strong>Resultado de la evaluación</strong>
                <br><br>
                El resultado aparecerá aquí después de seleccionar
                el tipo de agua, registrar los indicadores y realizar
                la consulta.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        resultado = st.session_state["resultado"]
        prediccion = resultado["prediccion"]

        imagen = SEMAFOROS.get(prediccion)

        # ----------------------------------------------
        # TRADUCCIÓN CIUDADANA
        # ----------------------------------------------

        if prediccion == "VERDE":

            clasificacion = "BUENA"
            clase_css = "state-good"

            mensaje = (
                "La condición evaluada presenta una calidad favorable "
                "de acuerdo con los criterios utilizados."
            )

        elif prediccion == "AMARILLO":

            clasificacion = "CALIDAD INTERMEDIA"
            clase_css = "state-medium"

            mensaje = (
                "La condición evaluada presenta aspectos que requieren "
                "atención y seguimiento."
            )

        else:

            clasificacion = "MALA"
            clase_css = "state-bad"

            mensaje = (
                "La condición evaluada presenta señales de deterioro "
                "que requieren atención."
            )


        st.markdown(
            '<div class="section-heading">Resultado de la evaluación</div>',
            unsafe_allow_html=True,
        )

        r1, r2 = st.columns(
            [0.38, 0.62],
            gap="medium",
        )

        with r1:

            if imagen and imagen.exists():

                st.image(
                    imagen,
                    use_container_width=True,
                )

        with r2:

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-title">Condición estimada</div>
                    <div class="result-state {clase_css}">{clasificacion}</div>
                    <div class="result-copy">{mensaje}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------
        # INTERPRETACIÓN
        # ----------------------------------------------

        st.markdown(
            """
            <div class="interpretation-card">
            <div class="interpretation-title">¿Qué significa este resultado?</div>
            <div class="interpretation-text">Esta evaluación brinda una referencia sobre la condición estimada del agua
            a partir de los indicadores ingresados
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        # ----------------------------------------------
        # NUEVA CONSULTA
        # ----------------------------------------------

        st.write("")

        if st.button(
            "Realizar otra consulta",
            use_container_width=True,
        ):

            if "resultado" in st.session_state:
                del st.session_state["resultado"]

            st.rerun()


# ==========================================================
# PIE COMÚN
# ==========================================================

st.write("")

if PIE_IMG.exists():

    st.image(
        PIE_IMG,
        use_container_width=True,
    )

else:

    st.caption(
        "Fuente de información: CONAGUA · "
        "Sistema de consulta ciudadana"
    )