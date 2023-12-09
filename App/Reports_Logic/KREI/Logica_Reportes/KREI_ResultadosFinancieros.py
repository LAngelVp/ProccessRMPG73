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

        self.columnas = [
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
        
        # creamos la tabla pivote, con el fin de obtener las unidades facturadas
        pivot = pd.pivot_table(df, index=['Numarticulo', 'Modelo', 'Sucursal', 'idCliente', 'NombreCte', 'idClienteAsignatario', 'NombreCteAsignatario', 'NumCategoria', 'Vendedor'], values=['cantidad', 'Venta', 'NC_Bonif', 'VentasNetas', 'CostoTotal', 'UtilidadBruta', '%_Margen_Conc', 'Compras', 'VtasInternas', 'NCreddeProv', 'NCargodeProv',	'ProvNCargoCargo',	'ProvNCargoAbono',	'ProvNCredCargo',	'ProvNCredAbono',	'NotaCargoCte'
        ],  aggfunc='sum')

        # copiamos la tabla pivote en una nueva variable
        df_pivote = pivot.copy()

        # eliminamos el formato de la tabla pivote, con la finalidas de aparecer los numeros que la tabla pivote maneja como vacios
        df_pivote.reset_index(inplace=True)
        
        # excluimos las cotizaciones
        df_unidades_facturadas = df_pivote.query("cantidad == 1").copy()

        df_unidades_facturadas_ordenado = df_unidades_facturadas[self.columnas]

        if (len(df_unidades_facturadas_ordenado) == 0):
            return
            
        else:
            df_unidades_facturadas_ordenado.insert(
                    loc = 0,
                    column = "Concesionario",
                    value = "ESTE",
                    allow_duplicates=True
                )
            
            departamento = df_unidades_facturadas_ordenado["Modelo"].apply(lambda x: self.obtenerDepartamento(x))

            df_unidades_facturadas_ordenado.insert(
                loc = 1,
                column = "Departamento",
                value = departamento,
                allow_duplicates = False
            )


            col_numero_articulo = "CH-" + df_unidades_facturadas_ordenado["Numarticulo"].map(str)
            col_modelo = "AM" + df_unidades_facturadas_ordenado["Modelo"].map(str)

            df_unidades_facturadas_ordenado["Numarticulo"] = col_numero_articulo
            df_unidades_facturadas_ordenado["Modelo"] = col_modelo

            Margen = df_unidades_facturadas_ordenado["UtilidadBruta"] / df_unidades_facturadas_ordenado["VentasNetas"]

            df_unidades_facturadas_ordenado.insert(
                loc = 16,
                column = "Margen(%)",
                value = Margen,
                allow_duplicates = True
            )

            Fecha = Variables().date_movement_config_document()

            df_unidades_facturadas_ordenado.insert(
                loc = 26,
                column = "Fecha",
                value = Fecha,
                allow_duplicates = True
            )

            for i in df_unidades_facturadas_ordenado:
                if ("fecha" in i.lower()):
                    try:
                        df_unidades_facturadas_ordenado[i] = pd.to_datetime(df_unidades_facturadas_ordenado[i], errors="coerce")
                        df_unidades_facturadas_ordenado[i] = df_unidades_facturadas_ordenado[i].dt.strftime("%d/%m/%Y")
                    except:
                        continue
                else:
                    continue

            columnas_bol=df_unidades_facturadas_ordenado.select_dtypes(include=bool).columns.tolist()
            df_unidades_facturadas_ordenado[columnas_bol] = df_unidades_facturadas_ordenado[columnas_bol].astype(str)

            df_unidades_facturadas_ordenado.columns = df_unidades_facturadas_ordenado.columns.str.replace("_", " ")

            df_unidades_facturadas_ordenado.to_excel(os.path.join(Variables().ruta_procesados,f'KREI_ResultadosFinancieros_KWESTE_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)


    def ReporteFinancieroKWSUR_KREI(self, PATH):
        # LEEMOS EL DOCUMENTO
        df = pd.read_excel(PATH, sheet_name="Hoja2")
        df.columns = df.columns.str.replace(" ", "_")
        
        # creamos la tabla pivote, con el fin de obtener las unidades facturadas
        pivot = pd.pivot_table(df, index=['Numarticulo', 'Modelo', 'Sucursal', 'idCliente', 'NombreCte', 'idClienteAsignatario', 'NombreCteAsignatario', 'NumCategoria', 'Vendedor'], values=['cantidad', 'Venta', 'NC_Bonif', 'VentasNetas', 'CostoTotal', 'UtilidadBruta', '%_Margen_Conc', 'Compras', 'VtasInternas', 'NCreddeProv', 'NCargodeProv',	'ProvNCargoCargo',	'ProvNCargoAbono',	'ProvNCredCargo',	'ProvNCredAbono',	'NotaCargoCte'
        ],  aggfunc='sum')

        # copiamos la tabla pivote en una nueva variable
        df_pivote = pivot.copy()

        # eliminamos el formato de la tabla pivote, con la finalidas de aparecer los numeros que la tabla pivote maneja como vacios
        df_pivote.reset_index(inplace=True)
        
        # excluimos las cotizaciones
        df_unidades_facturadas = df_pivote.query("cantidad == 1").copy()

        df_unidades_facturadas_ordenado = df_unidades_facturadas[self.columnas]

        if (len(df_unidades_facturadas_ordenado) == 0):
            return
            
        else:
            df_unidades_facturadas_ordenado.insert(
                    loc = 0,
                    column = "Concesionario",
                    value = "SUR",
                    allow_duplicates=True
                )
            
            departamento = df_unidades_facturadas_ordenado["Modelo"].apply(lambda x: self.obtenerDepartamento(x))

            df_unidades_facturadas_ordenado.insert(
                loc = 1,
                column = "Departamento",
                value = departamento,
                allow_duplicates = False
            )


            col_numero_articulo = "CH-" + df_unidades_facturadas_ordenado["Numarticulo"].map(str)
            col_modelo = "AM" + df_unidades_facturadas_ordenado["Modelo"].map(str)

            df_unidades_facturadas_ordenado["Numarticulo"] = col_numero_articulo
            df_unidades_facturadas_ordenado["Modelo"] = col_modelo

            Margen = df_unidades_facturadas_ordenado["UtilidadBruta"] / df_unidades_facturadas_ordenado["VentasNetas"]

            df_unidades_facturadas_ordenado.insert(
                loc = 16,
                column = "Margen(%)",
                value = Margen,
                allow_duplicates = True
            )

            Fecha = Variables().date_movement_config_document()

            df_unidades_facturadas_ordenado.insert(
                loc = 26,
                column = "Fecha",
                value = Fecha,
                allow_duplicates = True
            )

            for i in df_unidades_facturadas_ordenado:
                if ("fecha" in i.lower()):
                    try:
                        df_unidades_facturadas_ordenado[i] = pd.to_datetime(df_unidades_facturadas_ordenado[i], errors="coerce")
                        df_unidades_facturadas_ordenado[i] = df_unidades_facturadas_ordenado[i].dt.strftime("%d/%m/%Y")
                    except:
                        continue
                else:
                    continue

            columnas_bol=df_unidades_facturadas_ordenado.select_dtypes(include=bool).columns.tolist()
            df_unidades_facturadas_ordenado[columnas_bol] = df_unidades_facturadas_ordenado[columnas_bol].astype(str)

            df_unidades_facturadas_ordenado.columns = df_unidades_facturadas_ordenado.columns.str.replace("_", " ")

            df_unidades_facturadas_ordenado.to_excel(os.path.join(Variables().ruta_procesados,f'KREI_ResultadosFinancieros_KWSUR_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)


    def obtenerDepartamento(self,valor):
            currentYear = Variables().fecha_hoy.year
            if (valor < currentYear):
                return "SEMINUEVAS"
            else:
                return "NUEVAS"
            