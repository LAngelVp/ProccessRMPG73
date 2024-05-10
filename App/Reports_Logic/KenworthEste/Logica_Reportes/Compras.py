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

        # formateamos las columnas de fecha a trabajar, para poder hacer operaciones 
        for column_name in df2.columns:
            if "Fecha" in column_name:
                df2 = self.variables.global_date_format_america(df2, column_name)
            else:
                pass

        df2["Fecha_Hoy"] =  self.variables.date_movement_config_document()

        antiguedad = (df2['Fecha Captura'] - df2['Fecha Docto.']).apply(lambda x : x.days)
        antiguedad_factura = (df2['Fecha_Hoy'] - df2['Fecha Docto.']).apply(lambda x : x.days)

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
        for index, valor in df2["Antigüedad"].items():
            if (valor < 0):
                try:
                    df2.loc[index,"Antigüedad"] = 0
                except:
                    pass
            else:
                pass

        # creamos la columna de Mes al final del documento
        df2["Mes"] = df2["Fecha Docto."].apply(lambda x:self.variables.nombre_mes_base_columna(x))

        # devolver las columnas de tipo fecha al formato "dia,mes,año"
        # EXCEPTO...
        # Las columnas de "fecha documento y fecha factura",
        # su formato debe de ser "mes,dia,año"
        for column_name in df2.columns:
            if "Fecha" in column_name:
                df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
            else:
                pass

        df2.drop(['Folio','Fecha_Hoy'], axis=1, inplace=True)
        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)
    
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)