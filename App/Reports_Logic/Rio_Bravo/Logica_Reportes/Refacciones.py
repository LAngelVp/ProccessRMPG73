#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import*
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class Refacciones(Variables):
    def __init__(self):
        self.nombre_doc = 'RR.xlsx'
        self.concesionario = Concesionarios().concesionarioRioBravo
        path = os.path.join(Variables().ruta_Trabajos_kwrb, self.nombre_doc)

        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        
        df.drop(['% Margen', 'Meta Ventas Por Vendedor', 'Meta Margen Por Vendedor', 'Meta Cantidad Por Vendedor', 'Meta Ventas Por Sucursal', 'Meta Margen Por Sucursal', 'Meta Cantidad Por Sucursal', '% Comisión Por Margen', '% Comisión Por Ventas', 'Comisión Por Margen', 'Comisión Por Ventas', 'EsBonificacion', 'IdUsuario', 'IdPaquete', 'Paquete', 'Descripción Paquete', 'Cantidad Paquete', 'Subtotal Paquete', 'Potencial Total', 'Tipo de Cambio del día', 'OCCliente', '% Margen Sin Descuento'], axis=1, inplace=True)

        df = df[df.columns[0:93]].copy()

        self.columnas_fecha = df.select_dtypes(include=['datetime64']).columns
        
        for column_title in self.columnas_fecha:
            try:
                df[column_title] = pd.to_datetime(df[column_title], format='%d/%m/%Y', errors = 'coerce').dt.strftime('%d/%m/%Y')
            except:
                pass
        
        df["Departamento Venta"], df["Depa"] = zip(*df.apply(lambda fila: self.Clasificacion_departamentos_refacciones(fila["Sucursal"], fila["DepartamentoDocto"]), axis=1))

        df["Departamento Venta"], df["Depa"] = zip(*df.apply(lambda fila: self.Clasificacion_departamentos_servicio(fila["Sucursal"], fila["DepartamentoDocto"], fila["Departamento Venta"], fila["Depa"]), axis=1))

        df.loc[(df["Depa"] == "Mostrador"), "Area"] = "Refacc Mostrador"
        df.loc[(df["Depa"] == "Servicio"), "Area"] = "Refacc Servicio"

        # columna de Número de factura
        column_bill_number = df["Número Factura"].map(str) + df["Serie Factura"].map(str)

        df.drop(['Número Factura','Serie Factura'], axis=1, inplace=True)

        df.insert(loc=3, column="Número Factura", value=column_bill_number, allow_duplicates=False)

        #-------------
        
        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        Variables().guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)


    def Clasificacion_departamentos_refacciones(self, valor_sucursal, valor_departamento_documento):
        departamento_venta = None
        depa = None
        if (valor_sucursal.lower() == "matamoros") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador " + valor_sucursal.title()
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "trp acuña") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador TRP Acuña"
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "poza rica") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador " + valor_sucursal.title()
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "nuevo laredo (matriz)") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador NL Matriz"
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "trp nava") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador TRP Nava"
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "valle hermoso") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador " + valor_sucursal.title()
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "piedras negras") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador " + valor_sucursal.title()
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "trp reynosa") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador TRP Reynosa"
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "trp nuevo laredo") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador TRP Nuevo Laredo"
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "nuevo laredo (aeropuerto)") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador NL Aeropuerto"
            depa = "Mostrador"
        elif (valor_sucursal.lower() == "reynosa") and (valor_departamento_documento.lower() == "refacciones"):
            departamento_venta =  "Mostrador " + valor_sucursal.title()
            depa = "Mostrador"
        
        return departamento_venta, depa
    
    def Clasificacion_departamentos_servicio(self, valor_sucursal, valor_departamento_documento, departamento_venta, depa):
        if (valor_sucursal.lower() == "matamoros") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio " + valor_sucursal.title()
            depa = "Servicio"
        elif (valor_sucursal.lower() == "trp acuña") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio TRP Acuña"
            depa = "Servicio"
        elif (valor_sucursal.lower() == "poza rica") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio " + valor_sucursal.title()
            depa = "Servicio"
        elif (valor_sucursal.lower() == "nuevo laredo (matriz)") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio NL Matriz"
            depa = "Servicio"
        elif (valor_sucursal.lower() == "trp nava") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio TRP Nava"
            depa = "Servicio"
        elif (valor_sucursal.lower() == "valle hermoso") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio " + valor_sucursal.title()
            depa = "Servicio"
        elif (valor_sucursal.lower() == "piedras negras") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio " + valor_sucursal.title()
            depa = "Servicio"
        elif (valor_sucursal.lower() == "trp reynosa") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio TRP Reynosa"
            depa = "Servicio"
        elif (valor_sucursal.lower() == "trp nuevo laredo") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio TRP Nuevo Laredo"
            depa = "Servicio"
        elif (valor_sucursal.lower() == "nuevo laredo (aeropuerto)") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio NL Aeropuerto"
            depa = "Servicio"
        elif (valor_sucursal.lower() == "reynosa") and (valor_departamento_documento.lower() == "taller de servicio"):
            departamento_venta =  "Servicio " + valor_sucursal.title()
            depa = "Servicio"
        
        return departamento_venta, depa
