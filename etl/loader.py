# PATH: etl/loader.py

import pandas as pd

# Fase 1: Carga y Limpieza de Datos
def cargar_y_limpiar_datos(path_descarga, path_usuarios, path_wbs, path_fichajes):
    # Cargar archivos
    descarga_imputaciones = pd.read_excel(path_descarga)
    listado_usuarios = pd.read_excel(path_usuarios)
    wbs_por_clave = pd.read_excel(path_wbs)
    fichajes_sap = pd.read_excel(path_fichajes)
    
    # Eliminar espacios y tabulaciones al inicio y al final en todas las columnas de tipo string
    descarga_imputaciones = descarga_imputaciones.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    listado_usuarios = listado_usuarios.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    wbs_por_clave = wbs_por_clave.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    fichajes_sap = fichajes_sap.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # Agregar columna "chapa" en T_DESCARGA_IMPUTACIONES
    descarga_imputaciones['chapa'] = descarga_imputaciones['Usuario'].str[:5].astype(int)
    
    # Filtrar registros validados en T_DESCARGA_IMPUTACIONES
    descarga_imputaciones = descarga_imputaciones[descarga_imputaciones['VALIDADA'] == 'S']

    # Eliminar las tareas con OBRA_1 = 0
    descarga_imputaciones = descarga_imputaciones[descarga_imputaciones['OBRA_1'].notna()]
    descarga_imputaciones['OBRA_1'] = descarga_imputaciones['OBRA_1'].astype(int)
    descarga_imputaciones = descarga_imputaciones[descarga_imputaciones['OBRA_1'] != 0]
    
    return descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap
