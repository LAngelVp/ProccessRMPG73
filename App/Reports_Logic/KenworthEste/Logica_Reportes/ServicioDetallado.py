#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import datetime
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class ServicioDetallado(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        #COMMENT: VARIABLE AUXIALIARES PARA EL CODIGO
        self.nombre_doc = "SDE.xlsx"
        self.clientes_plm = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]
        self.clientes_garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        self.columnas_after_cliente = ['ObjRefacc','ObjUBTRef','ObjMO', 'ObjUTBMO', 'Clasificacion Cliente']

        #COMMENT: LECTURA DE ARCHIVOS
        self.json_vendedores = self.variables.vendedores_y_depas_este_servicio()

        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        d = pd.read_excel(path, sheet_name='Hoja2')

        #COMMENT: CREAR COLUMNAS DE OBJETIVOS Y CLASIFICACION CLENTE
        x = 3
        for i in self.columnas_after_cliente:
            if (x <= 6):
                d.insert(loc= x,column= i,value= 0, allow_duplicates=False)
            else:
                d.insert(loc= x,column= i,value= "CLIENTES GENERALES", allow_duplicates=False)
            x = x + 1

        #--------------
        #COMMENT: FORMALIZAR VALORES VACION EN CLIENTE
        d["Cliente"].fillna("", inplace=True)

        #COMMENT: CREAR LA COLUMNA DE CLASIFICACION CLIENTE
        d.loc[d["Cliente"].str.contains("KENWORTH"), "Clasificacion Cliente"] = "CONCESIONARIOS"
        d.loc[(d["Cliente"] == "KENWORTH DEL ESTE") | (d["Cliente"] == ""), "Clasificacion Cliente"] = "CI"
        d.loc[d["Cliente"].str.contains("|".join(self.clientes_garantia)), "Clasificacion Cliente"] = "GARANTIA"
        d.loc[d["Cliente"].str.contains("|".join(self.clientes_plm)), "Clasificacion Cliente"] = "PLM"
        d.loc[(d["Cliente"].str.contains("SEGUROS")) | (d["Cliente"].str.contains("SEGURO")) | (d["Cliente"] == "GRUPO NACIONAL PROVINCIAL"), "Clasificacion Cliente"] = "SEGUROS"

        #COMMENT: PONER EN 0 LOS TPK
        d.loc[d["Descripción"] == "Descuento TPK", "Subtotal"] = 0
        d.loc[d["Descripción"] == "Descuento TPK", "Margen"] = 0

        #COMMENT: FORMALIZAMOS LOS VALORES VACIOS DE UNIDAD
        d["Unidad"].fillna("", inplace=True)

        #COMMENT_FUNCTION: CREAR LA COLUMNA DE UNIDAD  
        d["Unidad"] = d.apply(lambda fila:self.unidad(fila["Unidad"]),axis=1)

        # COMMENT: CREAR LA CONCATENACION DE NUMERO DE ORDEN
        numero_orden = 'OS' + d["Número Orden"].astype(str).str.split(".").str[0].replace("nan","").fillna("")
        d["Número Orden"] = numero_orden

        #COMMENT: CAMBIAR DE NOMBRE A UN VENDEDOR
        d["Vendedor"] = d["Vendedor"].replace("VENDEDOR CI MATRIZ", "GERARDO MENESES N")

        #COMMENT_FUNCTION: CREAR LA CLASIFICACION DE LOS DEPARTAMENTOS (INICIAL)
        d[["Depa Venta", "Depa"]] = d.apply(
            lambda fila: pd.Series(self.obtener(fila["Vendedor"])), axis=1
        )

        #COMMENT:CAMBIAR DE NORBRE EL VENDEDOR
        d["Vendedor"] = d["Vendedor"].replace("ERICK G TRUJILLO M", "ERICK G TRUJILLO M SC")

        #COMMENT: CREAR CLASIFICACION DE TUXTLA Y TIPO SERVICIO
        # d.loc[(d["Sucursal"] == "Tuxtla1") & (d["Tipo Servicio"].str.contains("Rescate")), "Depa Venta"] = "Rescates"
        # d.loc[(d["Sucursal"] == "Tuxtla1") & (d["Tipo Servicio"].str.contains("Rescate")), "Depa"] = "Rescates Tuxtla1"
        # d.loc[(d["Sucursal"] == "Tuxtla1") & (d["Tipo Servicio"].str.contains("Servicio")), "Depa Venta"] = "Servicio"
        # d.loc[(d["Sucursal"] == "Tuxtla1") & (d["Tipo Servicio"].str.contains("Servicio")), "Depa"] = "Servicio Tuxtla1"
        d.loc[(d["Sucursal"] == "Tuxtla1"), "Depa Venta"] = "Servicio"
        d.loc[(d["Sucursal"] == "Tuxtla1"), "Depa"] = "Servicio Tuxtla1"

        #COMMENT: FORMALIZAMOS LOS VALORES VACIOS EN CENTRO DE COSTOS
        d['Centro de Costos'].fillna('', inplace=True)

        #COMMENT: CREAR LA CLASIFICACION POR CENTRO DE COSTOS (BS Y SURESTE)
        consulta_carroceria_veracruz = (d["Sucursal"] == 'Veracruz') & (d["Centro de Costos"].str.contains("BS"))
        consulta_carroceria_Matriz = (d["Sucursal"] == 'Matriz Cordoba') & (d["Centro de Costos"].str.contains("BS"))
        consulta_sureste = (d["Centro de Costos"].str.contains("SURESTE"))
        d.loc[consulta_carroceria_veracruz, ["Depa Venta", "Depa"]] = ["Carroceria", "Carroceria Veracruz"]
        d.loc[consulta_carroceria_Matriz, ["Depa Venta", "Depa"]] = ["Carroceria", "Carroceria Matriz"]
        d.loc[consulta_sureste, ["Depa Venta", "Depa"]] = ["SURESTE", "SURESTE"]

        #COMMENT_FUNCTION: CREAR LA FUNCION DE LA CLASIFICACION POR CENTRO DE COSTOS (RESCATES)
        d[["Depa Venta", "Depa"]] = d.apply(
            lambda fila: pd.Series(
                self.centro_costos_rescates(
                    fila["Sucursal"], fila["Depa Venta"], fila["Depa"], fila["Centro de Costos"]
                )
            ),
            axis=1,
        )

        #COMMENT: CLASIFICAMOS DAF
        d.loc[(d["Sucursal"] == "Veracruz") & (d["Área"].str.contains("DAF")), ["Clasificacion Cliente", "Depa Venta", "Depa"]] =  ["DAF", "DAF", "DAF"]

        #COMMENT: MOVEMOS LAS COLUMNAS DE DEPARTAMENTO
        columna_depaventa = d.pop("Depa Venta")
        columna_depa = d.pop("Depa")
        d.insert(
            22,
            "Departamento Venta",
            columna_depaventa
        )
        d.insert(
            23,
            "Depa",
            columna_depa
        )

        #COMMENT: COLUMNA FANTASMA
        d["Columna_Fantasma"] = ""
        
        #COMMENT: CREAR LA COLUMNA DE AREA
        d["Area"] = "Null"
        area_mo_carroceria = ((d["Depa"].str.contains("Carroceria")) & (d["DepartamentoDetalle"] == "TALLER DE SERVICIO"))
        area_mo_servicio = ((d["Depa"].str.contains("Rescates")) | (d["Depa"].str.contains("Servicio")) | (d["Depa"].str.contains("SURESTE"))) & ((d["DepartamentoDetalle"] == "TALLER DE SERVICIO"))
        d.loc[area_mo_carroceria, "Area"] = "MO Carroceria"
        d.loc[area_mo_servicio, "Area"] = "MO Servicio"

        #COMMENT: OBTENER COLUMNAS BOOL Y PASAMOS A CADENA
        columnas_booleanas = d.select_dtypes(include=bool).columns.to_list()
        d[columnas_booleanas] = d[columnas_booleanas].astype(str)

        #COMMENT: INSERTAR COLUMNAS DE FECHA
        d.insert(10,"Fecha Movimiento",self.variables.date_movement_config_document(),allow_duplicates=False)
        d.insert(11,"Mes",self.variables.nombre_mes(),allow_duplicates=False)

        

        #COMMENT: RECORRER COLUMNAS DE FECHA PARA TRANSFORMAR
        for column_name in d.columns:
            if "fecha" in column_name.lower():
                d = self.variables.global_date_format_america(d, column_name)
                d = self.variables.global_date_format_dmy_mexican(d, column_name)
            else:
                pass

        #COMMENT: ELIMINAMOS COLUMNAS
        d.drop(
            [
                "Hora Docto.",
                "Fecha Cancelación",
                "Id. Paquete",
                "Paquete",
                "Descripción Paquete",
                "Cantidad Paquete",
                "Subtotal Paquete",
                "Saldo",
            ],
            axis=1,
            inplace=True
        )
