# main.py
from etl.loader import cargar_y_limpiar_datos
from etl.transformer import generar_tabla_imputaciones, generar_cuadre_horas, generar_variables_negocio
from etl.exporter import generar_csv_salida, generar_cuadre_xlsx
from config.config import PATH_DESCARGA, PATH_USUARIOS, PATH_WBS, PATH_FICHAJES, OUTPUT_DIR
from datetime import datetime
import os

def ejecutar_etl():
    # Crear un subdirectorio con el timestamp dentro de OUTPUT_DIR
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_subdir = os.path.join(OUTPUT_DIR, f"output_{timestamp}")
    os.makedirs(output_subdir, exist_ok=True)

    # Carga y limpieza de datos
    descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap = cargar_y_limpiar_datos(
        PATH_DESCARGA, PATH_USUARIOS, PATH_WBS, PATH_FICHAJES
    )

    # Generar variables de negocio
    descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap = generar_variables_negocio(
        descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap
    )

    # Generar cuadre de horas y procesar el ETL
    cuadre_horas = generar_cuadre_horas(descarga_imputaciones, fichajes_sap)
    horas_proyecto = generar_tabla_imputaciones(descarga_imputaciones, listado_usuarios, wbs_por_clave, fichajes_sap)

    # Generar archivos de salida en el subdirectorio con timestamp
    generar_csv_salida(horas_proyecto, output_subdir)
    generar_cuadre_xlsx(cuadre_horas, output_subdir)

if __name__ == "__main__":
    ejecutar_etl()
