# PATH: main.py

# main.py
from etl.loader import cargar_y_limpiar_datos
from etl.transformer import generar_tabla_imputaciones, generar_cuadre_horas
from etl.exporter import generar_csv_salida, generar_cuadre_xlsx
from config.config import PATH_DESCARGA, PATH_USUARIOS, PATH_WBS, PATH_FICHAJES, OUTPUT_DIR

"""
T_LISTADO_USUARIOS (indica a qué WBS imputa cada usuario)

IdUsuario,Usuario,WBS,Cost,Cost_2
3,SUB. HORAS DISEÑO,FMOP3,RO60061.00,5105
10705,Eli Arroyo,FMOP3,RO60061.00,5105

T_WBS_por_clave (Indica qué WBS tiene cada uno de los proyectos, según si el usuario es de un tipo o de otro)

PROYECTO BAAN,PROYECTO SAP,WBS PROCESOS (FMOP3),WBS UTILLAJES (FU300),PSA
1010,RO-1010-1,RO-1010-1-T-B-W-MP-MAPB3,RO-1010-1-T-B-W-TO-TOOB3,BA01

T_FICHAJES_SAP: 

Centro,Sociedad,Intervalo de fechas,Número de empleado,Nombre del empleado,Supervisor,Nombre del equipo,ClockedHRS,ManufacturingHrs,OverCostHrs,IndirectHrs,ProjectHrs,MaintenanceHrs,TotConfirmHrs,TotalApprovedHours,DifferenceClockedConfirmed,DifferenceConfirmedApproved
AES1,ES01,2024-09-02 to 2024-09-30,10705,ELIXABETE ARROYO,EIDER ARRIOLA,50000635 AES1_D3_IP_PROCESOS,120.85,0,0.0,0,120.85,0,120.85,120.85,0,0

El excel de salida es el siguiente: 

AES1;30/09/2024;13144;2.5;RO60061.00;5105;RO-1010-1-T-B-W-MP-MAPB3;;;BG14

"""

def ejecutar_etl():
    # Crear un array con las rutas de los archivos
    paths = [PATH_DESCARGA, PATH_USUARIOS, PATH_WBS, PATH_FICHAJES]
    
    # Ejecutar fase de carga y limpieza, recibe un array de DataFrames
    dataframes = cargar_y_limpiar_datos(paths)
    
    # Asignar cada DataFrame a una variable específica para claridad
    descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap = dataframes

    # Generar cuadre de horas

    cuadre_horas = generar_cuadre_horas(descarga_imputaciones, fichajes_sap)
    
    # Ejecutar transformación y generación del archivo de salida
    horas_proyecto = generar_tabla_imputaciones(descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap)

    generar_csv_salida(horas_proyecto, OUTPUT_DIR)
    generar_cuadre_xlsx(cuadre_horas, OUTPUT_DIR)

if __name__ == "__main__":
    ejecutar_etl()