# PATH: etl/transformer.py

import pandas as pd

# Fase 2.1
def generar_variables_negocio(descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap):
    # Generar variable 'chapa' específica para 'descarga_imputaciones'
    descarga_imputaciones['chapa'] = descarga_imputaciones['Usuario'].str[:5].astype(int)

    # Aquí puedes agregar otras transformaciones de negocio previas que necesites en el futuro
    # Por ejemplo, podrías agregar cálculos adicionales o normalizar datos en cualquiera de los DataFrames.

    return descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap

# Fase 2.2: Generación de tablas por cruce de Datos
def generar_tabla_imputaciones(descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap):
    
    # FILTRADO: solo horas validadas y eliminando tareas específicas y obras inválidas
    df = descarga_imputaciones

    # Filtrar registros validados
    df = df[df['VALIDADA'] == 'S']
    
    # Eliminar tareas con OBRA_1 = 0
    df = df[df['OBRA_1'].notna()]  # Filtrar filas donde OBRA_1 no es NaN
    df['OBRA_1'] = df['OBRA_1'].astype(int)  # Convertir OBRA_1 a entero
    df = df[df['OBRA_1'] != 0]  # Filtrar filas donde OBRA_1 no es 0
    df['OBRA_1'] = df['OBRA_1'].astype(str) # Convertir OBRA_1 de vuelta a str para el cruce posterior


    df = df[df['IdTarea'] != 'E37']
    df = df[df['TAREA'] != 'AUTORIZACIÓN DE SALIDAS Y AUSENCIAS']

    # Agrupación de horas por proyecto
    df = df.groupby(['chapa', 'OBRA_1'])['Horas'].sum().reset_index()
    
    # Merge con T_LISTADO_USUARIOS para obtener datos de Cost y Cost_2
    df = df.merge(listado_usuarios, left_on='chapa', right_on='IdUsuario', how='left')
    
    # Merge con T_WBS_por_clave para obtener el WBS correcto en función de OBRA_1 y Proceso
    df = df.merge(wbs_por_clave, left_on='OBRA_1', right_on='PROYECTO BAAN', how='left')
    
    # Modificar la columna "WBS" basado en el valor actual de la columna WBS (FMOP3 o FU300)
    df['WBS'] = df.apply(lambda row: row['WBS PROCESOS (FMOP3)'] 
                                                  if 'FMOP3' in row['WBS'] 
                                                  else row['WBS UTILLAJES (FU300)'], axis=1)
    
    # Borrar columnas innecesarias y reordenar
    return df


def generar_cuadre_horas(descarga_imputaciones, fichajes_sap):
    
    #Filtramos solo horas validadas
    df = descarga_imputaciones[descarga_imputaciones['VALIDADA'] == 'S']

    # Agrupar horas por 'chapa' en descarga_imputaciones
    df = df.groupby('chapa')['Horas'].sum().reset_index()
    df.rename(columns={'Horas': 'HorasImputadas'}, inplace=True)
    
    # Obtener solo las columnas necesarias de fichajes_sap y renombrar 'Número de empleado' a 'chapa'
    fichajes_sap = fichajes_sap[['Número de empleado', 'ClockedHRS']].copy()
    fichajes_sap.rename(columns={'Número de empleado': 'chapa', 'ClockedHRS': 'HorasRegistradas'}, inplace=True)
    
    # Hacer un merge entre horas_imputadas y horas_registradas por 'chapa'
    cuadre_horas = pd.merge(df, fichajes_sap, on='chapa', how='outer')
    
    # Calcular la diferencia entre las horas imputadas y las horas registradas
    cuadre_horas['Diferencia'] = cuadre_horas['HorasImputadas'] - cuadre_horas['HorasRegistradas']
    
    return cuadre_horas