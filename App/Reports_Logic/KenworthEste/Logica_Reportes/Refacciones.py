#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class Refacciones(Variables):
    def __init__(self):

#COMMENT: APARTADO DE DOCUMENTOS DE APOYO
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()

        self.nombre_doc = 'RE.xlsx'

        self.j = self.variables.clasificacion_vendedores_departamentos_refacciones()
        self.c = self.variables.clasificacion_tamaño_clientes_refacciones()
        self.m = self.variables.marcas_refacciones_fun()


#COMMENT: LEER EL DOCUMENTO
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)

#COMMENT: ELIMINAMOS COLUMNAS
        df.drop(
            [
                "% Margen",
                "Meta Ventas Por Vendedor",
                "Meta Margen Por Vendedor",
                "Meta Cantidad Por Vendedor",
                "Meta Ventas Por Sucursal",
                "Meta Margen Por Sucursal",
                "Meta Cantidad Por Sucursal",
                "% Comisión Por Margen",
                "% Comisión Por Ventas",
                "Comisión Por Margen",
                "Comisión Por Ventas",
                "EsBonificacion",
                "IdUsuario",
                "IdPaquete",
                "Paquete",
                "Descripción Paquete",
                "Cantidad Paquete",
                "Subtotal Paquete",
                "Potencial Total",
                "Tipo de Cambio del día",
                "OCCliente",
                "% Margen Sin Descuento",
            ],
            axis=1,
            inplace=True,
        )
        a = df[df.columns[0:93]].copy()
        a = pd.concat([a, df['ECommerce']], axis=1)

#COMMENT: CONVERTIMOS LA FECHA
        for column_name in a.columns:
            if "fecha" in column_name.lower():
                a = self.variables.global_date_format_america(a, column_name)
                a = self.variables.global_date_format_mdy_america(a, column_name)
            else:
                pass

#COMMENT: CREAR COLUMNA DE MOVIMIENTO
        a["Columna_movimiento"] = "False"
        a.loc[(a["Cliente"] == "TRANSPORTES G.R.L.") | (a["Sucursal"] == "Coatzacoalcos"), "Columna_movimiento"] = 'e-KREI'
        a.loc[(a["Vendedor"] == "NOTAS DE CARGO"), "Vendedor"] = "EDWARD REYES P"

#COMMENT: CREAR LAS COLUMNAS DE CLASIFICACION DE VENDEDORES
        a[["Depto_venta","Depto_normal"]] = a.apply(
            lambda fila: pd.Series(
                self.clasificacion_vendedores(fila["Vendedor"], fila["Sucursal"])
            ),
            axis=1,
        )

#COMMENT: CONDICIONES PARA LAS CLASIFICACIONES DE CENTRO DE COSTOS 1
        consulta_carroceria_veracruz = (a["Sucursal"] == 'Veracruz') & (a["Centro de Costo"].str.contains("BS"))
        consulta_carroceria_Matriz = (a["Sucursal"] == 'Matriz Cordoba') & (a["Centro de Costo"].str.contains("BS"))
#COMMENT: CLASIFICACIONES POR LOS CENTROS DE COSTOS 1
        a.loc[consulta_carroceria_veracruz, "Depto_venta"] = "Carroceria Veracruz"
        a.loc[consulta_carroceria_veracruz, "Depto_normal"] = "Carroceria"
        a.loc[consulta_carroceria_Matriz, "Depto_venta"] = "Carroceria Matriz"
        a.loc[consulta_carroceria_Matriz, "Depto_normal"] = "Carroceria"

        a[["Depto_venta", "Depto_normal"]] = a.apply(
            lambda fila: pd.Series(
                self.centro_costos_rescates(
                    fila["Sucursal"],
                    fila["Depto_venta"],
                    fila["Depto_normal"],
                    fila["Centro de Costo"],
                )
            ),
            axis=1,
        )

#COMMENT: CLASIFICACION DEL DEPARTAMENTO DE MERIDA POR CENTRO DE COSTOS
        servicio_merida = ((a["Sucursal"] == "Merida") & (a["Centro de Costo"] == "REQUISICIONES"))
        a.loc[servicio_merida, ["Depto_venta", "Depto_normal"]] = ["Servicio Merida", "Servicio"]

#COMMENT: CLASIFICACION DEL TAMAÑO DE LOS CLIENTES
        a["Status_cliente"] = a.apply(lambda fila: pd.Series(self.clientes_grandes(fila["Cliente"], fila["Sucursal"])), axis=1)

