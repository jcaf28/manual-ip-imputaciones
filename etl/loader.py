# PATH: etl/loader.py

import pandas as pd

# Fase 1: Carga y Limpieza de Datos
def cargar_y_limpiar_datos(paths):
    # Crear lista de DataFrames
    dataframes = []
    
    # Cargar y limpiar cada archivo en paths
    for i, path in enumerate(paths):
        df = pd.read_excel(path)
        
        # Eliminar espacios en todas las columnas de tipo string
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Aplicar filtros específicos solo en descarga_imputaciones (primer archivo)
        if i == 0:
            # Agregar columna "chapa"
            df['chapa'] = df['Usuario'].str[:5].astype(int)
            
            # Filtrar registros validados
            df = df[df['VALIDADA'] == 'S']
            
            # Eliminar tareas con OBRA_1 = 0
            df = df[df['OBRA_1'].notna()]  # Filtrar filas donde OBRA_1 no es NaN
            df['OBRA_1'] = df['OBRA_1'].astype(int)  # Convertir OBRA_1 a entero
            df = df[df['OBRA_1'] != 0]  # Filtrar filas donde OBRA_1 no es 0
            df = df[df['IdTarea'] != 'E37'] # Filtrar filas donde IdTarea no es E37

            print("stop")
            
        # Agregar DataFrame a la lista de resultados
        dataframes.append(df)
    
    # Retorna un array de DataFrames
    return dataframes