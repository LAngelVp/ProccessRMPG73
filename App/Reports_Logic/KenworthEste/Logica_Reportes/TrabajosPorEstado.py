#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios


class TrabajosPorEstado(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        # ESTOS ARRAYS SON DE APOYO PARA LA CLASIFICACION DE LOS CLIENTES
        array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]

        self.nombre_doc = 'TEE.xlsx'

        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)

        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(' ', '_')

        df2 = df.copy()

        union_kenowrth_mexicana = df2.query("Cliente_Trabajo == ['KENWORTH MEXICANA', 'KENWORTH MEXICANA,S.A. DE C.V.']").copy()
        union_kenowrth_mexicana["Cliente_Trabajo"] = "KENWORTH MEXICANA"
        union_kenworth_mexicana_Negada = df2.query("~(Cliente_Trabajo == ['KENWORTH MEXICANA', 'KENWORTH MEXICANA,S.A. DE C.V.'])").copy()
        kenworth_mexicanas_unificadas = pd.concat([union_kenowrth_mexicana, union_kenworth_mexicana_Negada], join="inner")


        # CREAMOS LA COLUMNA DE CLASIFICACION CLIENTE
        kenworth_mexicanas_unificadas.insert(loc=5,column="Clasificacion_Cliente",value="CLIENTES GENERALES", allow_duplicates = False)

        #CLASIFICACION DEL CLIENTE (NORMAL)
        kenworth_mexicanas_unificadas.loc[kenworth_mexicanas_unificadas["Cliente_Trabajo"].str.contains("KENWORTH") & ~kenworth_mexicanas_unificadas["Cliente_Trabajo"].str.contains("KENWORTH MEXICANA","KENWORTH DEL ESTE") & ~kenworth_mexicanas_unificadas["Cliente_Trabajo"].str.contains("KENWORTH DEL ESTE"), "Clasificacion_Cliente"] = "CONCESIONARIOS"
        kenworth_mexicanas_unificadas.loc[kenworth_mexicanas_unificadas["Cliente_Trabajo"].str.contains("|".join(array_Garantia)),"Clasificacion_Cliente"] = "GARANTIA"
        kenworth_mexicanas_unificadas.loc[kenworth_mexicanas_unificadas["Cliente_Trabajo"].str.contains("|".join(array_PLM)),"Clasificacion_Cliente"] = "PLM"
        kenworth_mexicanas_unificadas.loc[kenworth_mexicanas_unificadas["Cliente_Trabajo"] == "KENWORTH DEL ESTE", "Clasificacion_Cliente"] = "CI"
        kenworth_mexicanas_unificadas.loc[(kenworth_mexicanas_unificadas["Cliente_Trabajo"].str.contains("SEGUROS")) | (kenworth_mexicanas_unificadas["Cliente_Trabajo"].str.contains("SEGURO")) | (kenworth_mexicanas_unificadas["Cliente_Trabajo"] == "GRUPO NACIONAL PROVINCIAL"), "Clasificacion_Cliente"] = "SEGUROS"

        # debemos de quitar garantia para hacer la clasificacion por tipo servicio
        QuitamosGarantia = kenworth_mexicanas_unificadas.query("~(Clasificacion_Cliente == ['GARANTIA'])").copy()
        TomamosGarantia = kenworth_mexicanas_unificadas.query("Clasificacion_Cliente == ['GARANTIA']").copy()

        #MANDAMOS A LLAMAR A LA FUNCION
        TomamosGarantia["Estado_Reclamo"] = TomamosGarantia.apply(self.SinTramitar, axis = 1)

        #CLASIFICACION DEL CLIENTE POR "TIPO SERVICIO"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Externo"),"Clasificacion_Cliente"] = "RESCATES EXTERNOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Avalado"), "Clasificacion_Cliente"] = "RESCATES AVALADOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Servicio a Domicilio"), "Clasificacion_Cliente"] = "SERVICIO A DOMICILIO"


        # concatenamos el dataframe que no tiene garantia y ya esta clasificado por tipo servicio con el dataframe que si tiene lo de garantia
        claficicacion_tipo_servicio = pd.concat([QuitamosGarantia, TomamosGarantia], join="inner")

        #MANDAMOS A LLAMAR A LA FUNCION
        claficicacion_tipo_servicio["Clasificacion_Cliente"] = claficicacion_tipo_servicio.apply(self.FiltroPorNumeroOrden, axis = 1)

        # CONCATENAMOS LA COLUMNA DE NUMERO DE ORDEN y UNIDAD
        NumOrden = "OS" + claficicacion_tipo_servicio["Número_Orden"].map(str)
        Unidad = "UN-" + claficicacion_tipo_servicio["Unidad"].map(str)

        # INSERTAMOS LAS COLUMNAS EN SUS RESPECTIVOS LUGARES
        claficicacion_tipo_servicio["Número_Orden"] = NumOrden
        claficicacion_tipo_servicio["Unidad"] = Unidad

        SinTramitar = claficicacion_tipo_servicio.query("Clasificacion_Cliente == ['GARANTIA'] and Estado_Trabajo != ['Cancelado', 'Facturado'] and Estado_Reclamo.isna()").copy()
        SinTramitar["Estado_Trabajo"] = "Sin Tramitar"
        Tramitadas = claficicacion_tipo_servicio.query("~(Clasificacion_Cliente == ['GARANTIA'] and Estado_Trabajo != ['Cancelado', 'Facturado'] and Estado_Reclamo.isna())")
        Completo = pd.concat([SinTramitar, Tramitadas], join="inner")

        for column_name in Completo.columns:
            if "fecha" in column_name.lower():
                Completo = self.variables.global_date_format_america(Completo, column_name)
            else:
                pass
        
        Antiguedad = (self.variables.date_movement_config_document() - Completo["Fecha_Trabajo"]).apply(lambda x : x.days)

        Completo.insert(loc = 3,column = 'Antigüedad',value = Antiguedad,allow_duplicates = False)

        for column_name in Completo.columns:
            if "fecha" in column_name.lower():
                Completo = self.variables.global_date_format_dmy_mexican(Completo, column_name)
            else:
                pass

        Completo.columns = Completo.columns.str.replace('_', ' ')

        columnas_bol=Completo.select_dtypes(include=bool).columns.tolist()
        Completo[columnas_bol] = Completo[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, Completo, self.concesionario)


    # CREAMOS LA FUNCION PARA LAS CLASIFICACIONES POR NUMERO DE ORDEN
    def FiltroPorNumeroOrden(self, row):
        if row["Número_Orden"] in [44757, 46087, 46098, 46339, 46395] and row["Sucursal"] == "Matriz Cordoba":
            return "SEGUROS"
        else:
            return row["Clasificacion_Cliente"]
        
    # CREAMOS LA FUNCION PARA LAS CLASIFICACIONES POR NUMERO DE ORDEN
    def SinTramitar(self, row):
        if row["Clasificacion_Cliente"] == "GARANTIA" and row["Estado_Trabajo"] not in ["Cancelado", "Facturado"] and pd.isna(row["Estado_Reclamo"]):
            return "Sin Tramitar"
        else:
            return row["Estado_Reclamo"]
        