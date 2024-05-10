#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# importamos librerias
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class VentasServicio(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()
        self.nombre_doc = 'VSS.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwsonora, self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)

        df.insert(
            loc=5,
            column='Fecha Hoy',
            value=self.variables.date_movement_config_document(),
            allow_duplicates=False
        )

        df["Número Orden"].fillna("", inplace=True)
        self.numero_orden = 'OS' + df["Número Orden"].astype(str).str.split(".").str[0]

        df["Unidad"].fillna("", inplace=True)
        self.unidad = 'UN-' + df["Unidad"].astype(str)

        df['Número Orden'] = self.numero_orden
        df["Unidad"] = self.unidad
        
        df[['Departamento Venta', 'Depa']] = df.apply(lambda fila : pd.Series(self.clasificacion_departamentos(fila["Sucursal"], fila["Vendedor"])), axis=1)

        for i in df:
            if ('fecha' in i.lower()):
                try:
                    df[i] = pd.to_datetime(df[i], format='%d/%m/%Y', errors='coerce').dt.strftime('%d/%m/%Y')
                except:
                    pass

        #COMMENT:OBTENEMOS LAS COLUMNAS BOOL A STR
        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        #COMMENT: MOVEMOS LA COLUMNA DE MOVIMIENTO A SU LUGAR
        df.insert(29, "Departamento Venta", df.pop("Departamento Venta"))
        df.insert(30, "Depa", df.pop("Depa"))

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)


    def clasificacion_departamentos(self, sucursal, vendedor):
        taller = 'Taller'
        carroceria = 'Carroceria'
        depa_taller = f'{taller} {sucursal}'
        depa_carroceria = f'{carroceria} {sucursal}'
        if (carroceria.upper() in vendedor):
            return carroceria, depa_carroceria
        else:
            return taller, depa_taller
