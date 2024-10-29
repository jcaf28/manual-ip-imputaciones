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