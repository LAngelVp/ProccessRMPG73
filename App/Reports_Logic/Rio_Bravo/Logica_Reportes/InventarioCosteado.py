#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from .Variables.ContenedorVariables import Variables
class InventarioCosteado(Variables):
    def Inventario_Costeado_KWRB(self):
        #obtenemos el archivo
        path = os.path.join(Variables().ruta_Trabajo,'ICR.xlsx')
        #leer el documento con pandas
        df = pd.read_excel(path, sheet_name="Hoja2")
        #reemplazar el ";" de los registros que lo contengan por un "-"
        df = df.replace(to_replace=";", value="-", regex=True)
        #--------------------------------------------------------------
        # INVENTARIO COSTEADO
        #---------------------------------------------------------------
        #obtener solo las celdas que vamos a trabajar.
        df2 = df[df.columns[0:33]].copy()
        #insertar la columna de fecha actual, con el fin de sacar la antiguedad.
        df2.insert(loc=28,column="Fecha_Hoy",value=Variables().fechaInsertar, allow_duplicates=False)
        #iterar en las cabeceras del dataframe para obtener las columnas de fecha.
        for column_title in df2:
            if ("Fecha" in column_title):
                try:
                    df[column_title] = pd.to_datetime(df[column_title], errors="coerce")
                except:
                    pass
            else:
                pass
        #crear la columna que contendra el valor de la antiguedad.
        Antiguedad = df2["Fecha_Hoy"] - df2["Fecha Entrada"]    #variable de la operacion.
        df2.insert(loc=29,column="Antigüedad",value=Antiguedad,allow_duplicates=False)
        #convertir la columna deantiguedad en numero.
        df2["Antigüedad"] = pd.to_numeric(df2["Antigüedad"].dt.days,downcast="integer")
        #ordenar el dataframe de manera descendente conforme a la columna de antiguedad.
        df2 = df2.sort_values(by=["Antigüedad"],ascending=True)
        #crear la columna de ClasDias.
        df2["ClasDias"] = ""
        #iterar sobre la columna de antiguedad, con la finalidad de remplazar los negativos por 0.
        for index, valor in df2["Antigüedad"].items(): 
            if (valor < 0):
                try:
                    df2.loc[index,"Antigüedad"] = 0
                except:
                    pass
            else:
                pass
        #clasificar ls registros conforme a su antiguedad.
        #Creamos la funcion para encapsular el procedimiento.
        def ClasDias(valor):
            if (valor >= 0 and valor <= 90):
                return "1 a 90"
            elif (valor >= 91 and valor <= 180):
                return "91 a 180"
            elif (valor >= 181 and valor <= 270):
                return "181 a 270"
            elif (valor >= 271 and valor <= 360):
                return "271 a 360"
            elif (valor >= 361):
                return "Mas de 360"
            else:
                pass
        #mandar a llamar la funcion dentro de una consulta.
        df2["ClasDias"] = df2["Antigüedad"].apply(lambda x:ClasDias(x))
        #cambiamos el formato de la columna de la "Fecha Entrada".
        for i in df2:
            try:
                if ("Fecha Entrada" in i):
                    df2[i] = df2[i].dt.strftime("%m/%d/%Y")
                elif ("Fecha" in i and "Fecha Entrada" not in i):
                    df2[i] = df2[i].dt.strftime("%d/%m/%Y")
                else:
                    pass
            except:
                pass
        #eliminar las columnas no necesarias.
        df2.drop(["Fecha_Hoy"], axis=1, inplace=True)
        #mandar el dataframe a una variable.
        df_inventarioCosteado = df2.copy()

        columnas_bol=df_inventarioCosteado.select_dtypes(include=bool).columns.tolist()
        df_inventarioCosteado[columnas_bol] = df_inventarioCosteado[columnas_bol].astype(str)

        #exportamos el dataframe del inventario costeado.
        df_inventarioCosteado.to_excel(os.path.join(Variables().ruta_procesados,f'KWRB_InventarioCosteado_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)

        #--------------------------------------------------------------
        # INVENTARIO COSTEADO POR DIA
        #---------------------------------------------------------------
        #realizamos ahora el inventario costeado por dia.
        df_inventarioCosteadoxDia = df2.copy()
        #eliminar columnas que no se ocuparan.
        df_inventarioCosteadoxDia["Fecha Entrada"] = pd.to_datetime(df_inventarioCosteadoxDia["Fecha Entrada"], errors="coerce")
        df_inventarioCosteadoxDia["Fecha Entrada"] = df_inventarioCosteadoxDia["Fecha Entrada"].dt.strftime("%d/%m/%Y")
        df_inventarioCosteadoxDia.drop(["Antigüedad","ClasDias"],axis=1,inplace=True)
        df_inventarioCosteadoxDia["Fecha_Dias"] = Variables().fechaInsertar
        df_inventarioCosteadoxDia["ClasSF"] = "Almacen"
        #realizar la clasificacion por "TipoDocumento"
        def ClasSF_TipoDocumento(valor_TipoDocumento,valor_almacen):
            if (valor_TipoDocumento == "Inventario"):
                return "Inventario"
            elif (valor_TipoDocumento == "Requisiciones"):
                return "Requisiciones"
            elif (valor_TipoDocumento == "Salidas en Vale"):
                return "Salidas en Vale"
            elif (valor_TipoDocumento == "Traspaso de Entrada" or valor == "Traspaso de Salida"):
                return "Traspaso"
            elif (valor_TipoDocumento == "Venta"):
                return "Venta"
            else:
                return valor_almacen
        #mandar a llamar a la clasificacion por tipoDocumento.
        df_inventarioCosteadoxDia["ClasSF"] = df_inventarioCosteadoxDia.apply(lambda fila:ClasSF_TipoDocumento(fila["TipoDocumento"], fila["ClasSF"]),axis=1)

        #clasificar por Almacen.
        def ClasSF_Almacen(valor_almacen, valor_clasSF):
            if ("Consigna" in valor_almacen):
                return "Consignas"
            elif ("Rescates" in valor_almacen or "Rescate" in valor_almacen):
                return "Rescates"
            else:
                return valor_clasSF
        #mandamos a llamar a la clasificacion por Almacen.
        df_inventarioCosteadoxDia["ClasSF"] = df_inventarioCosteadoxDia.apply(lambda fila:ClasSF_Almacen(fila["Almacén"], fila["ClasSF"]),axis=1)

        #convertir la fecha a formato "dia/mes/año"
        df_inventarioCosteadoxDia["Fecha_Dias"] = pd.to_datetime(df_inventarioCosteadoxDia["Fecha_Dias"], errors="coerce")
        df_inventarioCosteadoxDia["Fecha_Dias"] = df_inventarioCosteadoxDia["Fecha_Dias"].dt.strftime("%m/%d/%Y")

        #comment creamos la columna de mes
        df_inventarioCosteadoxDia["Mes"] = Variables().nombre_mes_actual_abreviado()

        columnas_bol=df_inventarioCosteadoxDia.select_dtypes(include=bool).columns.tolist()
        df_inventarioCosteadoxDia[columnas_bol] = df_inventarioCosteadoxDia[columnas_bol].astype(str)

        df_inventarioCosteadoxDia.to_excel(os.path.join(Variables().ruta_procesados,f'KWRB_InventarioCosteadoPorDia_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)