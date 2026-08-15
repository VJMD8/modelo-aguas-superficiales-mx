import pandas as pd
from sklearn.model_selection import (
    train_test_split,
    RepeatedStratifiedKFold
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

ruta = "datos/aguas_superficiales_2025.xlsx"

variables_x = [
    "DBO_mg/L",
    "DQO_mg/L",
    "SST_mg/L",
    "COLI_FEC_NMP_100mL",
    "E_COLI_NMP_100mL",
    "ENTEROC_NMP_100mL",
    "OD_PORC",
    "OD_PORC_SUP",
    "OD_PORC_MED",
    "OD_PORC_FON",
    "TOX_D_48_UT",
    "TOX_V_15_UT",
    "TOX_D_48_SUP_UT",
    "TOX_D_48_FON_UT",
    "TOX_FIS_SUP_15_UT",
    "TOX_FIS_FON_15_UT"
]

variable_y = "SEMAFORO"


# --------------------------------------------------
# 1. CARGAR DATOS
# --------------------------------------------------

def cargar_datos():
    return pd.read_excel(ruta)


# --------------------------------------------------
# 2. PREPARAR X e y
# --------------------------------------------------

def preparar_xy(df):

    df_modelado = df[
        df[variable_y].notna()
    ].copy()

    X = df_modelado[variables_x].copy()
    y = df_modelado[variable_y].copy()

    return df_modelado, X, y


# --------------------------------------------------
# 3. AUDITAR DATASET DE MODELADO
# --------------------------------------------------

def auditar_modelado():

    df = cargar_datos()
    df_modelado, X, y = preparar_xy(df)

    print("\nDATASET PARA MODELADO")

    print(f"Registros originales: {len(df)}")
    print(f"Registros con SEMAFORO: {len(df_modelado)}")

    print(
        f"Registros excluidos por Y ausente: "
        f"{len(df) - len(df_modelado)}"
    )

    print(
        f"\nNúmero de variables X candidatas: "
        f"{X.shape[1]}"
    )

    print("\nDistribución de y:")
    print(y.value_counts())

    print("\nDimensiones de X:")
    print(X.shape)

    print("\nFaltantes por variable X:")
    print(
        X.isna()
        .sum()
        .sort_values(ascending=False)
    )

# --------------------------------------------------
# 4. ANALIZAR X POR TIPO DE CUERPO DE AGUA
# --------------------------------------------------

def analizar_x_por_tipo():

    df = cargar_datos()

    # Solo registros que tienen variable objetivo
    df_modelado = df[
        df[variable_y].notna()
    ].copy()

    tipos_principales = [
        "LÓTICO",
        "LÉNTICO",
        "COSTERO"
    ]

    df_modelado = df_modelado[
        df_modelado["TIPO"].isin(tipos_principales)
    ].copy()

    print("\nDISPONIBILIDAD DE X POR TIPO")
    print("Solo registros con SEMAFORO conocido\n")

    for tipo in tipos_principales:

        datos_tipo = df_modelado[
            df_modelado["TIPO"] == tipo
        ]

        print("=" * 60)
        print(f"{tipo}")
        print(f"Registros: {len(datos_tipo)}")
        print("=" * 60)

        resultados = []

        for variable in variables_x:

            con_dato = datos_tipo[variable].notna().sum()
            total = len(datos_tipo)

            porcentaje = (
                con_dato / total * 100
                if total > 0
                else 0
            )

            resultados.append({
                "VARIABLE": variable,
                "CON_DATO": con_dato,
                "TOTAL": total,
                "%_DISPONIBLE": round(porcentaje, 1)
            })

        tabla = pd.DataFrame(resultados)

        print(
            tabla.to_string(index=False)
        )

        print()

# --------------------------------------------------
# 5. ANALIZAR COMPLETITUD SIMULTÁNEA DE INDICADORES
# --------------------------------------------------

def analizar_completitud():

    df = cargar_datos()

    # Solo registros con variable objetivo conocida
    df_modelado = df[
        df[variable_y].notna()
    ].copy()

    # Nos concentramos inicialmente en los dos tipos
    # con suficiente cantidad de registros etiquetados
    tipos_analisis = ["LÓTICO", "LÉNTICO"]

    escenarios = {
        "Escenario 1 - Base fisicoquímica": [
            "DBO_mg/L",
            "DQO_mg/L",
            "SST_mg/L"
        ],

        "Escenario 2 - Base + Coliformes": [
            "DBO_mg/L",
            "DQO_mg/L",
            "SST_mg/L",
            "COLI_FEC_NMP_100mL"
        ],

        "Escenario 3 - Base + Coliformes + E. coli": [
            "DBO_mg/L",
            "DQO_mg/L",
            "SST_mg/L",
            "COLI_FEC_NMP_100mL",
            "E_COLI_NMP_100mL"
        ]
    }

    print("\nCOMPLETITUD SIMULTÁNEA DE INDICADORES")
    print("Solo registros con SEMAFORO conocido\n")

    resultados = []

    for tipo in tipos_analisis:

        datos_tipo = df_modelado[
            df_modelado["TIPO"] == tipo
        ].copy()

        total = len(datos_tipo)

        for nombre, variables in escenarios.items():

            completos = datos_tipo[
                variables
            ].notna().all(axis=1).sum()

            porcentaje = (
                completos / total * 100
                if total > 0
                else 0
            )

            resultados.append({
                "TIPO": tipo,
                "ESCENARIO": nombre,
                "VARIABLES": len(variables),
                "REGISTROS_COMPLETOS": completos,
                "TOTAL": total,
                "%_UTILIZABLE": round(porcentaje, 1)
            })

    tabla = pd.DataFrame(resultados)

    print(
        tabla.to_string(index=False)
    )

# --------------------------------------------------
# 6. ANALIZAR DISTRIBUCIÓN DE Y POR ESCENARIO
# --------------------------------------------------

def analizar_y_por_escenario():

    df = cargar_datos()

    df_modelado = df[
        df[variable_y].notna()
    ].copy()

    tipos_analisis = ["LÓTICO", "LÉNTICO"]

    escenarios = {
        "Base fisicoquímica": [
            "DBO_mg/L",
            "DQO_mg/L",
            "SST_mg/L"
        ],

        "Base + Coliformes": [
            "DBO_mg/L",
            "DQO_mg/L",
            "SST_mg/L",
            "COLI_FEC_NMP_100mL"
        ],

        "Base + Coliformes + E. coli": [
            "DBO_mg/L",
            "DQO_mg/L",
            "SST_mg/L",
            "COLI_FEC_NMP_100mL",
            "E_COLI_NMP_100mL"
        ]
    }

    print("\nDISTRIBUCIÓN DE SEMAFORO POR ESCENARIO\n")

    resultados = []

    for tipo in tipos_analisis:

        datos_tipo = df_modelado[
            df_modelado["TIPO"] == tipo
        ].copy()

        # Distribución original del tipo
        for semaforo, cantidad in (
            datos_tipo[variable_y]
            .value_counts()
            .items()
        ):

            resultados.append({
                "TIPO": tipo,
                "ESCENARIO": "Todos los registros",
                "SEMAFORO": semaforo,
                "REGISTROS": cantidad
            })

        # Distribución después de exigir completitud
        for nombre, variables in escenarios.items():

            completos = datos_tipo[
                datos_tipo[variables]
                .notna()
                .all(axis=1)
            ]

            for semaforo, cantidad in (
                completos[variable_y]
                .value_counts()
                .items()
            ):

                resultados.append({
                    "TIPO": tipo,
                    "ESCENARIO": nombre,
                    "SEMAFORO": semaforo,
                    "REGISTROS": cantidad
                })

    tabla = pd.DataFrame(resultados)

    tabla_final = tabla.pivot_table(
        index=["TIPO", "ESCENARIO"],
        columns="SEMAFORO",
        values="REGISTROS",
        fill_value=0
    )

    print(tabla_final.to_string())

# --------------------------------------------------
# 7. PREPARAR ESCENARIO A Y DIVIDIR TRAIN / TEST
# --------------------------------------------------

def preparar_escenario_a():

    df = cargar_datos()

    # --------------------------------------------------
    # 1. Seleccionar población
    # --------------------------------------------------

    datos = df[
        (df["TIPO"] == "LÓTICO") &
        (df[variable_y].notna())
    ].copy()

    # --------------------------------------------------
    # 2. Variables del Escenario A
    # --------------------------------------------------

    variables_escenario_a = [
        "DBO_mg/L",
        "DQO_mg/L",
        "SST_mg/L"
    ]

    # --------------------------------------------------
    # 3. Conservar únicamente casos completos
    # --------------------------------------------------

    datos_completos = datos.dropna(
        subset=variables_escenario_a
    ).copy()

    X = datos_completos[
        variables_escenario_a
    ].copy()

    y = datos_completos[
        variable_y
    ].copy()

    # --------------------------------------------------
    # 4. División 80 / 20 estratificada
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # --------------------------------------------------
    # 5. Mostrar resultados
    # --------------------------------------------------

    print("\nESCENARIO A - LÓTICO")
    print("Variables: DBO + DQO + SST\n")

    print(f"Registros LÓTICOS con SEMAFORO: {len(datos)}")
    print(f"Registros completos utilizados: {len(datos_completos)}")

    print("\nDIVISIÓN TRAIN / TEST")
    print(f"Train: {len(X_train)} registros")
    print(f"Test:  {len(X_test)} registros")

    print("\nDISTRIBUCIÓN TOTAL")
    print(y.value_counts())
    print("\nPorcentaje:")
    print((y.value_counts(normalize=True) * 100).round(1))

    print("\nDISTRIBUCIÓN TRAIN")
    print(y_train.value_counts())
    print("\nPorcentaje:")
    print((y_train.value_counts(normalize=True) * 100).round(1))

    print("\nDISTRIBUCIÓN TEST")
    print(y_test.value_counts())
    print("\nPorcentaje:")
    print((y_test.value_counts(normalize=True) * 100).round(1))

    return X_train, X_test, y_train, y_test

# --------------------------------------------------
# 8. CONFIGURAR VALIDACIÓN CRUZADA
# --------------------------------------------------

def configurar_validacion_cruzada():

    cv = RepeatedStratifiedKFold(
        n_splits=5,
        n_repeats=3,
        random_state=42
    )

    print("\nVALIDACIÓN CRUZADA CONFIGURADA")
    print("Método: RepeatedStratifiedKFold")
    print("Número de folds: 5")
    print("Número de repeticiones: 3")
    print("Total de evaluaciones: 15")
    print("\nLa validación cruzada se aplicará SOLO sobre TRAIN.")

    return cv

# --------------------------------------------------
# 9. COMPARAR MODELOS INICIALES
# --------------------------------------------------

def comparar_modelos(X_train, y_train, cv):

    print("\nCOMPARACIÓN INICIAL DE MODELOS")
    print("Métrica principal: F1 macro")
    print("Evaluación: solo TRAIN mediante validación cruzada\n")

    # Regresión logística
    modelo_logistico = Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", LogisticRegression(
            max_iter=2000,
            random_state=42
        ))
    ])

    # Árbol de decisión
    modelo_arbol = DecisionTreeClassifier(
        random_state=42
    )

    modelos = {
        "Regresión Logística": modelo_logistico,
        "Árbol de Decisión": modelo_arbol
    }

    metricas = {
        "accuracy": "accuracy",
        "f1_macro": "f1_macro",
        "balanced_accuracy": "balanced_accuracy"
    }

    resultados = []

    for nombre, modelo in modelos.items():

        scores = cross_validate(
            modelo,
            X_train,
            y_train,
            cv=cv,
            scoring=metricas,
            n_jobs=-1
        )

        resultados.append({
            "MODELO": nombre,
            "ACCURACY_MEDIA": scores["test_accuracy"].mean(),
            "F1_MACRO_MEDIA": scores["test_f1_macro"].mean(),
            "BALANCED_ACC_MEDIA":
                scores["test_balanced_accuracy"].mean(),
            "F1_MACRO_STD":
                scores["test_f1_macro"].std()
        })

    tabla = pd.DataFrame(resultados)

    tabla = tabla.sort_values(
        by="F1_MACRO_MEDIA",
        ascending=False
    )

    print(
        tabla.round(3).to_string(index=False)
    )

    return tabla

# --------------------------------------------------
# 10. AUDITAR VALORES NO NUMÉRICOS
# --------------------------------------------------

def auditar_valores_no_numericos():

    df = cargar_datos()

    variables = [
        "DBO_mg/L",
        "DQO_mg/L",
        "SST_mg/L"
    ]

    print("\nAUDITORÍA DE VALORES NO NUMÉRICOS")
    print("Escenario A: DBO + DQO + SST\n")

    for variable in variables:

        serie_original = df[variable]

        # Intentar convertir a número.
        # Los valores que no puedan convertirse se vuelven NaN
        serie_numerica = pd.to_numeric(
            serie_original,
            errors="coerce"
        )

        # Identificar valores originales que existían,
        # pero que no pudieron convertirse a número
        mascara_no_numericos = (
            serie_original.notna()
            &
            serie_numerica.isna()
        )

        valores_problematicos = (
            serie_original[mascara_no_numericos]
            .astype(str)
            .value_counts()
        )

        print("=" * 50)
        print(variable)
        print("=" * 50)

        if len(valores_problematicos) == 0:
            print("Sin valores no numéricos.")
        else:
            print(valores_problematicos.to_string())

        print()

# --------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------

if __name__ == "__main__":

    auditar_valores_no_numericos()