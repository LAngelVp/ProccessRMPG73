#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
class ResultadosFinancieros(Variables):
    def __init__(self):
        # FUNCION PARA OBTENER EL DEPARTAMENTO
            
        # CREAMOS UN ARRAY CON EL NOMBRE DE LAS COLUMNAS QUE VAMOS A OCUPAR DEL DATAFRAME ORIGINAL
        # ESTE ARRAY SE VA A OCUPAR MAS ADELANTE PARA CREAR EL DATAFRAME FINAL.
            
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
            "NC Bonif",
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
        self.nombre_doc = 'RFR.xlsx'
        path = os.path.join(Variables().ruta_Trabajo,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        
        # creamos la tabla pivote, con el fin de obtener las unidades facturadas
        pivot = pd.pivot_table(df, index=['Numarticulo', 'Modelo', 'Sucursal', 'idCliente', 'NombreCte', 'idClienteAsignatario', 'NombreCteAsignatario', 'NumCategoria', 'Vendedor'], values=['cantidad', 'Venta', 'NC Bonif', 'VentasNetas', 'CostoTotal', 'UtilidadBruta', '% Margen Conc', 'Compras', 'VtasInternas', 'NCreddeProv', 'NCargodeProv',	'ProvNCargoCargo',	'ProvNCargoAbono',	'ProvNCredCargo',	'ProvNCredAbono',	'NotaCargoCte'
        ],  aggfunc='sum')
        

        # copiamos la tabla pivote en una nueva variable
        df_pivote = pivot.copy()

        # eliminamos el formato de la tabla pivote, con la finalidas de aparecer los numeros que la tabla pivote maneja como vacios
        df_pivote.reset_index(inplace=True)
        
        # excluimos las cotizaciones
        try:
            df_unidades_facturadas = df_pivote.query("cantidad == 1").copy()
        except:
            return

        df_unidades_facturadas_ordenado = df_unidades_facturadas[columnas]

        if (len(df_unidades_facturadas_ordenado) == 0):
            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            Variables().guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado)
            
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
                allow_duplicates=False
            )

            departamento = df_unidades_facturadas_ordenado["Modelo"].apply(lambda x: self.obtenerDepartamento(x))
            col_numero_articulo = "CH-" + df_unidades_facturadas_ordenado["Numarticulo"].map(str)
            col_modelo = "AM" + df_unidades_facturadas_ordenado["Modelo"].map(str)

            df_unidades_facturadas_ordenado["Numarticulo"] = col_numero_articulo
            df_unidades_facturadas_ordenado["Modelo"] = col_modelo

            df_unidades_facturadas_ordenado["Fecha"] = Variables().date_movement_config_document().replace(day=1)
            df_unidades_facturadas_ordenado["Ciudad"] = "Pendiente"
            df_unidades_facturadas_ordenado["Estado"] = "Pendiente"



            df_unidades_facturadas_ordenado.insert(
                loc = 0,
                column = "Departamento",
                value = departamento,
                allow_duplicates = False
            )

    # TERMINAMOS DE INSERTAR COLUMNAS ------------------

            # FORMATEAMOS LAS COLUMNAS DE FECHA

            for i in df_unidades_facturadas_ordenado:
                if ("fecha" in i.lower()):
                    try:
                        df_unidades_facturadas_ordenado[i] = pd.to_datetime(df_unidades_facturadas_ordenado[i], errors="coerce")
                        df_unidades_facturadas_ordenado[i] = df_unidades_facturadas_ordenado[i].dt.strftime("%d/%m/%Y")
                    except:
                        continue
                else:
                    continue

            # BUSCAMOS COLUMNAS QUE SEAN DE TIPO BOOLEANO, SI LAS ENCUENTRA, QUE LAS CONVIERTA EN CADENA.

            columnas_bol=df_unidades_facturadas_ordenado.select_dtypes(include=bool).columns.tolist()
            df_unidades_facturadas_ordenado[columnas_bol] = df_unidades_facturadas_ordenado[columnas_bol].astype(str)

            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            Variables().guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado)
        
    def obtenerDepartamento(self, valor):
            currentYear = datetime.now().year
            if (valor < currentYear):
                return "Unidades Seminuevas"
            else:
                return "Unidades Nuevas"
