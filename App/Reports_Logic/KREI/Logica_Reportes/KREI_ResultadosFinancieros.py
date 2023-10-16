#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from .Variables.ContenedorVariables import Variables
class ResultadosFinancierosKREI(Variables):
    def __init__(self) -> None:
        super().__init__()
        pathEste = os.path.join(Variables().ruta_Trabajo,'RFEKREI.xlsx')
        pathSur = os.path.join(Variables().ruta_Trabajo,'RFSKREI.xlsx')

        self.array_columnas_ATrabajar = [
            "Numarticulo",
            "idCliente",
            "NombreCte",
            "idClienteAsignatario",
            "NombreCteAsignatario",
            "NumCategoria",
            "Modelo",
            "Sucursal",
            "cantidad",
            "Venta",
            "NC_Bonif",
            "VentasNetas",
            "CostoTotal",
            "UtilidadBruta",
            "Compras",
            "VtasInternas",
            "NCreddeProv",
            "NCargodeProv",
            "ProvNCargoCargo",
            "ProvNCargoAbono",
            "ProvNCredCargo",
            "ProvNCredAbono",
            "NotaCargoCte",
            "Vendedor"  
                ]

        if os.path.exists(pathEste):
            self.ReporteFinancieroKWESTE_KREI(pathEste)
        elif os.path.exists(pathSur):
            self.ReporteFinancieroKWSUR_KREI(pathSur)
        else:
            pass
    def ReporteFinancieroKWESTE_KREI(self, PATH):
        # LEEMOS EL DOCUMENTO
        df = pd.read_excel(PATH, sheet_name="Hoja2")
        df.columns = df.columns.str.replace(" ", "_")
        
        df1 = df.query("cantidad == -1").copy()
        df1["Venta"] = df1["Venta"].abs()
        df1["VentasNetas"] = df1["VentasNetas"].abs()
        df1["CostoTotal"] = df1["CostoTotal"].abs()
        df1["Compras"] = df1["Compras"].abs()

         # Comparar DataFrames y eliminar coincidencias basadas en 'factura', 'venta', 'costoTotal' y 'utilidadBruta'
        df1_sin_coincidencias = df.merge(df1, on=['Vin', 'idDocto',"idCliente","NombreCte", 'Venta', 'Compras'], how='left', indicator=True)

        df1_sin_coincidencias = df1_sin_coincidencias[df1_sin_coincidencias['_merge'] == 'left_only']
        df1_sin_coincidencias = df1_sin_coincidencias.drop(columns=['_merge'])

        df1_sin_coincidencias = df1_sin_coincidencias.query("cantidad_x == 1").copy()

        df1_sin_coincidencias.columns  = df1_sin_coincidencias.columns .str.replace("_x","")

        financiero = df1_sin_coincidencias[self.array_columnas_ATrabajar]

        financiero.insert(
                loc = 0,
                column = "Concesionario",
                value = "ESTE",
                allow_duplicates=True
            )
        
        departamento = financiero["Modelo"].apply(lambda x: self.obtenerDepartamento(x))

        financiero.insert(
            loc = 1,
            column = "Departamento",
            value = departamento,
            allow_duplicates = False
        )


        col_numero_articulo = "CH-" + financiero["Numarticulo"].map(str)
        col_modelo = "AM" + financiero["Modelo"].map(str)

        financiero["Numarticulo"] = col_numero_articulo
        financiero["Modelo"] = col_modelo

        Margen = financiero["UtilidadBruta"] / financiero["VentasNetas"]

        financiero.insert(
            loc = 16,
            column = "Margen(%)",
            value = Margen,
            allow_duplicates = True
        )

        Fecha = Variables().fecha_hoy

        financiero.insert(
            loc = 26,
            column = "Fecha",
            value = Fecha,
            allow_duplicates = True
        )

        for i in financiero:
            if ("fecha" in i.lower()):
                try:
                    financiero[i] = pd.to_datetime(financiero[i], errors="coerce")
                    financiero[i] = financiero[i].dt.strftime("%d/%m/%Y")
                except:
                    continue
            else:
                continue

        columnas_bol=financiero.select_dtypes(include=bool).columns.tolist()
        financiero[columnas_bol] = financiero[columnas_bol].astype(str)

        financiero.columns = financiero.columns.str.replace("_", " ")

        financiero.to_excel(os.path.join(Variables().ruta_procesados,f'KREI_ResultadosFinancieros_KWESTE_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)


    def ReporteFinancieroKWSUR_KREI(self, PATH):
        # LEEMOS EL DOCUMENTO
        df = pd.read_excel(PATH, sheet_name="Hoja2")
        df.columns = df.columns.str.replace(" ", "_")
        
        df1 = df.query("cantidad == -1").copy()
        df1["Venta"] = df1["Venta"].abs()
        df1["VentasNetas"] = df1["VentasNetas"].abs()
        df1["CostoTotal"] = df1["CostoTotal"].abs()
        df1["Compras"] = df1["Compras"].abs()

         # Comparar DataFrames y eliminar coincidencias basadas en 'factura', 'venta', 'costoTotal' y 'utilidadBruta'
        df1_sin_coincidencias = df.merge(df1, on=['Vin', 'idDocto',"idCliente","NombreCte", 'Venta', 'Compras'], how='left', indicator=True)

        df1_sin_coincidencias = df1_sin_coincidencias[df1_sin_coincidencias['_merge'] == 'left_only']
        df1_sin_coincidencias = df1_sin_coincidencias.drop(columns=['_merge'])

        df1_sin_coincidencias = df1_sin_coincidencias.query("cantidad_x == 1").copy()

        df1_sin_coincidencias.columns  = df1_sin_coincidencias.columns .str.replace("_x","")

        financiero = df1_sin_coincidencias[self.array_columnas_ATrabajar]

        financiero.insert(
                loc = 0,
                column = "Concesionario",
                value = "SUR",
                allow_duplicates=True
            )
        
        departamento = financiero["Modelo"].apply(lambda x: self.obtenerDepartamento(x))

        financiero.insert(
            loc = 1,
            column = "Departamento",
            value = departamento,
            allow_duplicates = False
        )


        col_numero_articulo = "CH-" + financiero["Numarticulo"].map(str)
        col_modelo = "AM" + financiero["Modelo"].map(str)

        financiero["Numarticulo"] = col_numero_articulo
        financiero["Modelo"] = col_modelo

        Margen = financiero["UtilidadBruta"] / financiero["VentasNetas"]

        financiero.insert(
            loc = 16,
            column = "Margen(%)",
            value = Margen,
            allow_duplicates = True
        )

        Fecha = Variables().date_movement_config_document()

        financiero.insert(
            loc = 26,
            column = "Fecha",
            value = Fecha,
            allow_duplicates = True
        )

        for i in financiero:
            if ("fecha" in i.lower()):
                try:
                    financiero[i] = pd.to_datetime(financiero[i], errors="coerce")
                    financiero[i] = financiero[i].dt.strftime("%d/%m/%Y")
                except:
                    continue
            else:
                continue

        columnas_bol=financiero.select_dtypes(include=bool).columns.tolist()
        financiero[columnas_bol] = financiero[columnas_bol].astype(str)

        financiero.columns = financiero.columns.str.replace("_", " ")

        financiero.to_excel(os.path.join(Variables().ruta_procesados,f'KREI_ResultadosFinancieros_KWSUR_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)


    def obtenerDepartamento(self,valor):
            currentYear = Variables().fecha_hoy.year
            if (valor < currentYear):
                return "SEMINUEVAS"
            else:
                return "NUEVAS"
            