# PATH: etl/loader.py

import pandas as pd
from etl._constants import COLUMNAS_MINIMAS
from etl._utils import verificar_mes_unico

def cargar_y_limpiar_datos(*paths):
    dataframes = []
    tabla_nombres = ["descarga_imputaciones", "listado_usuarios", "wbs_por_clave", "fichajes_sap"]
    
    # Cargar y limpiar cada archivo en paths
    for nombre_tabla, path in zip(tabla_nombres, paths):
        df = pd.read_excel(path)

        # Eliminar espacios en todas las columnas de tipo string
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Verificar que las columnas mínimas estén presentes en el archivo
        columnas_faltantes = [col for col in COLUMNAS_MINIMAS[nombre_tabla] if col not in df.columns]
        if columnas_faltantes:
            raise ValueError(f"El archivo '{nombre_tabla}' no tiene las siguientes columnas mínimas necesarias: {', '.join(columnas_faltantes)}")
        
        # Verificar que todos los registros de 'Intervalo de fechas' pertenezcan al mismo mes para fichajes_sap
        if nombre_tabla == "fichajes_sap":
            verificar_mes_unico(df)

        dataframes.append(df)
    
    return dataframes  # Devolvemos lista de DataFrames
