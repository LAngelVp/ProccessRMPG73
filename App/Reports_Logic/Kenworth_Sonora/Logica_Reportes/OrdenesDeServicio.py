#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
from decimal import Decimal
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import pandas as pd
from datetime import *
import numpy as np
from .Variables.ContenedorVariables import Variables
class OrdenesDeServicio(Variables):
    def __init__(self):
        super().__init__()
        path = os.path.join(Variables().ruta_Trabajo,'OSS.xlsx')
        
        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(' ', '_')
        df2 = df.copy()

        # ESTOS ARRAYS SON DE APOYO PARA LA CLASIFICACION DE LOS CLIENTES
        array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]

        # CREAMOS LA COLUMNA DE CLASIFICACION CLIENTE
        df2.insert(loc=5,column="Clasificacion_Cliente",value="CLIENTES GENERALES", allow_duplicates = False)

        #CLASIFICACION DEL CLIENTE (NORMAL)
        df2.loc[df2["Cliente"].str.contains("KENWORTH") & ~df2["Cliente"].str.contains("KENWORTH MEXICANA") & ~df2["Cliente"].str.contains("KENWORTH DISTRIBUIDORA DE SONORA"), "Clasificacion_Cliente"] = "CONCESIONARIOS"
        df2.loc[df2["Cliente"].str.contains("|".join(array_Garantia)),"Clasificacion_Cliente"] = "GARANTIA"
        df2.loc[df2["Cliente"].str.contains("|".join(array_PLM)),"Clasificacion_Cliente"] = "PLM"
        df2.loc[df2["Cliente"] == "KENWORTH DISTRIBUIDORA DE SONORA", "Clasificacion_Cliente"] = "CI"
        df2.loc[(df2["Cliente"].str.contains("SEGUROS")) | (df2["Cliente"].str.contains("SEGURO")) | (df2["Cliente"] == "GRUPO NACIONAL PROVINCIAL"), "Clasificacion_Cliente"] = "SEGUROS"

        # debemos de quitar garantia para hacer la clasificacion por tipo servicio
        QuitamosGarantia = df2.query("~(Clasificacion_Cliente == ['GARANTIA'])").copy()
        TomamosGarantia = df2.query("Clasificacion_Cliente == ['GARANTIA']").copy()

        #CLASIFICACION DEL CLIENTE POR "TIPO SERVICIO"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Externo"),"Clasificacion_Cliente"] = "RESCATES EXTERNOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Avalado"), "Clasificacion_Cliente"] = "RESCATES AVALADOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Taller Móvil"), "Clasificacion_Cliente"] = "TALLER MOVIL"

        # concatenamos el dataframe que no tiene garantia y ya esta clasificado por tipo servicio con el dataframe que si tiene lo de garantia
        claficicacion_tipo_servicio = pd.concat([QuitamosGarantia, TomamosGarantia], join="inner")

        # CONCATENAMOS LA COLUMNA DE NUMERO DE ORDEN y UNIDAD
        NumOrden = "OS" + claficicacion_tipo_servicio["Número_Orden"].map(str)
        Unidad = "UN-" + claficicacion_tipo_servicio["Unidad"].map(str)
        
        # INSERTAMOS LAS COLUMNAS EN SUS RESPECTIVOS LUGARES
        claficicacion_tipo_servicio.insert(0,"Num_Orden",NumOrden,allow_duplicates=True)
        claficicacion_tipo_servicio["Unidad"] = Unidad

        claficicacion_tipo_servicio.drop(["Número_Orden","Folio_Cotizaciones"], axis = 1, inplace=True)

        ultima_columna = claficicacion_tipo_servicio.columns.get_loc("Estado_Orden_Global")
        
        claficicacion_tipo_servicio = claficicacion_tipo_servicio.iloc[:,:ultima_columna + 1]

        Clasificacion_Venta = claficicacion_tipo_servicio["Clasificacion_Cliente"]

        claficicacion_tipo_servicio.insert(6,"Clasificacion_Venta",Clasificacion_Venta,allow_duplicates=False)
        

        for i in claficicacion_tipo_servicio:
            if ("fecha" in i.lower()):
                claficicacion_tipo_servicio[i] = pd.to_datetime(claficicacion_tipo_servicio[i] , errors = 'coerce')

        columna = claficicacion_tipo_servicio.pop("Subtotal_Ref_Sin_Facturar")
        claficicacion_tipo_servicio.insert(21, "Subtotal_Ref_Sin_Facturar", columna)

        claficicacion_tipo_servicio.insert(loc=25, column = 'Total OS Pde Fact', value = claficicacion_tipo_servicio[['MO', 'CM', 'TOT', 'Subtotal_Ref_Sin_Facturar']].fillna(0).sum(axis=1), allow_duplicates = False)

        claficicacion_tipo_servicio.columns = claficicacion_tipo_servicio.columns.str.replace('_', ' ')

        for col_fecha in claficicacion_tipo_servicio:
            if ("fecha" in col_fecha.lower()):
                try:
                    claficicacion_tipo_servicio[col_fecha] = claficicacion_tipo_servicio[col_fecha].dt.strftime("%d/%m/%Y")
                except:
                    pass
        
        columnas_bol=claficicacion_tipo_servicio.select_dtypes(include=bool).columns.tolist()
        claficicacion_tipo_servicio[columnas_bol] = claficicacion_tipo_servicio[columnas_bol].astype(str)

        claficicacion_tipo_servicio.to_excel(os.path.join(Variables().ruta_procesados,f'KWSonora_OrdenesDeServicio_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)