#COMMENT: CLASIFICACION DE LA COLUMNA DE AREA
        a["Area"] = ""
        a.loc[(a["Depto_normal"] == "Mostrador"), "Area"] = "Refacc Mostrador"
        a.loc[(a["Depto_normal"] == "Carroceria"), "Area"] = "Refacc Carroceria"
        a.loc[((a["Depto_normal"] == "Servicio") | (a["Depto_normal"] == "Rescates")), "Area"] = "Refacc Servicio"


#COMMENT: CLASIFICACION DE LA MARCA DE LAS REFACCIONES
        a["Marca"] = a.apply(
            lambda fila: pd.Series(
                self.marca_refacciones(
                    fila["Número Artículo"], fila["Número Categoría"], fila["Categoría"]
                )
            ),
            axis=1,
        )

#COMMENT: CREATE COLUMN JOB POSITION
        a["Puesto de Trabajo"] = a.apply(lambda fila: pd.Series(self.posicion_de_trabajo(fila["Sucursal"])), axis=1)

#COMMENT: CREATE COLUMN "ID_CLIENTE" (CONCATENATE)
        Id_Cliente = "ID" + a["Id Cliente"].map(str)
        a.drop(["Id Cliente"], axis=1, inplace=True)
        a.insert(
            loc = 15,
            column = "Id Cliente",
            value = Id_Cliente,
            allow_duplicates = False
        )

#COMMENT:OBTENEMOS LAS COLUMNAS BOOL A STR
        columnas_bol=a.select_dtypes(include=bool).columns.tolist()
        a[columnas_bol] = a[columnas_bol].astype(str)

#COMMENT: MOVEMOS LA COLUMNA DE MOVIMIENTO A SU LUGAR
        columna_movimiento = a.pop("Columna_movimiento")
        a.insert(67, "Columna_movimiento", columna_movimiento)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, a, self.concesionario)


#SEPARATOR ---------------------------------------------------------------------------------
#COMMENT:FUNCIONES PARA LA CREACION DE COLUMNAS
            
#COMMENT_FUNCTION: FUNCION PARA CLASIFICAR LOS VENDEDORES CON SUS DEPARTAMENTOS
    def clasificacion_vendedores(self, vendedor, sucursal):
        for index, valor in self.j.iterrows():
            valor_vendedor = valor["vendedor"]
            valor_sucursal = valor["sucursal"]
            valor_depto_venta = valor["depto venta"]
            valor_departamento = valor["departamento"]
            if vendedor == valor_vendedor and sucursal == valor_sucursal:
                return valor_depto_venta, valor_departamento
        return "", ""
    
#COMMENT_FUNCTION: FUNCION PARA CLASIFICAR RESCATES POR CENTRO DE COSTOS 2
    def centro_costos_rescates(self, sucursal, depa_venta, depa, valor_centro_costos):
        nombre_sucursal = sucursal.split(" ")[0]
        departamento = "Rescates"
        departamento_venta = f"{departamento} {nombre_sucursal}"
        if "RESC" in str(valor_centro_costos):
            return departamento_venta, departamento
        else:
            return depa_venta, depa

#COMMENT_FUNCTION: FUNCION PARA LA CLASIFICACION DE LOS TAMAÑOS DE LOS CLIENTES
    def clientes_grandes(self, cliente,sucursal):
        for i, valor in self.c.iterrows():
            valor_cliente = valor["cliente"]
            valor_sucursal = valor["sucursal"]

            if (str(cliente) == str(valor_cliente)) and (str(sucursal) == str(valor_sucursal)):
                return "grandes"
        return "pequeños"

#COMMENT_FUNCTION: FUNCION PARA LA CLASIFICACION DE LA MARCA DE LAS REFACCIONES
    def marca_refacciones(self, numero_articulo, numero_categoria, categoria):
        for i, valor in self.m.iterrows():
            valor_articulo = valor["Número Artículo"]
            valor_num_categoria = valor["Número Categoría"]
            valor_categoria = valor["Ctegoria"]
            valor_marca = valor["Marca"]
            if (
                (str(numero_articulo) == str(valor_articulo))
                and (str(numero_categoria) == str(valor_num_categoria))
                and (str(categoria) == str(valor_categoria))
            ):
                return valor_marca
        return "SM"
    
    def posicion_de_trabajo(self, sucursal):
        for index, valor in self.j.iterrows():
            valor_vendedor = valor["vendedor"]
            valor_sucursal = valor["sucursal"]
            valor_jerarquia = valor["jerarquia"]
            if sucursal == valor_sucursal and valor_jerarquia.lower() == "coordinador":
                return valor_vendedor
        return ""