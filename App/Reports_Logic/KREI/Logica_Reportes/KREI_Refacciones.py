#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import numpy as np
import pandas as pd
from ...globalModulesShare.WebScraping import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class RefaccionesKWESTEKREI(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()
        self.fecha_final = Variables().date_movement_config_document().strftime('%d/%m/%Y')
        self.fecha_inicial = Variables().date_movement_config_document().replace(day=1).strftime('%d/%m/%Y')
        self.dolares = Web_scraping().obtener_dolares(self.fecha_inicial, self.fecha_final)

    def RefaccionesKWESTE_KREI(self):
        self.nombre_doc = 'REKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        # NOTE Leer el archivo
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # NOTE  ELIMINAMOS LAS COLUMNAS NECESARIAS
        df.drop(['% Margen', 'Meta Ventas Por Vendedor', 'Meta Margen Por Vendedor', 'Meta Cantidad Por Vendedor', 'Meta Ventas Por Sucursal', 'Meta Margen Por Sucursal', 'Meta Cantidad Por Sucursal', '% Comisión Por Margen', '% Comisión Por Ventas', 'Comisión Por Margen', 'Comisión Por Ventas', 'EsBonificacion', 'IdUsuario', 'IdPaquete', 'Paquete', 'Descripción Paquete', 'Cantidad Paquete', 'Subtotal Paquete', 'Potencial Total', 'Tipo de Cambio del día', 'OCCliente', '% Margen Sin Descuento'], axis=1, inplace=True)
        # NOTE SELECCIONAMOS LAS COLUMNAS CON LAS CUALES TRABAJAR
        df_nuevo = df[df.columns[0:93]].copy()

        df_nuevo.insert(0,"Concesionario","KW ESTE", allow_duplicates=False)
        for column_name in df_nuevo.columns:
                if "fecha" in column_name.lower():
                    df_nuevo = self.variables.global_date_format_america(df_nuevo, column_name)
                    df_nuevo = self.variables.global_date_format_dmy_mexican(df_nuevo, column_name)
                else:
                    pass
        
        df_con_dolares = df_nuevo.merge(self.dolares, on='Fecha', how='left')
        df_con_dolares["Subtotal Dolares"] = np.divide(df_con_dolares['Subtotal'], df_con_dolares['Valor'])
        df_con_dolares["Margen Dolares"] = np.divide(df_con_dolares['Margen'], df_con_dolares['Valor'])
        df_con_dolares = df_con_dolares.rename(columns = {'Valor' : 'Valor Dólar'})

        columnas_bol=df_con_dolares.select_dtypes(include=bool).columns.tolist()

        df_con_dolares[columnas_bol] = df_con_dolares[columnas_bol].astype(str)
        

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df_con_dolares, self.concesionario)


    def RefaccionesKWSUR_KREI(self):
        self.nombre_doc = 'RSKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        # NOTE Leer el archivo
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # NOTE  ELIMINAMOS LAS COLUMNAS NECESARIAS
        df.drop(['% Margen', 'Meta Ventas Por Vendedor', 'Meta Margen Por Vendedor', 'Meta Cantidad Por Vendedor', 'Meta Ventas Por Sucursal', 'Meta Margen Por Sucursal', 'Meta Cantidad Por Sucursal', '% Comisión Por Margen', '% Comisión Por Ventas', 'Comisión Por Margen', 'Comisión Por Ventas', 'EsBonificacion', 'IdUsuario', 'IdPaquete', 'Paquete', 'Descripción Paquete', 'Cantidad Paquete', 'Subtotal Paquete', 'Potencial Total', 'Tipo de Cambio del día', 'OCCliente', '% Margen Sin Descuento'], axis=1, inplace=True)
        # NOTE SELECCIONAMOS LAS COLUMNAS CON LAS CUALES TRABAJAR
        df_nuevo = df[df.columns[0:93]].copy()

        df_nuevo.insert(0,"Concesionario","KW SUR", allow_duplicates=False)

        for column_name in df_nuevo.columns:
                if "fecha" in column_name.lower():
                    df_nuevo = self.variables.global_date_format_america(df_nuevo, column_name)
                    df_nuevo = self.variables.global_date_format_dmy_mexican(df_nuevo, column_name)
                else:
                    pass

        df_con_dolares = df_nuevo.merge(self.dolares, on='Fecha', how='left')
        df_con_dolares["Subtotal Dolares"] = np.divide(df_con_dolares['Subtotal'], df_con_dolares['Valor'])
        df_con_dolares["Margen Dolares"] = np.divide(df_con_dolares['Margen'], df_con_dolares['Valor'])
        df_con_dolares = df_con_dolares.rename(columns = {'Valor' : 'Valor Dólar'})
                
        columnas_bol=df_con_dolares.select_dtypes(include=bool).columns.tolist()
        df_con_dolares[columnas_bol] = df_con_dolares[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df_con_dolares, self.concesionario)