#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class ResultadosFinancieros(Variables):

    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()
            
        columnas = [
            "Sucursal",
            "Numarticulo",
            "idCliente",
            "NombreCte",
            "idClienteAsignatario",
            "NombreCteAsignatario",
            "Vendedor",
            "NumCategoria",
            "Modelo",
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
            "NotaCargoCte"
        ]

        # OBTENEMOS LA RUTA DEL ARCHIVO Y PARSEAMOS SU CONTENIDO Y SUS CABECERAS.
        self.nombre_doc = 'RFS.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
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
        print(0)
        df_unidades_facturadas_ordenado = df_unidades_facturadas[columnas]

        if (len(df_unidades_facturadas_ordenado) == 0):
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado, self.concesionario)

        else:

            df_unidades_facturadas_ordenado.insert(
                loc = 1,
                column = "ZonaVenta",
                value = df_unidades_facturadas_ordenado["Sucursal"],
                allow_duplicates=True
            )
            df_unidades_facturadas_ordenado.insert(
                loc = 16,
                column = "Margen(%)",
                value = df_unidades_facturadas_ordenado["UtilidadBruta"] / df_unidades_facturadas_ordenado["VentasNetas"],
                allow_duplicates = True
            )

            
            departamento = df_unidades_facturadas_ordenado["Modelo"].apply(lambda x: self.obtenerDepartamento(x))

            df_unidades_facturadas_ordenado.insert(
                loc = 0,
                column = "Departamento",
                value = departamento,
                allow_duplicates = False
            )

            col_numero_articulo =df_unidades_facturadas_ordenado["Numarticulo"].map(str)
            col_modelo =df_unidades_facturadas_ordenado["Modelo"].map(str)

            df_unidades_facturadas_ordenado["Numarticulo"] = col_numero_articulo
            df_unidades_facturadas_ordenado["Modelo"] = col_modelo


            df_unidades_facturadas_ordenado["Fecha"] = self.variables.date_movement_config_document().replace(day=1)
            df_unidades_facturadas_ordenado["Ciudad"] = "Pendiente"
            df_unidades_facturadas_ordenado["Estado"] = "Pendiente"

    # TERMINAMOS DE INSERTAR COLUMNAS ------------------

            # FORMATEAMOS LAS COLUMNAS DE FECHA
            print(1)
            for column_name in df_unidades_facturadas_ordenado.columns:
                if "fecha" in column_name.lower():
                    print(2)
                    df_unidades_facturadas_ordenado = self.variables.global_date_format_america(df_unidades_facturadas_ordenado, column_name)
                    print(3)
                    df_unidades_facturadas_ordenado = self.variables.global_date_format_dmy_mexican(df_unidades_facturadas_ordenado, column_name)
                else:
                    pass

            # BUSCAMOS COLUMNAS QUE SEAN DE TIPO BOOLEANO, SI LAS ENCUENTRA, QUE LAS CONVIERTA EN CADENA.

            columnas_bol=df_unidades_facturadas_ordenado.select_dtypes(include=bool).columns.tolist()
            df_unidades_facturadas_ordenado[columnas_bol] = df_unidades_facturadas_ordenado[columnas_bol].astype(str)

            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado, self.concesionario)

    def obtenerDepartamento(self, valor):
        currentYear = datetime.now().year
        if (valor < currentYear):
            return "Unidades Seminuevas"
        else:
            return "Unidades Nuevas"