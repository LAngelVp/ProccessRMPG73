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
        super().__init__()
        # obtenemos la ruta del documento.
        # leemos el archivo.
        self.nombre_doc = 'CDS.xlsx'
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()

        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # copiamos el data original.
        df2 = df.copy()
        # cambiamos el nombre de las columnas con las que
        # vamos a realizar las operaciones.
        # insertamos la columna del dia actual.
        # dentro de la funcion, en el valor, le estamos diciendo a python que inserte la variable de fecha,
        # pero formateada en dia,mes, año.

        for column_name in df2.columns:
            if "Fecha" in column_name:
                df2 = self.variables.global_date_format_america(df2, column_name)
            else:
                pass
        df2["Fecha_Hoy"] =  self.variables.date_movement_config_document()

        antiguedad = (df2['Fecha Captura'] - df2['Fecha Docto.']).apply(lambda x : x.days)
        antiguedad_factura = (df2['Fecha_Hoy'] - df2['Fecha Docto.']).apply(lambda x : x.days)
        # insertamos la columna de antigüedad, con la resta del 
        # fecha factura - fecha documento.
        df2.insert(
            loc = 6,
            column = 'Antigüedad',
            value = antiguedad,
            allow_duplicates = False
        )
        # insertamos la columna de "Antigüedad Factura", con la resta,
        # fecha actual - fecha documento
        df2.insert(
            loc = 7,
            column = 'Antigüedad Fact',
            value = antiguedad_factura,
            allow_duplicates = False
        )
        

        # procedemos a formatear la columna de antigüedad a tipo Entero,
        # con el objetivo de poder condicionar la iteracion de la columna,
        # como se muestra en el bucle [1] de la funcion "Antiguedad".

        # Bucle [1].
        # En esta funcion iteramos toda la columna de "Antigüedad",
        # aplicando una condicion.
        # SI, el contenido es menos a 0, remplazara dicho contenido por un 0.
        # SI NO, ignorará el contenido y continuara su ciclo. 
        for column in df2['Antigüedad']:
            if (column < (0)):
                df2['Antigüedad'] = df2['Antigüedad'].replace(column,0)
            else:
                pass
        # devolvemos al nombre original.
            
        df2["Mes"] = df2["Fecha Docto."].apply(lambda x:self.variables.nombre_mes_base_columna_month_year(x))
        
        

        df2.drop(['Folio','Fecha_Hoy'], axis=1, inplace=True)
        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # formatear las columnas de fecha para trabajar con ellas.
        for column_name in df2.columns:
            if "Fecha" in column_name:
                df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
            else:
                pass

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)
