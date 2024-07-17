#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# importamos librerias.
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
# clase del reporte a realizar
class Compras(Variables):
    def __init__(self):
        super().__init__()
        self.variables = Variables()
        self.concesionario = Concesionarios().concesionarioEste
        # obtenemos la ruta del documento.
        # leemos el archivo.
        self.nombre_doc = 'CDE.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)

        # copiamos el data original.
        df2 = df.copy()
        
        # cambiamos el nombre de las columnas con las que
        # vamos a realizar las operaciones.
        df2["Fecha_Hoy"] =  self.variables.date_movement_config_document()

        # formateamos las columnas de fecha a trabajar, para poder hacer operaciones 
        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_america(df2, column_name)
            else:
                pass

        antiguedad = (df2['Fecha Captura'] - df2['Fecha Docto.'])


        antiguedad_factura = (df2['Fecha_Hoy'] - df2['Fecha Docto.'])


        df2.insert(
            loc = 5,
            column = 'Antigüedad',
            value = antiguedad,
            allow_duplicates = False
        )
        # insertamos la columna de "Antigüedad Factura", con la resta,
        # fecha actual - fecha documento
        df2.insert(
            loc = 6,
            column = 'Antigüedad Fact',
            value = antiguedad_factura,
            allow_duplicates = False
        )

        df2["Antigüedad"] = pd.to_timedelta(df2["Antigüedad"])
        df2["Antigüedad"] = df2["Antigüedad"].dt.days

        df2["Antigüedad Fact"] = pd.to_timedelta(df2["Antigüedad Fact"])
        df2["Antigüedad Fact"] = df2["Antigüedad Fact"].dt.days

        df2["Antigüedad"] = df2["Antigüedad"].apply(self.convertir_a_cero)

        df2["Antigüedad Fact"] = df2["Antigüedad Fact"].apply(self.convertir_a_cero)

        df2["Mes"] = df2["Fecha Docto."].apply(lambda x:self.variables.nombre_mes_base_columna(x))


        df2.drop(['Folio','Fecha_Hoy'], axis=1, inplace=True)
        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)
    
        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_mdy_america(df2, column_name)
            else:
                pass
        
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)
    
    def convertir_a_cero(self, valor):
        if valor < 0:
            return 0
        else:
            return valor