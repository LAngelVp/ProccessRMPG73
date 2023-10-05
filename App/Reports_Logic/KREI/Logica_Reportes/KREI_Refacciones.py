#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from .Variables.ContenedorVariables import Variables
class RefaccionesKWESTEKREI(Variables):
    def RefaccionesKWESTE_KREI(self):
        path = os.path.join(Variables().ruta_Trabajo,'REKREI.xlsx')
        # NOTE Leer el archivo
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # NOTE  ELIMINAMOS LAS COLUMNAS NECESARIAS
        df.drop(['% Margen', 'Meta Ventas Por Vendedor', 'Meta Margen Por Vendedor', 'Meta Cantidad Por Vendedor', 'Meta Ventas Por Sucursal', 'Meta Margen Por Sucursal', 'Meta Cantidad Por Sucursal', '% Comisión Por Margen', '% Comisión Por Ventas', 'Comisión Por Margen', 'Comisión Por Ventas', 'EsBonificacion', 'IdUsuario', 'IdPaquete', 'Paquete', 'Descripción Paquete', 'Cantidad Paquete', 'Subtotal Paquete', 'Potencial Total', 'Tipo de Cambio del día', 'OCCliente', '% Margen Sin Descuento'], axis=1, inplace=True)
        # NOTE SELECCIONAMOS LAS COLUMNAS CON LAS CUALES TRABAJAR
        df_nuevo = df[df.columns[0:93]].copy()

        df_nuevo.insert(0,"Concesionario","KW ESTE", allow_duplicates=False)

        for i in df_nuevo:
            if ("fecha" in i.lower()):
                try:
                    df_nuevo[i] = pd.to_datetime(df_nuevo[i], errors = "coerce")
                except:
                    pass
        for i in df_nuevo:
            if ("fecha" in i.lower()):
                try:
                    df_nuevo[i] = df_nuevo[i].dt.strftime("%d/%m/%Y")
                except:
                    pass
        columnas_bol=df_nuevo.select_dtypes(include=bool).columns.tolist()
        df_nuevo[columnas_bol] = df_nuevo[columnas_bol].astype(str)

        df_nuevo.to_excel(os.path.join(Variables().ruta_procesados,f'KREI_Refacciones_KWESTE_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)
    def RefaccionesKWSUR_KREI(self):
        path = os.path.join(Variables().ruta_Trabajo,'RSKREI.xlsx')
        # NOTE Leer el archivo
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # NOTE  ELIMINAMOS LAS COLUMNAS NECESARIAS
        df.drop(['% Margen', 'Meta Ventas Por Vendedor', 'Meta Margen Por Vendedor', 'Meta Cantidad Por Vendedor', 'Meta Ventas Por Sucursal', 'Meta Margen Por Sucursal', 'Meta Cantidad Por Sucursal', '% Comisión Por Margen', '% Comisión Por Ventas', 'Comisión Por Margen', 'Comisión Por Ventas', 'EsBonificacion', 'IdUsuario', 'IdPaquete', 'Paquete', 'Descripción Paquete', 'Cantidad Paquete', 'Subtotal Paquete', 'Potencial Total', 'Tipo de Cambio del día', 'OCCliente', '% Margen Sin Descuento'], axis=1, inplace=True)
        # NOTE SELECCIONAMOS LAS COLUMNAS CON LAS CUALES TRABAJAR
        df_nuevo = df[df.columns[0:93]].copy()

        df_nuevo.insert(0,"Concesionario","KW SUR", allow_duplicates=False)

        for i in df_nuevo:
            if ("fecha" in i.lower()):
                try:
                    df_nuevo[i] = pd.to_datetime(df_nuevo[i], errors = "coerce")
                except:
                    pass
        for i in df_nuevo:
            if ("fecha" in i.lower()):
                try:
                    df_nuevo[i] = df_nuevo[i].dt.strftime("%d/%m/%Y")
                except:
                    pass
        columnas_bol=df_nuevo.select_dtypes(include=bool).columns.tolist()
        df_nuevo[columnas_bol] = df_nuevo[columnas_bol].astype(str)

        df_nuevo.to_excel(os.path.join(Variables().ruta_procesados,f'KREI_Refacciones_KWSUR_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)