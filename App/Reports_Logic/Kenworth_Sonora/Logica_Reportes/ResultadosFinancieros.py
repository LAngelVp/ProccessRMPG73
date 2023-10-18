#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from .Variables.ContenedorVariables import Variables
class ResultadosFinancieros(Variables):

    def __init__(self):
        super().__init__()
        # FUNCION PARA OBTENER EL DEPARTAMENTO
            
        # CREAMOS UN ARRAY CON EL NOMBRE DE LAS COLUMNAS QUE VAMOS A OCUPAR DEL DATAFRAME ORIGINAL
        # ESTE ARRAY SE VA A OCUPAR MAS ADELANTE PARA CREAR EL DATAFRAME FINAL.
            
        array_columnas_ATrabajar = [
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

        path = os.path.join(Variables().ruta_Trabajo,'RFS.xlsx')
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(" ", "_")
        
        # REALIZAMOS UNA COPIA DEL DATAFRAME
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
 
        financiero = df1_sin_coincidencias[array_columnas_ATrabajar]


        financiero.insert(
            loc = 1,
            column = "ZonaVenta",
            value = financiero["Sucursal"],
            allow_duplicates=True
        )
        financiero.insert(
            loc = 16,
            column = "Margen(%)",
            value = financiero["UtilidadBruta"] / financiero["VentasNetas"],
            allow_duplicates = True
        )

        def obtenerDepartamento(valor):
            currentYear = datetime.now().year
            if (valor < currentYear):
                return "Unidades Seminuevas"
            else:
                return "Unidades Nuevas"
        departamento = financiero["Modelo"].apply(lambda x: obtenerDepartamento(x))

        financiero.insert(
            loc = 0,
            column = "Departamento",
            value = departamento,
            allow_duplicates = False
        )

        col_numero_articulo = "CH-" + financiero["Numarticulo"].map(str)
        col_modelo = "AM" + financiero["Modelo"].map(str)

        financiero["Numarticulo"] = col_numero_articulo
        financiero["Modelo"] = col_modelo


        financiero["Fecha"] = Variables().date_movement_config_document().replace(day=1)
        financiero["Ciudad"] = "Pendiente"
        financiero["Estado"] = "Pendiente"

# TERMINAMOS DE INSERTAR COLUMNAS ------------------

        # FORMATEAMOS LAS COLUMNAS DE FECHA

        for i in financiero:
            if ("fecha" in i.lower()):
                try:
                    financiero[i] = pd.to_datetime(financiero[i], errors="coerce")
                    financiero[i] = financiero[i].dt.strftime("%d/%m/%Y")
                except:
                    continue
            else:
                continue

        # BUSCAMOS COLUMNAS QUE SEAN DE TIPO BOOLEANO, SI LAS ENCUENTRA, QUE LAS CONVIERTA EN CADENA.

        columnas_bol=financiero.select_dtypes(include=bool).columns.tolist()
        financiero[columnas_bol] = financiero[columnas_bol].astype(str)

        # GUARDAMOS EL ARCHIVO
        print(4)
        financiero.to_excel(os.path.join(Variables().ruta_procesados,f'KWSonora_ResultadosFinancieros_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)

        