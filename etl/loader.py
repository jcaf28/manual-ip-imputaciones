# PATH: etl/loader.py

import pandas as pd

def cargar_y_limpiar_datos(*paths):
    # Definir las columnas mínimas requeridas para cada archivo
    columnas_minimas = {
        "descarga_imputaciones": ["Id.", "Usuario", "Fecha", "Clave Obra", "CodObra", "OBRA", "Proceso", 
                                  "IdTarea", "TAREA", "Descripción", "Plano", "Horas", "Euros", "VALIDADA", 
                                  "TIPO", "OBRA_1", "QTY_1", "OBRA_2", "QTY_2", "Nº Mod. OT"],
        "listado_usuarios": ["IdUsuario", "Usuario", "WBS", "Cost", "Cost_2"],
        "wbs_por_clave": ["PROYECTO BAAN", "PROYECTO SAP", "WBS PROCESOS (FMOP3)", "WBS UTILLAJES (FU300)", "PSA"],
        "fichajes_sap": ["Centro", "Sociedad", "Intervalo de fechas", "Número de empleado", "Nombre del empleado", 
                          "Supervisor", "Nombre del equipo", "ClockedHRS", "ManufacturingHrs", "OverCostHrs", 
                          "IndirectHrs", "ProjectHrs", "MaintenanceHrs", "TotConfirmHrs", "TotalApprovedHours", 
                          "DifferenceClockedConfirmed", "DifferenceConfirmedApproved"]
    }
    
    dataframes = []
    tabla_nombres = ["descarga_imputaciones", "listado_usuarios", "wbs_por_clave", "fichajes_sap"]
    
    # Cargar y limpiar cada archivo en paths
    for nombre_tabla, path in zip(tabla_nombres, paths):
        df = pd.read_excel(path)

        # Eliminar espacios en todas las columnas de tipo string
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Verificar que las columnas mínimas estén presentes en el archivo
        columnas_faltantes = [col for col in columnas_minimas[nombre_tabla] if col not in df.columns]
        if columnas_faltantes:
            raise ValueError(f"El archivo '{nombre_tabla}' no tiene las siguientes columnas mínimas necesarias: {', '.join(columnas_faltantes)}")

        dataframes.append(df)
    
    return dataframes  # Devolvemos lista de DataFrames
