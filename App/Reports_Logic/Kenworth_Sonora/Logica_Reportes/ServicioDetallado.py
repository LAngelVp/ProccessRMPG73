#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from .Variables.ContenedorVariables import Variables

class ServicioDetallado(Variables):
    def __init__(self):
        super().__init__()
        # array_columns = ['ObjRefacc','ObjUBTRef','ObjMO', 'ObjUTBMO','Clasificacion Cliente']
        array_columns2 = ['DepaVenta', 'Depa']
        array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]

        self.nombre_doc = "SDS.xlsx"
        path = os.path.join(Variables().ruta_Trabajo,self.nombre_doc)
        pt = pd.read_excel(path, sheet_name='Hoja2')
        pt = pt.replace(to_replace=';', value='-', regex=True)
        df = pt.copy()

        df.insert(
            loc=5,
            column='Fecha_Movimiento',
            value=Variables().date_movement_config_document(),
            allow_duplicates=True
        )
        df.insert(
            loc=6,
            column='Mes',
            value= Variables().nombre_mes(),
            allow_duplicates=True
        )

        df.insert(3,"Clasificacion Cliente","CLIENTES GENERALES",allow_duplicates=False)

        y = 20
        for i in array_columns2:
            df.insert(
                loc = y,
                column = i,
                value = '',
                allow_duplicates = False
            )
            y = y+1

        df["Cliente"].fillna("", inplace=True)
        #CLASIFICACION DEL CLIENTE (NORMAL)
        df.loc[df["Cliente"].str.contains("KENWORTH") & ~df["Cliente"].str.contains("KENWORTH MEXICANA") & ~df["Cliente"].str.contains("KENWORTH DISTRIBUIDORA DE SONORA"), "Clasificacion Cliente"] = "CONCESIONARIOS"
        df.loc[df["Cliente"].str.contains("|".join(array_Garantia)),"Clasificacion Cliente"] = "GARANTIA"
        df.loc[df["Cliente"].str.contains("|".join(array_PLM)),"Clasificacion Cliente"] = "PLM"
        df.loc[(df["Cliente"] == "KENWORTH DISTRIBUIDORA DE SONORA") | (df["Cliente"] == ""), "Clasificacion Cliente"] = "CI"
        df.loc[(df["Cliente"].str.contains("SEGUROS")) | (df["Cliente"].str.contains("SEGURO")) | (df["Cliente"] == "GRUPO NACIONAL PROVINCIAL"), "Clasificacion Cliente"] = "SEGUROS"

        unidad = "UN-" + df["Unidad"].map(str)
        numero_orden = "OS" + df["Número Orden"].map(str)
        
        df["Unidad"] = unidad
        df["Número Orden"] = numero_orden

        # clasificacion del vendedor
        # "TALLER"
        # Depa Venta
        # obregon
        df.loc[df["Vendedor"] == "TALLER OBREGON", "DepaVenta"] = "Taller"
        df.loc[df["Vendedor"] == "MANUEL BELTRAN", "DepaVenta"] = "Taller"
        # Hermosillo
        df.loc[df["Vendedor"] == "TALLER HERMOSILLO", "DepaVenta"] = "Taller"
        # Nogales
        df.loc[df["Vendedor"] == "TALLER NOGALES", "DepaVenta"] = "Taller"
        # Rene Alejandro
        df.loc[df["Vendedor"] == "RENE ALEJANDRO ACOSTA VALENZUELA", "DepaVenta"] = "Taller"
        # Baldenegro Arvayo
        df.loc[df["Vendedor"] == "BALDENEGRO ARVAYO MIGUEL BAUDELIO", "DepaVenta"] = "Taller"

        # Depa
        df.loc[df["Vendedor"] == "TALLER OBREGON" , "Depa"] = "Taller Obregon"
        df.loc[df["Vendedor"] == "MANUEL BELTRAN" , "Depa"] = "Taller Obregon"
        # Hermosillo
        df.loc[df["Vendedor"] == "TALLER HERMOSILLO", "Depa"] = "Taller Hermosillo"
        # Nogales
        df.loc[df["Vendedor"] == "TALLER NOGALES", "Depa"] = "Taller Nogales"
        # Rene Alejandro
        df.loc[df["Vendedor"] == "RENE ALEJANDRO ACOSTA VALENZUELA", "Depa"] = "Taller Nogales"
        # Baldenegro Arvayo
        df.loc[df["Vendedor"] == "BALDENEGRO ARVAYO MIGUEL BAUDELIO", "Depa"] = "Taller Hermosillo"

        # "CARROCERIA"
        # Depa Venta
        df.loc[df["Vendedor"] == "CARROCERIA HERMOSILLO", "DepaVenta"] = "Carroceria"
        df.loc[df["Vendedor"] == "TALLER DE CARR. Y PINT.", "DepaVenta"] = "Carroceria"
        # Depa
        df.loc[df["Vendedor"] == "CARROCERIA HERMOSILLO", "Depa"] = "Carroceria Hermosillo"
        df.loc[df["Vendedor"] == "TALLER DE CARR. Y PINT.", "Depa"] = "Carroceria Hermosillo"

        for column_title in df:
            if ('Fecha' in column_title):
                try:
                    df[column_title] = (df[column_title].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        df.drop(['Hora Docto.','Fecha Cancelación','Id. Paquete','Paquete','Descripción Paquete','Cantidad Paquete',"Subtotal Paquete",'Saldo'], axis=1, inplace=True)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        if (os.path.basename(Variables().comprobar_reporte_documento_rutas(self.nombre_doc)).split(".")[1] == self.nombre_doc.split(".")[1]):
            df.to_excel(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), index=False )
        else:
            df.to_csv(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), encoding="utf-8", index=False )