#//////////////////////////////////////////////////////////////////////////////////////

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, d, self.concesionario)

#//////////////////////////////////////////////////////////////////////////////////////
    #COMMENT_FUNCTION: FUNCION PARA CONCATENAR UNIDAD
    def unidad(self, valor):
        valor = str(valor)
        if (valor == ""):
            return ""
        elif (valor.isdigit()):
            return "UN-" + valor
        else:
            return "UN-F" + valor 

    #COMMENT_FUNCTION: FUNCION PARA CLASIFICAR VENDEDORES EN SUS DEPARTAMENTOS
    def obtener(self, vendedor):
        for index, fila in self.json_vendedores.iterrows():
            vendedor_actual = fila["Vendedor"]
            departamento_venta = fila["Depa_Venta"]
            departamento = fila["Depa"]

            if vendedor == vendedor_actual:
                return departamento_venta, departamento

        #COMMENT: SI NO ENCUENTRA VALORES, RETORNE VACIO
        return "", ""
    #COMMENT_FUNCTION: CLASIFICACION DE RESCATES CON EL CENTRO DE COSTOS
    def centro_costos_rescates(self, sucursal, depa_venta, depa, valor_centro_costos):
        nombre_sucursal = sucursal.split(" ")[0]
        departamento_venta = "Rescates"
        departamento = f"{departamento_venta} {nombre_sucursal}"
        if "RESC" in valor_centro_costos:
            return departamento_venta, departamento
        else:
            return depa_venta, depa
        
