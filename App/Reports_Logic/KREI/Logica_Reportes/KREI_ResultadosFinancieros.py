#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class ResultadosFinancierosKREI(Variables):
    def __init__(self) -> None:
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()

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

    def ReporteFinancieroKWESTE_KREI(self):
        self.nombre_doc = 'RFEKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        # LEEMOS EL DOCUMENTO
        df = pd.read_excel(path, sheet_name="Hoja2")
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
            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado, self.concesionario)
            
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

            Fecha = self.variables.date_movement_config_document()

            df_unidades_facturadas_ordenado.insert(
                loc = 26,
                column = "Fecha",
                value = Fecha,
                allow_duplicates = True
            )

            for column_name in df_unidades_facturadas_ordenado.columns:
                if "fecha" in column_name.lower():
                    df_unidades_facturadas_ordenado = self.variables.global_date_format_america(df_unidades_facturadas_ordenado, column_name)
                    df_unidades_facturadas_ordenado = self.variables.global_date_format_dmy_mexican(df_unidades_facturadas_ordenado, column_name)
                else:
                    pass

            columnas_bol=df_unidades_facturadas_ordenado.select_dtypes(include=bool).columns.tolist()
            df_unidades_facturadas_ordenado[columnas_bol] = df_unidades_facturadas_ordenado[columnas_bol].astype(str)

            df_unidades_facturadas_ordenado.columns = df_unidades_facturadas_ordenado.columns.str.replace("_", " ")

            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado, self.concesionario)


    def ReporteFinancieroKWSUR_KREI(self):
        self.nombre_doc = 'RFSKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        # LEEMOS EL DOCUMENTO
        df = pd.read_excel(path, sheet_name="Hoja2")
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
            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado, self.concesionario)
            
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

            Fecha = self.variables.date_movement_config_document()

            df_unidades_facturadas_ordenado.insert(
                loc = 26,
                column = "Fecha",
                value = Fecha,
                allow_duplicates = True
            )

            for column_name in df_unidades_facturadas_ordenado.columns:
                if "fecha" in column_name.lower():
                    df_unidades_facturadas_ordenado = self.variables.global_date_format_america(df_unidades_facturadas_ordenado, column_name)
                    df_unidades_facturadas_ordenado = self.variables.global_date_format_dmy_mexican(df_unidades_facturadas_ordenado, column_name)
                else:
                    pass

            columnas_bol=df_unidades_facturadas_ordenado.select_dtypes(include=bool).columns.tolist()
            df_unidades_facturadas_ordenado[columnas_bol] = df_unidades_facturadas_ordenado[columnas_bol].astype(str)

            df_unidades_facturadas_ordenado.columns = df_unidades_facturadas_ordenado.columns.str.replace("_", " ")

            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado, self.concesionario)


    def obtenerDepartamento(self,valor):
            currentYear = self.variables.fecha_hoy.year
            if (valor < currentYear):
                return "SEMINUEVAS"
            else:
                return "NUEVAS"
            