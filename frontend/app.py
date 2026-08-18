from pathlib import Path

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

st.set_page_config(
    page_title="Aguas Superficiales de México",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================================
# RUTAS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
MODELO_DIR = BASE_DIR / "modelo"

ENCABEZADO_IMG = ASSETS_DIR / "encabezado.png"
PIE_IMG = ASSETS_DIR / "pie_pagina.png"

MAPA_HTML = MODELO_DIR / "mapa_clusters.html"
MAPA_CSV = MODELO_DIR / "mapa_clusters.csv"

API_URL = "http://127.0.0.1:8000/predecir"

SEMAFOROS = {
    "VERDE": ASSETS_DIR / "semaforo_verde.png",
    "AMARILLO": ASSETS_DIR / "semaforo_amarillo.png",
    "ROJO": ASSETS_DIR / "semaforo_rojo.png",
}


# ==========================================================
# CATÁLOGOS DE CONTEXTO
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


DESCRIPCION_TIPO = {
    "LÓTICO":
        "Ríos, arroyos y corrientes con movimiento continuo.",

    "LÉNTICO":
        "Lagos, lagunas, presas y cuerpos de agua con flujo reducido.",

    "COSTERO":
        "Bahías, esteros, estuarios y zonas asociadas al entorno marino.",
}


# ==========================================================
# VARIABLES REALES DEL MODELO
# ==========================================================

INDICADORES_MODELO = [
    "sst",
    "coli_fec",
    "e_coli",
    "dqo",
    "dbo",
    "tox_v_15",
    "tox_d_48",
    "od_porc",
]


ETIQUETAS_INDICADORES = {
    "sst": "SST (mg/L)",
    "coli_fec": "Coliformes fecales (NMP/100 mL)",
    "e_coli": "E. coli (NMP/100 mL)",
    "dqo": "DQO (mg/L)",
    "dbo": "DBO (mg/L)",
    "tox_v_15": "Toxicidad Vibrio fischeri 15 min (UT)",
    "tox_d_48": "Toxicidad Daphnia 48 h (UT)",
    "od_porc": "Oxígeno disuelto (%)",
}


DESCRIPCION_INDICADORES = {
    "sst":
        "Cantidad de sólidos suspendidos presentes en el agua.",

    "coli_fec":
        "Indicador microbiológico asociado con contaminación fecal.",

    "e_coli":
        "Bacteria utilizada como indicador específico de contaminación fecal.",

    "dqo":
        "Cantidad de oxígeno necesaria para oxidar químicamente la materia presente.",

    "dbo":
        "Oxígeno requerido por microorganismos para degradar materia orgánica.",

    "tox_v_15":
        "Respuesta de toxicidad medida con Vibrio fischeri a 15 minutos.",

    "tox_d_48":
        "Respuesta de toxicidad medida con Daphnia a 48 horas.",

    "od_porc":
        "Porcentaje de oxígeno disuelto disponible en el agua.",
}


VALORES_INICIALES = {
    "sst": 12.0,
    "coli_fec": 100.0,
    "e_coli": 20.0,
    "dqo": 18.0,
    "dbo": 2.5,
    "tox_v_15": 1.0,
    "tox_d_48": 1.0,
    "od_porc": 72.0,
}


PASOS = {
    "sst": 0.1,
    "coli_fec": 1.0,
    "e_coli": 1.0,
    "dqo": 0.1,
    "dbo": 0.1,
    "tox_v_15": 0.1,
    "tox_d_48": 0.1,
    "od_porc": 0.1,
}


# ==========================================================
# ESTILOS
# ==========================================================

st.markdown(
    """
    <style>

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

    .metric-card {
        background: white;
        border: 1px solid #DDE8ED;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }

    .metric-number {
        color: #0D5C8B;
        font-size: 28px;
        font-weight: 850;
    }

    .metric-label {
        color: #607784;
        font-size: 12px;
        margin-top: 4px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# DATOS
# ==========================================================

@st.cache_data
def cargar_mapa_clusters():
    if MAPA_CSV.exists():
        return pd.read_csv(MAPA_CSV)

    return pd.DataFrame()


df_mapa = cargar_mapa_clusters()


# ==========================================================
# ESTADO DE NAVEGACIÓN
# ==========================================================

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "EXPLORAR"


# ==========================================================
# CABECERA
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
        type="primary"
        if st.session_state["pagina"] == "EXPLORAR"
        else "secondary",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "EXPLORAR"
        st.rerun()

with nav2:
    if st.button(
        "📖 COMPRENDER\n\n¿Qué significa la información?",
        type="primary"
        if st.session_state["pagina"] == "COMPRENDER"
        else "secondary",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "COMPRENDER"
        st.rerun()

with nav3:
    if st.button(
        "💧 EVALUAR\n\nConsulta una condición del agua",
        type="primary"
        if st.session_state["pagina"] == "EVALUAR"
        else "secondary",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "EVALUAR"
        st.rerun()


# ==========================================================
# PÁGINA 1 — EXPLORAR
# ==========================================================

if st.session_state["pagina"] == "EXPLORAR":

    st.markdown(
        """
        <div class="page-heading">
            Explorar las aguas superficiales de México
        </div>

        <div class="page-intro">
            Conoce la distribución geográfica de los sitios analizados,
            su clasificación observada y los patrones identificados
            mediante agrupamiento.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_mapa.empty:

        st.warning(
            "No se encontró el archivo mapa_clusters.csv."
        )

    else:

        total_sitios = len(df_mapa)
        total_estados = df_mapa["ESTADO"].nunique()

        conteo_verde = (
            df_mapa["SEMAFORO"]
            .astype(str)
            .str.upper()
            .eq("VERDE")
            .sum()
        )

        conteo_rojo = (
            df_mapa["SEMAFORO"]
            .astype(str)
            .str.upper()
            .eq("ROJO")
            .sum()
        )

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                "Sitios analizados",
                f"{total_sitios:,}",
            )

        with m2:
            st.metric(
                "Estados representados",
                total_estados,
            )

        with m3:
            st.metric(
                "Sitios en verde",
                conteo_verde,
            )

        with m4:
            st.metric(
                "Sitios en rojo",
                conteo_rojo,
            )

        st.write("")

        filtro1, filtro2 = st.columns(2)

        with filtro1:

            estados = [
                "Todos"
            ] + sorted(
                df_mapa["ESTADO"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            estado = st.selectbox(
                "Filtrar por estado",
                estados,
            )

        with filtro2:

            semaforos = [
                "Todos"
            ] + sorted(
                df_mapa["SEMAFORO"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            semaforo = st.selectbox(
                "Filtrar por semáforo",
                semaforos,
            )

        df_filtrado = df_mapa.copy()

        if estado != "Todos":
            df_filtrado = df_filtrado[
                df_filtrado["ESTADO"] == estado
            ]

        if semaforo != "Todos":
            df_filtrado = df_filtrado[
                df_filtrado["SEMAFORO"] == semaforo
            ]

        st.markdown(
            '<div class="section-heading">Mapa de sitios y clusters</div>',
            unsafe_allow_html=True,
        )

        if estado == "Todos" and semaforo == "Todos" and MAPA_HTML.exists():

            html_mapa = MAPA_HTML.read_text(
                encoding="utf-8"
            )

            components.html(
                html_mapa,
                height=560,
                scrolling=False,
            )

    mapa_streamlit = df_filtrado[
        [
            "LATITUD",
            "LONGITUD",
            "SEMAFORO",
        ]
    ].dropna(
        subset=["LATITUD", "LONGITUD"]
    ).copy()

    mapa_streamlit["SEMAFORO"] = (
        mapa_streamlit["SEMAFORO"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    COLORES_SEMAFORO = {
        "VERDE": "#2E8B57",
        "AMARILLO": "#E0A800",
        "ROJO": "#D83A3A",
    }

    mapa_streamlit["COLOR"] = (
        mapa_streamlit["SEMAFORO"]
        .map(COLORES_SEMAFORO)
        .fillna("#7A8C95")
    )

    mapa_streamlit = mapa_streamlit.rename(
        columns={
            "LATITUD": "lat",
            "LONGITUD": "lon",
        }
    )

    if not mapa_streamlit.empty:

        st.map(
            mapa_streamlit,
            latitude="lat",
            longitude="lon",
            color="COLOR",
            size=25,
            use_container_width=True,
        )
        st.caption(
            f"Sitios mostrados: {len(df_filtrado):,}"
        )

        st.markdown(
            '<div class="section-heading">Detalle de sitios</div>',
            unsafe_allow_html=True,
        )

        columnas_tabla = [
            "CLAVE",
            "SITIO",
            "ESTADO",
            "SEMAFORO",
            "CLUSTER",
        ]

        st.dataframe(
            df_filtrado[columnas_tabla],
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            """
            <div class="interpretation-card">
                <div class="interpretation-title">
                    ¿Qué representa el cluster?
                </div>
                <div class="interpretation-text">
                    Los clusters son grupos de sitios que presentan
                    características ambientales similares. No equivalen
                    automáticamente a Verde, Amarillo o Rojo; representan
                    patrones encontrados mediante K-Means.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==========================================================
# PÁGINA 2 — COMPRENDER
# ==========================================================

elif st.session_state["pagina"] == "COMPRENDER":

    st.markdown(
        """
        <div class="page-heading">
            Comprender los indicadores de calidad del agua
        </div>

        <div class="page-intro">
            Conoce qué representa cada indicador utilizado por el modelo
            y cómo contribuye a describir la condición del agua.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="context-card">
            El modelo final utiliza ocho variables ambientales.
            El tipo y subtipo del cuerpo de agua aportan contexto,
            pero no forman parte de la predicción del semáforo.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    for indice, variable in enumerate(INDICADORES_MODELO):

        columna = col1 if indice % 2 == 0 else col2

        with columna:

            st.markdown(
                f"""
                <div class="interpretation-card">
                    <div class="interpretation-title">
                        {ETIQUETAS_INDICADORES[variable]}
                    </div>
                    <div class="interpretation-text">
                        {DESCRIPCION_INDICADORES[variable]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    st.markdown(
        '<div class="section-heading">¿Cómo se relacionan con el modelo?</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="interpretation-card">
            <div class="interpretation-title">
                De los indicadores a una estimación
            </div>
            <div class="interpretation-text">
                El modelo de clasificación analiza conjuntamente los
                ocho valores ingresados y estima una categoría de
                semáforo: Verde, Amarillo o Rojo. La predicción no debe
                interpretarse como una determinación oficial, sino como
                una estimación generada a partir del modelo entrenado.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="interpretation-card">
            <div class="interpretation-title">
                ¿Qué variables resultaron más relevantes?
            </div>
            <div class="interpretation-text">
                En el modelo final, DQO, coliformes fecales y E. coli
                aparecen entre las variables con mayor importancia
                predictiva. La importancia del modelo no implica por sí
                sola una relación causal.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# PÁGINA 3 — EVALUAR
# ==========================================================

else:

    st.markdown(
        """
        <div class="page-heading">
            Evaluar la calidad del agua
        </div>

        <div class="page-intro">
            Ingresa los ocho indicadores ambientales utilizados por el
            modelo para obtener una estimación del semáforo de calidad.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="context-card">
            <strong>¿Qué utiliza el modelo?</strong><br>
            La predicción se realiza únicamente con los ocho indicadores
            ambientales mostrados abajo. El tipo y subtipo del cuerpo de
            agua no forman parte del modelo predictivo actual.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_formulario, col_resultado = st.columns(
        [1.15, 0.85],
        gap="large",
    )

    # ======================================================
    # FORMULARIO
    # ======================================================

    with col_formulario:

        st.markdown(
            '<div class="section-heading">Indicadores ambientales</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "Puedes escribir valores con decimales. "
            "La estimación se genera al presionar el botón."
        )

        valores = {}

        columnas = st.columns(2)

        for indice, variable in enumerate(INDICADORES_MODELO):

            with columnas[indice % 2]:

                valores[variable] = st.number_input(
                    ETIQUETAS_INDICADORES[variable],
                    min_value=0.0,
                    value=float(VALORES_INICIALES[variable]),
                    step=0.001,
                    format="%.3f",
                    key=f"input_{variable}",
                )

        st.write("")

        evaluar = st.button(
            "💧 Evaluar calidad del agua",
            type="primary",
            use_container_width=True,
        )

    # ======================================================
    # CONSULTA A LA API
    # ======================================================

    if evaluar:

        payload = {
            # Se mantienen por compatibilidad con la API actual.
            # No son variables predictoras del modelo.
            "tipo": "NO_APLICA",
            "subtipo": None,

            "sst": valores["sst"],
            "coli_fec": valores["coli_fec"],
            "e_coli": valores["e_coli"],
            "dqo": valores["dqo"],
            "dbo": valores["dbo"],
            "tox_v_15": valores["tox_v_15"],
            "tox_d_48": valores["tox_d_48"],
            "od_porc": valores["od_porc"],
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
                "No fue posible conectarse con la API. "
                "Verifica que esté ejecutándose en el puerto 8000."
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"Se presentó un inconveniente al procesar "
                f"la consulta: {error}"
            )

    # ======================================================
    # RESULTADO
    # ======================================================

    with col_resultado:

        st.markdown(
            '<div class="section-heading">Resultado de la evaluación</div>',
            unsafe_allow_html=True,
        )

        if "resultado" not in st.session_state:

            st.markdown(
                """
                <div class="waiting-card">
                    <strong>Sin evaluación</strong>
                    <br><br>
                    Ingresa los indicadores ambientales y presiona
                    <strong>Evaluar calidad del agua</strong>.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            resultado = st.session_state["resultado"]

            prediccion = str(
                resultado["prediccion"]
            ).upper()

            imagen = SEMAFOROS.get(prediccion)

            # --------------------------------------------------
            # INTERPRETACIÓN DEL RESULTADO
            # --------------------------------------------------

            if prediccion == "VERDE":

                clasificacion = "BUENA CALIDAD"

                mensaje = (
                    "El patrón de indicadores ingresado fue clasificado "
                    "por el modelo en la categoría VERDE."
                )

                orientacion = (
                    "La estimación es favorable. Conviene mantener el "
                    "seguimiento de los indicadores y contrastar con "
                    "información oficial cuando corresponda."
                )

            elif prediccion == "AMARILLO":

                clasificacion = "CALIDAD INTERMEDIA"

                mensaje = (
                    "El patrón de indicadores ingresado fue clasificado "
                    "por el modelo en la categoría AMARILLO."
                )

                orientacion = (
                    "La estimación sugiere una condición que requiere "
                    "atención y seguimiento de los indicadores."
                )

            else:

                clasificacion = "MALA CALIDAD"

                mensaje = (
                    "El patrón de indicadores ingresado fue clasificado "
                    "por el modelo en la categoría ROJO."
                )

                orientacion = (
                    "La estimación sugiere señales compatibles con "
                    "deterioro de la calidad y amerita revisión técnica."
                )

            # --------------------------------------------------
            # SEMÁFORO
            # --------------------------------------------------

            if imagen and imagen.exists():

                centro1, centro2, centro3 = st.columns(
                    [0.28, 0.44, 0.28]
                )

                with centro2:

                    st.image(
                        imagen,
                        use_container_width=True,
                    )

            # --------------------------------------------------
            # RESULTADO VISUAL
            # --------------------------------------------------

            st.markdown(
                "#### Condición estimada"
            )

            if prediccion == "VERDE":

                st.success(
                    f"🟢 **{prediccion} — {clasificacion}**"
                )

            elif prediccion == "AMARILLO":

                st.warning(
                    f"🟡 **{prediccion} — {clasificacion}**"
                )

            else:

                st.error(
                    f"🔴 **{prediccion} — {clasificacion}**"
                )

            st.write(
                mensaje
            )

            # --------------------------------------------------
            # COMPRENSIÓN
            # --------------------------------------------------

            st.markdown(
                "#### ¿Qué significa este resultado?"
            )

            st.write(
                "El modelo analiza conjuntamente los ocho indicadores "
                "ambientales registrados y estima una categoría de "
                "semáforo: Verde, Amarillo o Rojo."
            )

            # --------------------------------------------------
            # ORIENTACIÓN
            # --------------------------------------------------

            st.markdown(
                "#### ¿Qué conviene revisar?"
            )

            st.write(
                orientacion
            )

            # --------------------------------------------------
            # INFORMACIÓN DEL MODELO
            # --------------------------------------------------

            st.caption(
                f"Modelo: {resultado.get('modelo', 'N/D')} · "
                f"Versión: {resultado.get('version', 'N/D')}"
            )

            st.caption(
                "Esta predicción es una estimación generada por un "
                "modelo de Machine Learning y no sustituye una "
                "determinación oficial de calidad del agua."
            )

            st.write("")

            # --------------------------------------------------
            # NUEVA CONSULTA
            # --------------------------------------------------

            if st.button(
                "↻ Realizar otra consulta",
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