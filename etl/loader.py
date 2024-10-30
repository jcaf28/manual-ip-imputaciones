# PATH: etl/loader.py

import pandas as pd

# Fase 1: Carga y Limpieza de Datos
def cargar_y_limpiar_datos(paths):
    # Diccionario para almacenar los DataFrames con nombres descriptivos
    dataframes = {}

    # Mapear nombres de tabla a cada ruta del archivo
    tabla_nombres = {
        "descarga_imputaciones": paths[0],
        "listado_usuarios": paths[1],
        "wbs_por_clave": paths[2],
        "fichajes_sap": paths[3]
    }
    
    # Cargar y limpiar cada archivo en paths
    for nombre_tabla, path in tabla_nombres.items():
        df = pd.read_excel(path)

        # Eliminar espacios en todas las columnas de tipo string
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # Aplicar filtros específicos solo en la tabla descarga_imputaciones
        if nombre_tabla == "descarga_imputaciones":
            # Agregar columna "chapa"
            df['chapa'] = df['Usuario'].str[:5].astype(int)

        # Añadir el DataFrame al diccionario con el nombre de la tabla
        dataframes[nombre_tabla] = df
    
    # Retorna un diccionario de DataFrames con nombres de tabla
    return dataframes
