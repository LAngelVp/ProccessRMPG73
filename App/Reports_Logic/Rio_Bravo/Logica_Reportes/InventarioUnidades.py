#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from .Variables.ContenedorVariables import Variables
class InventarioUnidades(Variables):
    def __init__(self):
        path = os.path.join(Variables().ruta_Trabajo,'IUR.xlsx')
        df = pd.read_excel(path, sheet_name="Hoja2")
        df1 = df.copy()
        df1.columns = df1.columns.str.replace(" ", "_")
        df1.drop(["Serie_Motor","Int._Diario","Fecha_Vencimiento","Importe_Inventario_Moneda_Local","Moneda_Artículo","Fact._Compra_TipoCambio","Fact._Compra_Moneda"], axis=1, inplace=True)
        df1.insert(
            loc = 5,
            column = "Año Modelo",
            value = "AM"+df1["Año_Modelo"].map(str),
            allow_duplicates = True
        )
        col_serie = "S-" + df1["Serie"].map(str)
        df1["Serie"] = col_serie
        def ClasificacionTipoInv(valor):
            if (valor == "Factura"):
                return "Propia"
            else:
                return "Consigna"
        df1["TipoInv"] = df1["Tipo_Docto."].apply(lambda x:ClasificacionTipoInv(x))
        for i in df1:
            try:
                if ("f." in i.lower()):
                    df1[i] = pd.to_datetime(df1[i], errors="coerce")
                    df1[i] = df1[i].dt.strftime("%d/%m/%Y")
                else:
                    continue
            except:
                continue

        df1.drop(["Año_Modelo"], axis=1, inplace=True)
        columnas_bol=df1.select_dtypes(include=bool).columns.tolist()
        df1[columnas_bol] = df1[columnas_bol].astype(str)
        df1.columns = df1.columns.str.replace("_", " ")
        df1.to_excel(os.path.join(Variables().ruta_procesados,f'KWRB_InventarioDeUnidades_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)