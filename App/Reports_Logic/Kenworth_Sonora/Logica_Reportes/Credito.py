#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class Credito(Variables):
    def __init__(self):
        super().__init__()
        # obtenemos el path del archivo
        self.nombre_doc = 'CS.xlsx'
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()

        path =  os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        # leer el documento.
        df = pd.read_excel(path, sheet_name="Hoja2")
        # obtenemos las columnas que se van a utilizar
        df2 = df[df.columns[0:52]].copy()
        df2 = df2.replace(to_replace = ";", value = "_", regex = True)
        # remplazamos los espacios en los titulos por cuestiones de normatividad
        df2.columns = df2.columns.str.replace(" ", "_")
        # creacion de la columna de clasificacion
        df2.insert(loc=2,column="Clasificacion",value="CLIENTES GENERALES", allow_duplicates = False)
        # array de lo que no queremos filtrar
        array_excepto_clientes = ["KENWORTH","PACCAR PARTS MEXICO", "PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA", "DISTRIBUIDORA MEGAMAK", "SEGUROS", "SEGURO", "GRUPO NACIONAL PROVINCIAL"]
        # Clasificacion
        df2.loc[df2["Cliente"].str.contains("KENWORTH") & ~df2["Cliente"].str.contains("KENWORTH MEXICANA"), "Clasificacion"] = "CONCESIONARIOS"
        df2.loc[df2["Cliente"] == "KENWORTH MEXICANA", "Clasificacion"] = "KENMEX"
        df2.loc[df2["Cliente"] == "PACCAR PARTS MEXICO", "Clasificacion"] = "PACCAR PARTS"
        df2.loc[df2["Cliente"] == "DISTRIBUIDORA MEGAMAK", "Clasificacion"] = "MEGAMAK"
        df2.loc[(df2["Cliente"] == "PACCAR FINANCIAL MEXICO") | (df2["Cliente"] == "PACLEASE MEXICANA"), "Clasificacion"] = "PLM"
        df2.loc[(df2["Cliente"].str.contains('SEGUROS')) | (df2["Cliente"].str.contains('SEGURO')) | (df2["Cliente"] == 'GRUPO NACIONAL PROVINCIAL'), "Clasificacion" ]= "SEGUROS"
        df2.loc[~df2["Cliente"].str.contains("|".join(array_excepto_clientes)), "Clasificacion"] = "CLIENTES GENERALES"
        # ponemos todas las columnas de fecha en formato fecha
        for i in df2:
            if ("fecha" in i.lower()):
                try:
                    df2[i] = pd.to_datetime(df2[i], errors = "coerce")
                except:
                    pass

        # CREAMOS LA COLUMNA DE SEMANA
        valor_loc = 1
        for columna in df2:
            if ("fecha_vencimiento" == columna.lower()):
                df2.insert(loc=valor_loc, column="Semana", value = "S-" + (df2["Fecha_Vencimiento"].dt.isocalendar().week).map(str), allow_duplicates=False)
            valor_loc +=1

        # FORMATEAMOS LAS COLUMNAS DE FECHA
        for i in df2:
            if ("fecha" in i.lower()):
                try:
                    df2[i] = df2[i].dt.strftime("%d/%m/%Y")
                except:
                    pass

        # egresamos el titulo de las columnas a su formato original
        df2.columns = df2.columns.str.replace("_", " ")

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)


        self.nombre_doc = 'CSG.xlsx'
        CreditoGlobal = df2.copy()
        CreditoGlobal.drop(["Clasificacion","Semana"], axis=1, inplace=True)
        CreditoGlobal["Mes"] = self.variables.nombre_mes_actual_abreviado()

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, CreditoGlobal, self.concesionario)
