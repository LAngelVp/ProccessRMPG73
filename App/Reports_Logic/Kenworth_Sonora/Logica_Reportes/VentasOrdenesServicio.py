#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# importamos librerias
import os
import pandas as pd
from datetime import *
from .Variables.ContenedorVariables import Variables

class VentasServicio(Variables):
    def __init__(self):
        super().__init__()
        self.nombre_doc = 'VSS.xlsx'
        path = os.path.join(Variables().ruta_Trabajo, self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)

        df.insert(
            loc=5,
            column='Fecha Hoy',
            value=Variables().date_movement_config_document(),
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
        if (os.path.basename(Variables().comprobar_reporte_documento_rutas(self.nombre_doc)).split(".")[1] == self.nombre_doc.split(".")[1]):
            df.to_excel(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), index=False )
        else:
            df.to_csv(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), encoding="utf-8", index=False )


    def clasificacion_departamentos(self, sucursal, vendedor):
        taller = 'Taller'
        carroceria = 'Carroceria'
        depa_taller = f'{taller} {sucursal}'
        depa_carroceria = f'{carroceria} {sucursal}'
        if (carroceria.upper() in vendedor):
            return carroceria, depa_carroceria
        else:
            return taller, depa_taller
