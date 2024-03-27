#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# importamos librerias.
import os
import pandas as pd
from datetime import *
from .Variables.ContenedorVariables import Variables
class Compras(Variables):
    def __init__(self):
        super().__init__()
        # obtenemos la ruta del documento.
        # leemos el archivo.
        self.nombre_doc = 'CDS.xlsx'
        path = os.path.join(Variables().ruta_Trabajo,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # copiamos el data original.
        df2 = df.copy()
        # cambiamos el nombre de las columnas con las que
        # vamos a realizar las operaciones.
        df2.rename(columns={ 'Fecha Docto.': 'FD', 'Fecha Captura':'FC'}, inplace=True)
        # insertamos la columna del dia actual.
        # dentro de la funcion, en el valor, le estamos diciendo a python que inserte la variable de fecha,
        # pero formateada en dia,mes, año.
        df2.insert(
            loc = 5,
            column = "Hoy",
            value = Variables().date_movement_config_document(),
            allow_duplicates = False
        )
        # formateamos las columnas de fecha a trabajar, para poder hacer operaciones 
        df2['FD'] = pd.to_datetime(df2.FD, format='%d/%m/%Y')
        df2['FC'] = pd.to_datetime(df2.FC, format='%d/%m/%Y')
        df2['Hoy'] = pd.to_datetime(df2.Hoy, format='%d/%m/%Y')
        # insertamos la columna de antigüedad, con la resta del 
        # fecha factura - fecha documento.
        df2.insert(
            loc = 6,
            column = 'Antigüedad',
            value = df2['FC'] - df2['FD'],
            allow_duplicates = False
        )
        # insertamos la columna de "Antigüedad Factura", con la resta,
        # fecha actual - fecha documento
        df2.insert(
            loc = 7,
            column = 'Antigüedad Fact',
            value = df2['Hoy'] - df2['FD'],
            allow_duplicates = False
        )
        

        # procedemos a formatear la columna de antigüedad a tipo Entero,
        # con el objetivo de poder condicionar la iteracion de la columna,
        # como se muestra en el bucle [1] de la funcion "Antiguedad".
        df2['Antigüedad'] = pd.to_numeric(df2['Antigüedad'].dt.days, downcast='integer')
        df2['Antigüedad Fact'] = pd.to_numeric(df2['Antigüedad Fact'].dt.days, downcast='integer')

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
            
        df2["Mes"] = df2["FD"].apply(lambda x:Variables().nombre_mes_base_columna_month_year(x))
        
        df2.rename(columns={ 'FD':'Fecha Docto.', 'FC':'Fecha Captura'}, inplace=True)
        

        df2.drop(['Folio','Hoy'], axis=1, inplace=True)
        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        self.columnas_fecha = df2.select_dtypes(include=['datetime64']).columns
        # formatear las columnas de fecha para trabajar con ellas.
        for column_title in self.columnas_fecha:
                try:
                    df2[column_title] = df2[column_title].dt.strftime('%d/%m/%Y')
                except:
                    pass

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        if (os.path.basename(Variables().comprobar_reporte_documento_rutas(self.nombre_doc)).split(".")[1] == self.nombre_doc.split(".")[1]):
            df2.to_excel(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), index=False )
        else:
            df2.to_csv(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), encoding="utf-8", index=False )
