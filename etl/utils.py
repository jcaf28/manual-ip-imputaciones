# PATH: etl/utils.py

import pandas as pd

def verificar_mes_unico(df, columna_fechas="Intervalo de fechas"):
    """
    Verifica que todos los registros en la columna de intervalo de fechas 
    pertenecen al mismo mes. Asume que los valores están en formato "YYYY-MM-DD to YYYY-MM-DD".
    """
    # Extraer los meses de la columna de fechas
    meses = df[columna_fechas].apply(lambda x: pd.to_datetime(x.split(" to ")[0]).month)
    
    # Comprobar si todos los meses son iguales
    if meses.nunique() > 1:
        raise ValueError("El archivo de fichajes contiene intervalos de fechas que no pertenecen al mismo mes.")
    
    return True

def extraer_centro_por_chapa(fichajes_sap, chapa_col='Número de empleado', centro_col='Centro'):
    """
    Devuelve un DataFrame con las columnas 'chapa' y 'centro' para cada empleado 
    según los registros en fichajes_sap.
    """
    return fichajes_sap[[chapa_col, centro_col]].rename(columns={chapa_col: 'chapa', centro_col: 'centro'})

def extraer_fecha_imputacion(fichajes_sap, intervalo_fechas_col='Intervalo de fechas'):
    """
    Extrae la última fecha de 'Intervalo de fechas' y devuelve un DataFrame con 'chapa' y 'fecha_imput'.
    """
    fecha_imput = fichajes_sap[[intervalo_fechas_col, 'Número de empleado']].copy()
    fecha_imput['fecha_imput'] = fecha_imput[intervalo_fechas_col].apply(lambda x: x.split(' to ')[-1].strip())
    fecha_imput['fecha_imput'] = pd.to_datetime(fecha_imput['fecha_imput'], format='%Y-%m-%d')
    return fecha_imput.rename(columns={'Número de empleado': 'chapa'})[['chapa', 'fecha_imput']]