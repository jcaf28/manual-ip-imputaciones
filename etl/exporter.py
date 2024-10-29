# PATH: etl/exporter.py

from datetime import datetime
import os

# Fase 3: Generación del Archivo de Salida
def generar_csv_salida(horas_proyecto, output_dir):
    # Asegurarse de que la carpeta output existe
    os.makedirs(output_dir, exist_ok=True)

    mes = 10
    
    # Crear nombre del archivo con fecha y hora actual
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_path = f"{output_dir}/salida_ETL_{mes}_{timestamp}.xlsx"
    
    # Guardar en Excel
    horas_proyecto.to_excel(output_path, index=False)
    print(f"Archivo exportado a {output_path}")


# etl/exporter.py
import os
from datetime import datetime

def generar_cuadre_xlsx(cuadre_horas, output_dir):
    # Asegurarse de que el directorio de salida existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Crear nombre de archivo con timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_path = os.path.join(output_dir, f"cuadre_horas_{timestamp}.xlsx")
    
    # Guardar el DataFrame en un archivo Excel
    cuadre_horas.to_excel(output_path, index=False)
    print(f"Archivo de cuadre de horas exportado a {output_path}")