# PATH: etl/transformer.py

import pandas as pd

# Fase 2: Transformación de Datos
def generar_tabla_imputaciones(descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap):
    
    # FILTRADO: solo horas validadas y eliminando tareas específicas y obras inválidas
    df = descarga_imputaciones

    # Filtrar registros validados
    df = df[df['VALIDADA'] == 'S']
    
    # Eliminar tareas con OBRA_1 = 0
    df = df[df['OBRA_1'].notna()]  # Filtrar filas donde OBRA_1 no es NaN
    df['OBRA_1'] = df['OBRA_1'].astype(int)  # Convertir OBRA_1 a entero
    df = df[df['OBRA_1'] != 0]  # Filtrar filas donde OBRA_1 no es 0
    df = df[df['IdTarea'] != 'E37']
    df = df[df['TAREA'] != 'AUTORIZACIÓN DE SALIDAS Y AUSENCIAS']

    # Agrupación de horas por proyecto
    df = df.groupby(['chapa', 'Clave Obra'])['Horas'].sum().reset_index()
    
    # Merge con T_LISTADO_USUARIOS para obtener datos de Cost y Cost_2
    df = df.merge(listado_usuarios, left_on='chapa', right_on='IdUsuario', how='left')
    
    # Merge con T_WBS_por_clave para obtener el WBS correcto en función de Clave Obra y Proceso
    df = df.merge(wbs_por_clave, left_on='Clave Obra', right_on='PROYECTO BAAN', how='left')
    
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
    df = fichajes_sap[['Número de empleado', 'ClockedHRS']].copy()
    df.rename(columns={'Número de empleado': 'chapa', 'ClockedHRS': 'HorasRegistradas'}, inplace=True)
    
    # Hacer un merge entre horas_imputadas y horas_registradas por 'chapa'
    cuadre_horas = pd.merge(df, df, on='chapa', how='outer')
    
    # Calcular la diferencia entre las horas imputadas y las horas registradas
    cuadre_horas['Diferencia'] = cuadre_horas['HorasImputadas'] - cuadre_horas['HorasRegistradas']
    
    return cuadre_horas