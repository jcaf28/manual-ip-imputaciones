# PATH: etl/transformer.py

# Fase 2: Transformación de Datos
def transformar_datos(descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap):
    # Agrupación de horas por proyecto
    horas_proyecto = descarga_imputaciones.groupby(['chapa', 'Clave Obra'])['Horas'].sum().reset_index()
    
    # Merge con T_LISTADO_USUARIOS para obtener datos de Cost y Cost_2
    horas_proyecto = horas_proyecto.merge(listado_usuarios, left_on='chapa', right_on='IdUsuario', how='left')
    
    # Merge con T_WBS_por_clave para obtener el WBS correcto en función de Clave Obra y Proceso
    horas_proyecto = horas_proyecto.merge(wbs_por_clave, left_on='Clave Obra', right_on='PROYECTO BAAN', how='left')
    
    # Modificar la columna "WBS" basado en el valor actual de la columna WBS (FMOP3 o FU300)
    horas_proyecto['WBS'] = horas_proyecto.apply(lambda row: row['WBS PROCESOS (FMOP3)'] 
                                                  if 'FMOP3' in row['WBS'] 
                                                  else row['WBS UTILLAJES (FU300)'], axis=1)
    return horas_proyecto