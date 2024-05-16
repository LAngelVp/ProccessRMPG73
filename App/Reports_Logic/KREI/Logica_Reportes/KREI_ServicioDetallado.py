#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class ServicioDetalladoKWESTEKREI(Variables):

    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()

    def ServicioDetalladoKWESTE_KREI(self):
        self.nombre_doc = "SDEKREI.xlsx"
        path = os.path.join(self.variables.ruta_Trabajos_krei,self.nombre_doc)
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
        df["Fecha_Movimiento"] = self.variables.date_movement_config_document()
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
        df.drop(['Hora Docto.','NO','U','Fecha Cancelación','Fecha Inicio Garantía','Fecha Fin Garantía','Id. Paquete','Paquete','Descripción Paquete','Cantidad Paquete',"Subtotal Paquete",'Saldo'], axis=1, inplace=True)

        # NOTE INTENTAMOS HACER LOS CAMBIOS DE FORMATO PARA LAS FECHAS EN PYTHON
        for column_name in df.columns:
                if "fecha" in column_name.lower():
                    df = self.variables.global_date_format_america(df, column_name)
                    df = self.variables.global_date_format_dmy_mexican(df, column_name)
                else:
                    pass
        
        df.insert(0,"Concesionario", "ESTE", allow_duplicates=False)

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)

    def ServicioDetalladoKWSUR_KREI(self):
        self.nombre_doc = "SDSKREI.xlsx"
        path = os.path.join(self.variables.ruta_Trabajos_krei,self.nombre_doc)
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
        df["Fecha_Movimiento"] = self.variables.date_movement_config_document()
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
        df.drop(['Hora Docto.','NO','U','Fecha Cancelación','Fecha Inicio Garantía','Fecha Fin Garantía','Id. Paquete','Paquete','Descripción Paquete','Cantidad Paquete',"Subtotal Paquete",'Saldo'], axis=1, inplace=True)

        # NOTE INTENTAMOS HACER LOS CAMBIOS DE FORMATO PARA LAS FECHAS EN PYTHON
        for column_name in df.columns:
                if "fecha" in column_name.lower():
                    df = self.variables.global_date_format_america(df, column_name)
                    df = self.variables.global_date_format_dmy_mexican(df, column_name)
                else:
                    pass

        df.insert(0,"Concesionario", "SUR", allow_duplicates=False)

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)
