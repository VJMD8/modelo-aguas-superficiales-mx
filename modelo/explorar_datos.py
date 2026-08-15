import pandas as pd

# Ruta donde se encuentra el dataset de CONAGUA
ruta = "datos/aguas_superficiales_2025.xlsx"

# Leer el archivo Excel
df = pd.read_excel(ruta)

# Mostrar información básica
print("Dimensiones del dataset:")
print(df.shape)

print("\nPrimeras 5 filas:")
print(df.head())

print("\nColumnas del dataset:")
for i, columna in enumerate(df.columns, start=1):
    print(f"{i}. {columna}")

    # --------------------------------------------------
# AUDITORÍA DE TIPO DE CUERPO DE AGUA
# --------------------------------------------------

print("\nTipos de cuerpos de agua:")
print(df["TIPO"].value_counts(dropna=False))


# --------------------------------------------------
# VARIABLES DE MEDICIÓN
# --------------------------------------------------

variables_medicion = [
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

# --------------------------------------------------
# DISPONIBILIDAD DE VARIABLES POR TIPO
# --------------------------------------------------

print("\nDisponibilidad de variables por TIPO (%):")

disponibilidad_tipo = (
    df.groupby("TIPO")[variables_medicion]
      .apply(lambda grupo: grupo.notna().mean() * 100)
      .round(1)
)

# Transponer la tabla:
# filas = variables
# columnas = tipos de cuerpo de agua
tabla_disponibilidad = disponibilidad_tipo.T

print(tabla_disponibilidad.to_string())

# --------------------------------------------------
# TABLA SIMPLIFICADA:
# SOLO LOS TRES TIPOS PRINCIPALES
# --------------------------------------------------

tipos_principales = ["LÓTICO", "LÉNTICO", "COSTERO"]

tabla_principal = tabla_disponibilidad[
    [col for col in tipos_principales if col in tabla_disponibilidad.columns]
]

print("\nDisponibilidad en los tres tipos principales (%):")
print(tabla_principal.to_string())

# --------------------------------------------------
# AUDITORÍA DE SUBTIPOS
# --------------------------------------------------

print("\nCantidad de registros por TIPO y SUBTIPO:")

tipos_subtipos = (
    df.groupby(["TIPO", "SUBTIPO"], dropna=False)
      .size()
      .reset_index(name="REGISTROS")
      .sort_values(["TIPO", "REGISTROS"], ascending=[True, False])
)

print(tipos_subtipos.to_string(index=False))

# --------------------------------------------------
# MATRIZ DE APLICABILIDAD OBSERVADA
# Casos principales para comparación
# --------------------------------------------------

casos_principales = {
    "LÓTICO - RÍO": ("LÓTICO", "RÍO"),
    "LÉNTICO - PRESA": ("LÉNTICO", "PRESA"),
    "COSTERO - OCÉANO/MAR": ("COSTERO", "OCÉANO-MAR")
}

resultados = {}

for nombre, (tipo, subtipo) in casos_principales.items():

    filtro = (
        (df["TIPO"].astype(str).str.strip() == tipo) &
        (df["SUBTIPO"].astype(str).str.strip() == subtipo)
    )

    grupo = df.loc[filtro, variables_medicion]

    resultados[nombre] = (
        grupo.notna().mean() * 100
    ).round(1)

matriz_aplicabilidad = pd.DataFrame(resultados)

print("\nMATRIZ DE DISPONIBILIDAD OBSERVADA (%)")
print(matriz_aplicabilidad.to_string())

print("\nNúmero de registros analizados:")

for nombre, (tipo, subtipo) in casos_principales.items():

    filtro = (
        (df["TIPO"].astype(str).str.strip() == tipo) &
        (df["SUBTIPO"].astype(str).str.strip() == subtipo)
    )

    print(f"{nombre}: {filtro.sum()} registros")

# --------------------------------------------------
# ANÁLISIS 5
# FALTANTES EN INDICADORES APLICABLES
# --------------------------------------------------

def auditar_indicadores_aplicables():

    aplicabilidad = {

        "LÓTICO": [
            "DBO_mg/L",
            "DQO_mg/L",
            "SST_mg/L",
            "COLI_FEC_NMP_100mL",
            "E_COLI_NMP_100mL",
            "OD_PORC",
            "TOX_D_48_UT",
            "TOX_V_15_UT"
        ],

        "LÉNTICO": [
            "DBO_mg/L",
            "DQO_mg/L",
            "SST_mg/L",
            "COLI_FEC_NMP_100mL",
            "E_COLI_NMP_100mL",
            "OD_PORC_SUP",
            "OD_PORC_MED",
            "OD_PORC_FON",
            "TOX_D_48_SUP_UT",
            "TOX_D_48_FON_UT",
            "TOX_FIS_SUP_15_UT",
            "TOX_FIS_FON_15_UT"
        ],

        "COSTERO": [
            "SST_mg/L",
            "COLI_FEC_NMP_100mL",
            "ENTEROC_NMP_100mL",
            "OD_PORC_SUP",
            "OD_PORC_MED",
            "OD_PORC_FON",
            "TOX_FIS_SUP_15_UT",
            "TOX_FIS_FON_15_UT"
        ]
    }

    resultados = []

    for tipo, variables in aplicabilidad.items():

        grupo = df[
            df["TIPO"]
            .astype(str)
            .str.strip()
            == tipo
        ]

        total = len(grupo)

        for variable in variables:

            disponibles = (
                grupo[variable]
                .notna()
                .sum()
            )

            faltantes = (
                grupo[variable]
                .isna()
                .sum()
            )

            resultados.append({

                "TIPO": tipo,
                "INDICADOR": variable,
                "REGISTROS": total,
                "CON_DATO": disponibles,
                "SIN_DATO": faltantes,

                "%_DISPONIBLE": round(
                    disponibles / total * 100,
                    1
                ),

                "%_AUSENTE": round(
                    faltantes / total * 100,
                    1
                )
            })

    auditoria = pd.DataFrame(resultados)

    print(
        "\nAUDITORÍA DE "
        "INDICADORES APLICABLES"
    )

    print(
        auditoria.to_string(index=False)
    )

# --------------------------------------------------
# ANÁLISIS 6
# DISTRIBUCIÓN TEMPORAL DEL DATASET
# --------------------------------------------------

def analizar_distribucion_temporal():

    print("\nDISTRIBUCIÓN TEMPORAL DEL DATASET")

    # 1. Registros por año
    registros_anio = (
        df["AÑO"]
        .value_counts(dropna=False)
        .sort_index()
        .rename_axis("AÑO")
        .reset_index(name="REGISTROS")
    )

    print("\n1. REGISTROS POR AÑO")
    print(registros_anio.to_string(index=False))


    # 2. Registros por año y tipo principal
    tipos_principales = ["LÓTICO", "LÉNTICO", "COSTERO"]

    df_temporal = df[
        df["TIPO"]
        .astype(str)
        .str.strip()
        .isin(tipos_principales)
    ].copy()

    tabla_anio_tipo = pd.crosstab(
        df_temporal["AÑO"],
        df_temporal["TIPO"].astype(str).str.strip()
    )

    # Garantizar orden de columnas
    tabla_anio_tipo = tabla_anio_tipo.reindex(
        columns=tipos_principales,
        fill_value=0
    )

    tabla_anio_tipo["TOTAL"] = tabla_anio_tipo.sum(axis=1)

    print("\n2. REGISTROS POR AÑO Y TIPO")
    print(tabla_anio_tipo.to_string())


    # 3. Resumen general
    print("\n3. RESUMEN TEMPORAL")

    print(f"Año mínimo: {df['AÑO'].min()}")
    print(f"Año máximo: {df['AÑO'].max()}")
    print(f"Años diferentes: {df['AÑO'].nunique()}")
    print(f"Registros totales: {len(df)}")

# --------------------------------------------------
# ANÁLISIS 7
# AUDITORÍA DE LA VARIABLE OBJETIVO: SEMAFORO
# --------------------------------------------------

def auditar_semaforo():

    print("\nAUDITORÍA DE LA VARIABLE OBJETIVO: SEMAFORO")

    # --------------------------------------------------
    # 1. Distribución general
    # --------------------------------------------------

    distribucion = (
        df["SEMAFORO"]
        .value_counts(dropna=False)
        .rename_axis("SEMAFORO")
        .reset_index(name="REGISTROS")
    )

    distribucion["PORCENTAJE"] = (
        distribucion["REGISTROS"] / len(df) * 100
    ).round(1)

    print("\n1. DISTRIBUCIÓN GENERAL")
    print(distribucion.to_string(index=False))


    # --------------------------------------------------
    # 2. Valores ausentes
    # --------------------------------------------------

    faltantes = df["SEMAFORO"].isna().sum()

    print("\n2. VALORES AUSENTES EN SEMAFORO")
    print(f"Registros sin SEMAFORO: {faltantes}")


    # --------------------------------------------------
    # 3. Semáforo por tipo principal
    # --------------------------------------------------

    tipos_principales = ["LÓTICO", "LÉNTICO", "COSTERO"]

    df_principal = df[
        df["TIPO"]
        .astype(str)
        .str.strip()
        .isin(tipos_principales)
    ].copy()

    tabla_tipo_semaforo = pd.crosstab(
        df_principal["TIPO"].astype(str).str.strip(),
        df_principal["SEMAFORO"],
        margins=True,
        margins_name="TOTAL"
    )

    print("\n3. SEMAFORO POR TIPO PRINCIPAL")
    print(tabla_tipo_semaforo.to_string())


    # --------------------------------------------------
    # 4. Porcentajes dentro de cada tipo
    # --------------------------------------------------

    tabla_porcentajes = pd.crosstab(
        df_principal["TIPO"].astype(str).str.strip(),
        df_principal["SEMAFORO"],
        normalize="index"
    ) * 100

    tabla_porcentajes = tabla_porcentajes.round(1)

    print("\n4. PORCENTAJE DE SEMAFORO DENTRO DE CADA TIPO")
    print(tabla_porcentajes.to_string())

# --------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------

if __name__ == "__main__":

    auditar_semaforo()