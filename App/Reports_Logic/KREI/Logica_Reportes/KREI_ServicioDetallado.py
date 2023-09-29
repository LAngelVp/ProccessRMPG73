#########################
# DESARROLLADOR
# LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from .Variables.ContenedorVariables import Variables
class ServicioDetalladoKWESTEKREI(Variables):
    def ServicioDetalladoKWESTE_KREI(self):
        path = os.path.join(Variables().ruta_Trabajo,"SDEKREI.xlsx")
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)

        # # NOTE Cambiamos el titulo de la columna.
        df = df.rename(columns={'Número Orden':'NO','Unidad':'U'})

        df.insert(
                loc = 1,
                column = 'Columna_Fantasma1',
                value = "",
                allow_duplicates = False
            )
        
        df["Columna_Fantasma2"] = ""
        df["Fecha_Movimiento"] = Variables().fechaInsertar
        # NOTE Creamos la columna con la fecha actual
        
        df.insert(
            loc = 18,
            column = "Número Orden",
            value = 'OS' + df['NO'].map(str).str.split('.').str[0],
            allow_duplicates = False
        )
        df.insert(
            loc = 21,
            column = 'Unidad',
            value = 'UN-' + df['U'].map(str).str.split('.').str[0],
            allow_duplicates = False
        )
        df.drop(['Hora Docto.','NO','U','Fecha Cancelación','Fecha Inicio Garantía','Fecha Fin Garantía','Categoría','Id. Paquete','Paquete','Descripción Paquete','Cantidad Paquete','Saldo'], axis=1, inplace=True)

        # NOTE INTENTAMOS HACER LOS CAMBIOS DE FORMATO PARA LAS FECHAS EN PYTHON
        for column_title in df:
            if ('Fecha' in column_title):
                try:
                    df[column_title] = (df[column_title].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        df.to_excel(os.path.join(Variables().ruta_procesados,f'SERV_KWESTE_KREI_SDR_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)
    def ServicioDetalladoKWSUR_KREI(self):
        path = os.path.join(Variables().ruta_Trabajo,"SDSKREI.xlsx")
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)

        
        # # NOTE Cambiamos el titulo de la columna.
        df = df.rename(columns={'Número Orden':'NO','Unidad':'U'})

        df.insert(
                loc = 1,
                column = 'Columna_Fantasma1',
                value = "",
                allow_duplicates = False
            )
        
        df["Columna_Fantasma2"] = ""
        df["Fecha_Movimiento"] = Variables().fechaInsertar
        # NOTE Creamos la columna con la fecha actual
        
        df.insert(
            loc = 18,
            column = "Número Orden",
            value = 'OS' + df['NO'].map(str).str.split('.').str[0],
            allow_duplicates = False
        )
        df.insert(
            loc = 21,
            column = 'Unidad',
            value = 'UN-' + df['U'].map(str).str.split('.').str[0],
            allow_duplicates = False
        )
        df.drop(['Hora Docto.','NO','U','Fecha Cancelación','Fecha Inicio Garantía','Fecha Fin Garantía','Categoría','Id. Paquete','Paquete','Descripción Paquete','Cantidad Paquete','Saldo'], axis=1, inplace=True)

        # NOTE INTENTAMOS HACER LOS CAMBIOS DE FORMATO PARA LAS FECHAS EN PYTHON
        for column_title in df:
            if ('Fecha' in column_title):
                try:
                    df[column_title] = (df[column_title].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        df.to_excel(os.path.join(Variables().ruta_procesados,f'SERV_KWSUR_KREI_SDR_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)