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
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()
        # ESTOS ARRAYS SON DE APOYO PARA LA CLASIFICACION DE LOS CLIENTES
        array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]
        #------------------------------------------------------
        self.nombre_doc = 'TES.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)

        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(' ', '_')

        df2 = df.copy()

        # CREAMOS LA COLUMNA DE CLASIFICACION CLIENTE
        df2.insert(loc=5,column="Clasificacion_Cliente",value="CLIENTES GENERALES", allow_duplicates = False)

        #CLASIFICACION DEL CLIENTE (NORMAL)
        df2.loc[df2["Cliente_Trabajo"].str.contains("KENWORTH") & ~df2["Cliente_Trabajo"].str.contains("KENWORTH MEXICANA") & ~df2["Cliente_Trabajo"].str.contains("KENWORTH DISTRIBUIDORA DE SONORA"), "Clasificacion_Cliente"] = "CONCESIONARIOS"
        df2.loc[df2["Cliente_Trabajo"].str.contains("|".join(array_Garantia)),"Clasificacion_Cliente"] = "GARANTIA"
        df2.loc[df2["Cliente_Trabajo"].str.contains("|".join(array_PLM)),"Clasificacion_Cliente"] = "PLM"
        df2.loc[df2["Cliente_Trabajo"] == "KENWORTH DISTRIBUIDORA DE SONORA", "Clasificacion_Cliente"] = "CI"
        df2.loc[(df2["Cliente_Trabajo"].str.contains("SEGUROS")) | (df2["Cliente_Trabajo"].str.contains("SEGURO")) | (df2["Cliente_Trabajo"] == "GRUPO NACIONAL PROVINCIAL"), "Clasificacion_Cliente"] = "SEGUROS"

        # debemos de quitar garantia para hacer la clasificacion por tipo servicio
        QuitamosGarantia = df2.query("~(Clasificacion_Cliente == ['GARANTIA'])").copy()
        TomamosGarantia = df2.query("Clasificacion_Cliente == ['GARANTIA']").copy()

        #MANDAMOS A LLAMAR A LA FUNCION
        TomamosGarantia["Estado_Reclamo"] = TomamosGarantia.apply(self.SinTramitar, axis = 1)

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
        claficicacion_tipo_servicio["Número_Orden"] = NumOrden
        claficicacion_tipo_servicio["Unidad"] = Unidad

        SinTramitar = claficicacion_tipo_servicio.query("Clasificacion_Cliente == ['GARANTIA'] and Estado_Trabajo != ['Cancelado', 'Facturado'] and Estado_Reclamo.isna()").copy()
        SinTramitar["Estado_Trabajo"] = "Sin Tramitar"
        Tramitadas = claficicacion_tipo_servicio.query("~(Clasificacion_Cliente == ['GARANTIA'] and Estado_Trabajo != ['Cancelado', 'Facturado'] and Estado_Reclamo.isna())")
        Completo = pd.concat([SinTramitar, Tramitadas], join="inner")

        for i in Completo:
            if ("fecha" in i.lower()):
                Completo[i] = pd.to_datetime(Completo[i] , errors = 'coerce')
            else:
                pass
        
        Antiguedad = self.variables.fecha_hoy - Completo["Fecha_Trabajo"]

        Completo.insert(loc = 3,column = 'Antigüedad',value = Antiguedad,allow_duplicates = False)
        Completo['Antigüedad'] = pd.to_numeric(Completo['Antigüedad'].dt.days, downcast='integer')

        for col_fecha in Completo:
            if ("fecha" in col_fecha.lower()):
                try:
                    Completo[col_fecha] = Completo[col_fecha].dt.strftime("%d/%m/%Y")
                except:
                    pass
        
        

        Completo.columns = Completo.columns.str.replace('_', ' ')

        columnas_bol=Completo.select_dtypes(include=bool).columns.tolist()
        Completo[columnas_bol] = Completo[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, Completo, self.concesionario)

    # CREAMOS LA FUNCION PARA LAS CLASIFICACIONES POR NUMERO DE ORDEN
    def SinTramitar(self, row):
        if row["Clasificacion_Cliente"] == "GARANTIA" and row["Estado_Trabajo"] not in ["Cancelado", "Facturado"] and pd.isna(row["Estado_Reclamo"]):
            return "Sin Tramitar"
        else:
            return row["Estado_Reclamo"]