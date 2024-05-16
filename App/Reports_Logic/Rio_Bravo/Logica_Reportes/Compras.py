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
class Compras(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()
        # obtenemos la ruta del documento.
        # leemos el archivo.
        self.nombre_doc = 'CDR.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwrb, self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # copiamos el data original.
        df2 = df.copy()
        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_america(df2, column_name)
            else:
                pass
        # insertamos la columna del dia actual.
        # dentro de la funcion, en el valor, le estamos diciendo a python que inserte la variable de fecha,
        # pero formateada en dia,mes, año.

        df2.insert(
            loc = 6,
            column = "Fecha_Hoy",
            value = self.variables.date_movement_config_document(),
            allow_duplicates = False
        )
        antiguedad = (df2['Fecha Captura'] - df2['Fecha Docto.']).apply(lambda x : x.days)
        antiguedad_factura = (df2['Fecha_Hoy'] - df2['Fecha Docto.']).apply(lambda x : x.days)
        # insertamos la columna de antigüedad, con la resta del 
        # fecha factura - fecha documento.
        df2.insert(
            loc = 7,
            column = 'Antigüedad',
            value = antiguedad,
            allow_duplicates = False
        )
        # insertamos la columna de "Antigüedad Factura", con la resta,
        # fecha actual - fecha documento
        df2.insert(
            loc = 8,
            column = 'Antigüedad Fact',
            value = antiguedad_factura,
            allow_duplicates = False
        )


        # Bucle [1].
        # En esta funcion iteramos toda la columna de "Antigüedad",
        # aplicando una condicion.
        # SI, el contenido es menos a 0, remplazara dicho contenido por un 0.
        # SI NO, ignorará el contenido y continuara su ciclo. 
        for index, valor in df2["Antigüedad"].items():
            if (valor < 0):
                try:
                    df2.loc[index,"Antigüedad"] = 0
                except:
                    pass
            else:
                pass

        # devolver las columnas de tipo fecha al formato "dia,mes,año"
        # EXCEPTO...
        # Las columnas de "fecha documento y fecha factura",
        # su formato debe de ser "mes,dia,año"
        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
            else:
                pass
        df2.drop(['Folio','Fecha_Hoy'], axis=1, inplace=True)
        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)
        