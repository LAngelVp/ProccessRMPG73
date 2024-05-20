#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class Inventario(Variables):
    def __init__(self):
        self.variables = Variables()
        self.concesionario = Concesionarios().concesionarioEste
        self.m = self.variables.marcas_refacciones_fun()

        #obtenemos el archivo
        self.nombre_doc = 'ICE.xlsx'
        self.nombre_doc2 = 'ICDE.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
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
        df2.insert(loc=27,column="Fecha_Hoy",value=self.variables.date_movement_config_document(), allow_duplicates=False)
        #iterar en las cabeceras del dataframe para obtener las columnas de fecha.
        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_america(df2, column_name)
            else:
                pass
        #crear la columna que contendra el valor de la antiguedad.
        Antiguedad = (df2["Fecha_Hoy"] - df2["Fecha Entrada"]).apply(lambda x : x.days)  #variable de la operacion.

        df2.insert(loc=28,column="Antigüedad",value=Antiguedad,allow_duplicates=False)
        #convertir la columna deantiguedad en numero.
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
        
        #mandar a llamar la funcion dentro de una consulta.
        df2["ClasDias"] = df2["Antigüedad"].apply(lambda x:self.ClasDias(x))
        #cambiamos el formato de la columna de la "Fecha Entrada".
        for column_name in df2.columns:
            if "fecha entrada" in column_name.lower():
                df2 = self.variables.global_date_format_mdy_america(df2, column_name)
            elif "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)


        #eliminar las columnas no necesarias.
        df2.drop(["Fecha_Hoy"], axis=1, inplace=True)
        #mandar el dataframe a una variable.
        df_inventarioCosteado = df2.copy()
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df_inventarioCosteado, self.concesionario)

