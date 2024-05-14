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
        # obtenemos el path.
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()
        self.nombre_doc = 'TER.xlsx'
        # leemos el documento.
        registroos_tallerMovil = ['TM', 'Taller Movil']
        registroos_exceptoTipoServicio = ['Rescate Avalado','Rescate Carretero','TM', 'Taller Movil']
        array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "ALESSO"]
        array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]
        #------------------------------------------------------
        path = os.path.join(self.variables.ruta_Trabajos_kwrb, self.nombre_doc)
        df = pd.read_excel(path, sheet_name = "Hoja2")
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(' ', '_')

        df1 = df.copy()

        # CONCATENAMOS LA COLUMNA DE NUMERO DE ORDEN y UNIDAD
        NumOrden = "OS" + df1["Número_Orden"].map(str)
        Unidad = "UN-" + df1["Unidad"].map(str)

        # INSERTAMOS LAS COLUMNAS EN SUS RESPECTIVOS LUGARES
        df1["Número_Orden"] = NumOrden
        df1["Unidad"] = Unidad

        df1.insert(loc = 5,column = 'Clasificacion_Cliente',value = 'CLIENTES GENERALES',allow_duplicates = False)
        df1.loc[df1["Cliente_Trabajo"].str.contains("KENWORTH") & ~df1["Cliente_Trabajo"].str.contains("KENWORTH MEXICANA") & df1["Cliente_Trabajo"].str.contains("KENWORTH DEL ESTE"), "Clasificacion_Cliente"] = "CONCESIONARIOS"
        df1.loc[df1["Cliente_Trabajo"].str.contains("|".join(array_Garantia)), "Clasificacion_Cliente"] = "GARANTIA"
        df1.loc[df1["Cliente_Trabajo"].str.contains("|".join(array_PLM)), "Clasificacion_Cliente"] = "PLM"
        df1.loc[df1["Cliente_Trabajo"] == "KENWORTH DEL ESTE", "Clasificacion_Cliente"] = "CI"

        QuitamosGarantia = df1.query("~(Clasificacion_Cliente == ['GARANTIA'])")
        TomamosGarantia = df1.query("(Clasificacion_Cliente == ['GARANTIA'])")

        #MANDAMOS A LLAMAR A LA FUNCION
        TomamosGarantia["Estado_Reclamo"] = TomamosGarantia.apply(self.SinTramitar, axis = 1)

        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Avalado"), "Clasificacion_Cliente"] = "RESCATES AVALADOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Carretero"), "Clasificacion_Cliente"] = "RESCATES CARRETEROS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("|".join(registroos_tallerMovil)), "Clasificacion_Cliente"] = "TALLER MOVIL"

        # concatenamos el dataframe que no tiene garantia y ya esta clasificado por tipo servicio con el dataframe que si tiene lo de garantia
        claficicacion_tipo_servicio = pd.concat([QuitamosGarantia, TomamosGarantia], join="inner")
        claficicacion_tipo_servicio.insert(loc = 3,column = "Fecha_Hoy",value = self.variables.date_movement_config_document(),allow_duplicates = False)

        for column_name in claficicacion_tipo_servicio.columns:
            if "Fecha" in column_name:
                claficicacion_tipo_servicio = self.variables.global_date_format_america(claficicacion_tipo_servicio, column_name)
            else:
                pass


        Antiguedad = (claficicacion_tipo_servicio["Fecha_Hoy"] - claficicacion_tipo_servicio["Fecha_Trabajo"]).apply(lambda x : x.days)

        claficicacion_tipo_servicio.insert(loc = 4,column = 'Antigüedad',value = Antiguedad, allow_duplicates = False)


        for column_name in claficicacion_tipo_servicio.columns:
            if "Fecha" in column_name:
                claficicacion_tipo_servicio = self.variables.global_date_format_dmy_mexican(claficicacion_tipo_servicio, column_name)
            else:
                pass
            
        claficicacion_tipo_servicio.drop(['Fecha_Hoy'], axis=1, inplace=True)

        columnas_bol=claficicacion_tipo_servicio.select_dtypes(include=bool).columns.tolist()
        claficicacion_tipo_servicio[columnas_bol] = claficicacion_tipo_servicio[columnas_bol].astype(str)
        
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, claficicacion_tipo_servicio, self.concesionario)

    # CREAMOS LA FUNCION PARA LAS CLASIFICACIONES POR NUMERO DE ORDEN
    def SinTramitar(self, row):
        if row["Clasificacion_Cliente"] == "GARANTIA" and row["Estado_Trabajo"] not in ["Cancelado", "Facturado"] and pd.isna(row["Estado_Reclamo"]):
            return "Sin Tramitar"
        else:
            return row["Estado_Reclamo"]
