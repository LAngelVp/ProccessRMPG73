#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class InventarioKWESTEKREI(Variables):

    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()

    def InventarioKWESTE_KREI(self):
        #obtenemos el archivo
        self.nombre_doc = 'ICEKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei,self.nombre_doc)
        #leer el documento con pandas
        df = pd.read_excel(path, sheet_name="Hoja2")
        #reemplazar el ";" de los registros que lo contengan por un "-"
        df = df.replace(to_replace=";", value="-", regex=True)
        #obtener solo las celdas que vamos a trabajar.
        df2 = df[df.columns[0:33]].copy()

        df2.insert(0,"Concesionario","KW ESTE", allow_duplicates=False)

        for column_name in df2.columns:
                if "fecha" in column_name.lower():
                    df2 = self.variables.global_date_format_america(df2, column_name)
                else:
                    pass

        antiguedad = self.variables.date_movement_config_document() - df2["Fecha Entrada"]

        df2["Antigüedad"] =  antiguedad.dt.days


        for column_name in df2.columns:
                if "fecha" in column_name.lower():
                    df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
                else:
                    pass

        # columna del mes actual
        df2["Mes"] = self.variables.nombre_mes_actual_abreviado()

        df2["ClassAlmacen"] = "Inventario"

        df2.loc[df2["Almacén"].str.contains("Infant"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.contains("MX"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.contains("T380"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.contains("T680"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.contains("DAF"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.contains("KW45/55"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.contains("Servicio Express"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[(df2["Almacén"].str.contains("Rescates")) | 
                                     (df2["Almacén"].str.contains("Rescate")), "ClassAlmacen"] = "Inventario de Seguridad"


        df2.loc[(df2["Almacén"].str.contains("Consigna")) | 
                                     ( df2["Almacén"].str.contains("Consignas")), "ClassAlmacen"] = "Consigna"

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)
    
    def InventarioKWSUR_KREI(self):
        self.nombre_doc = 'ICSKREI.xlsx'
        #obtenemos el archivo
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        #leer el documento con pandas
        df = pd.read_excel(path, sheet_name="Hoja2")
        #reemplazar el ";" de los registros que lo contengan por un "-"
        df = df.replace(to_replace=";", value="-", regex=True)
        #obtener solo las celdas que vamos a trabajar.
        df2 = df[df.columns[0:33]].copy()

        df2.insert(0,"Concesionario","KW SUR", allow_duplicates=False)

        for column_name in df2.columns:
                if "fecha" in column_name.lower():
                    df2 = self.variables.global_date_format_america(df2, column_name)
                else:
                    pass

        antiguedad = self.variables.date_movement_config_document() - df2["Fecha Entrada"]

        df2["Antigüedad"] =  antiguedad.dt.days


        for column_name in df2.columns:
                if "fecha" in column_name.lower():
                    df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
                else:
                    pass
            
        # columna del mes actual
        df2["Mes"] = self.variables.nombre_mes_actual_abreviado()

        df2["ClassAlmacen"] = "Inventario"

        df2.loc[df2["Almacén"].str.contains("Infant"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.contains("T380"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.contains("T680"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.contains("DAF"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.contains("MX"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.contains("KW45/55"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.contains("Servicio Express"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[(df2["Almacén"].str.contains("Rescates")) | 
                                     (df2["Almacén"].str.contains("Rescate")), "ClassAlmacen"] = "Inventario de Seguridad"


        df2.loc[(df2["Almacén"].str.contains("Consigna")) | 
                                     ( df2["Almacén"].str.contains("Consignas")), "ClassAlmacen"] = "Consigna"

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)