#         #--------------------------------------------------------------
#         # INVENTARIO COSTEADO POR DIA
#         #---------------------------------------------------------------
        #realizamos ahora el inventario costeado por dia.
        df_inventarioCosteadoxDia = df2.copy()
        #eliminar columnas que no se ocuparan.
        # df_inventarioCosteadoxDia["Fecha Entrada"] = pd.to_datetime(df_inventarioCosteadoxDia["Fecha Entrada"])
        df_inventarioCosteadoxDia= self.variables.global_date_format_america(df_inventarioCosteadoxDia, "Fecha Entrada")
        df_inventarioCosteadoxDia= self.variables.global_date_format_dmy_mexican(df_inventarioCosteadoxDia, "Fecha Entrada")
        
        # df_inventarioCosteadoxDia["Fecha Entrada"] = df_inventarioCosteadoxDia["Fecha Entrada"].dt.strftime("%d/%m/%Y")
        df_inventarioCosteadoxDia.drop(["ClasDias"],axis=1,inplace=True)
        df_inventarioCosteadoxDia["Fecha_Dias"] = self.variables.date_movement_config_document()
        df_inventarioCosteadoxDia["ClasSF"] = ""

        
        #mandar a llamar a la clasificacion por tipoDocumento.
        df_inventarioCosteadoxDia["ClasSF"] = df_inventarioCosteadoxDia.apply(lambda fila:self.ClasSF_TipoDocumento(fila["TipoDocumento"], fila["ClasSF"]),axis=1)

       
        #mandamos a llamar a la clasificacion por Almacen.
        df_inventarioCosteadoxDia["ClasSF"] = df_inventarioCosteadoxDia.apply(lambda fila:self.ClasSF_Almacen(fila["Almacén"],fila["TipoDocumento"], fila["ClasSF"]),axis=1)

        #creamoa la columna de marca
        df_inventarioCosteadoxDia["Marca"] = df_inventarioCosteadoxDia.apply(
            lambda fila: pd.Series(
                self.marca_inventario(
                    fila["Núm Artículo"], fila["Número Categoría"], fila["Categoría"]
                )
            ),
            axis=1,
        )
        #creamos la del mes
        df_inventarioCosteadoxDia["Mes"] = self.variables.nombre_mes_actual_abreviado()

        #convertir la fecha a formato "dia/mes/año"
        df_inventarioCosteadoxDia= self.variables.global_date_format_america(df_inventarioCosteadoxDia, "Fecha_Dias")

        df_inventarioCosteadoxDia= self.variables.global_date_format_mdy_america(df_inventarioCosteadoxDia, "Fecha_Dias")
        #comment : vamos a crear la columna de ClassAlmacen

        df_inventarioCosteadoxDia["ClassAlmacen"] = "Inventario"

        df_inventarioCosteadoxDia.insert(12, "ClassAlmacen", df_inventarioCosteadoxDia.pop("ClassAlmacen"))

        df_inventarioCosteadoxDia.loc[df_inventarioCosteadoxDia["Almacén"].str.contains("Infant"), "ClassAlmacen"] = "Infant Care"


        df_inventarioCosteadoxDia.loc[df_inventarioCosteadoxDia["Almacén"].str.contains("MX"), "ClassAlmacen"] = "MX"

        df_inventarioCosteadoxDia.loc[df_inventarioCosteadoxDia["Almacén"].str.contains("KW45/55"), "ClassAlmacen"] = "Inventario de Seguridad"

        df_inventarioCosteadoxDia.loc[df_inventarioCosteadoxDia["Almacén"].str.contains("Servicio Express"), "ClassAlmacen"] = "Servicio Express"

        df_inventarioCosteadoxDia.loc[(df_inventarioCosteadoxDia["Almacén"].str.contains("Rescates")) | 
                                     (df_inventarioCosteadoxDia["Almacén"].str.contains("Rescate")), "ClassAlmacen"] = "Rescates"


        df_inventarioCosteadoxDia.loc[(df_inventarioCosteadoxDia["Almacén"].str.contains("Consigna")) | 
                                     ( df_inventarioCosteadoxDia["Almacén"].str.contains("Consignas")), "ClassAlmacen"] = "Consigna"

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc2, df_inventarioCosteadoxDia, self.concesionario)

    # clasificar ls registros conforme a su antiguedad.
    # Creamos la funcion para encapsular el procedimiento.
    def ClasDias(self, valor):
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

    #realizar la clasificacion por "TipoDocumento"
    def ClasSF_TipoDocumento(self, valor_TipoDocumento,valor_almacen):
        if (valor_TipoDocumento.lower() == "inventario"):
            return "Almacen"
        elif (valor_TipoDocumento.lower() == "requisiciones"):
            return "Requisiciones"
        elif (valor_TipoDocumento.lower() == "salidas en vale"):
            return "Salidas en Vale"
        elif ((valor_TipoDocumento.lower() == "traspaso de entrada") | (valor_TipoDocumento.lower() == "traspaso de salida")):
            return "Traspaso"
        elif (valor_TipoDocumento.lower() == "venta"):
            return "Venta"
        else:
            return valor_almacen
    
     #clasificar por Almacen.
    def ClasSF_Almacen(self, valor_almacen,tipo_documento, valor_clasSF):
        if ("consigna" in valor_almacen.lower() and "inventario" in tipo_documento.lower()):
            return "Consignas"
        elif ("rescates" in valor_almacen.lower() or "rescate" in valor_almacen.lower() and "inventario" in tipo_documento.lower()):
            return "Rescates"
        elif ("infant" in valor_almacen.lower() or "infantCare" in valor_almacen.lower() and "inventario" in tipo_documento.lower()):
            return "InfantCare"
        elif ("mx" in valor_almacen.lower() and "inventario" in tipo_documento.lower()):
            return "Motor MX"
        elif ("servicio express" in valor_almacen.lower() and "inventario" in tipo_documento.lower()):
            return "Servicio Express"
        elif ("ultrashift" in valor_almacen.lower() and "inventario" in tipo_documento.lower()):
            return "Ultrashift"
        else:
            return valor_clasSF
#COMMENT_FUNCTION: FUNCION PARA LA CLASIFICACION DE LA MARCA DE LAS REFACCIONES
    def marca_inventario(self, numero_articulo, numero_categoria, categoria):
        for i, valor in self.m.iterrows():
            valor_articulo = valor["Número Artículo"]
            valor_num_categoria = valor["Número Categoría"]
            valor_categoria = valor["Ctegoria"]
            valor_marca = valor["Marca"]
            if (
                (str(numero_articulo) == str(valor_articulo))
                and (str(numero_categoria) == str(valor_num_categoria))
                and (str(categoria) == str(valor_categoria))
            ):
                return valor_marca
        return "SM"
    