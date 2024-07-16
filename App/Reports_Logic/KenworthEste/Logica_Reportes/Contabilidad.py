#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class FactSitic_document():
    def __init__(self) :
        print("dos")
        self.compras_detallado_nombredoc = 'CDEFS.xlsx'
        self.notas_cargo_proveedor_detallado = 'NCPDFS.xlsx'
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.uso_columnas = ['Tipo Docto.','UUID','Sucursal','Subtotal','Total','Saldo']
        print("MUNDO")


#APARTADO DE COMPRAS
    @property
    def compras_detallado(self):
        self.nb_compras_detallado = pd.read_excel(os.path.join(self.variables.ruta_Trabajos_kwe, self.compras_detallado_nombredoc), sheet_name='Hoja2', usecols=self.uso_columnas)
        self.nb_compras_detallado = self.nb_compras_detallado.query(" `Tipo Docto.` == 'Factura' ")
        self.nb_compras_detallado = self.nb_compras_detallado.drop(columns=['Tipo Docto.'])
        self.nb_compras_detallado = self.nb_compras_detallado.dropna(subset=["UUID"])
        self.nb_compras_detalle = self.nb_compras_detallado.pivot_table(index=['UUID','Sucursal'],values=['Subtotal', 'Total'], aggfunc='sum').reset_index()
        self.saldo_max = self.nb_compras_detallado.groupby('UUID')['Saldo'].max().reset_index()
        # Realizar la combinación
        self.completo_compras = pd.merge(self.nb_compras_detalle, self.saldo_max, on='UUID', how='left')
        uuid_mayusculas = self.completo_compras['UUID'].str.upper()
        self.completo_compras['UUID'] = uuid_mayusculas
        self.variables.guardar_datos_dataframe(self.compras_detallado_nombredoc, self.completo_compras, self.concesionario)

# APARTADO DE NOTAS DE CARGO
    @property
    def notas_cargo_proveedor(self):
        self.nb_nota_cargo_proveedor = pd.read_excel(os.path.join(self.variables.ruta_Trabajos_kwe,self.notas_cargo_proveedor_detallado), sheet_name='Hoja2', usecols=self.uso_columnas)
        self.nb_nota_cargo_proveedor = self.nb_nota_cargo_proveedor.dropna(subset=['UUID'])
        self.nb_nota_cargo_proveedor_pivote = self.nb_nota_cargo_proveedor.pivot_table(index=['UUID','Sucursal'],values=['Subtotal', 'Total'], aggfunc='sum').reset_index()
        self.saldo_max = self.nb_nota_cargo_proveedor.groupby('UUID')['Saldo'].max().reset_index()
        self.completo_notas_cargo = pd.merge(self.nb_nota_cargo_proveedor_pivote, self.saldo_max, on='UUID', how='left')

        # COMPLETO DE NOTAS DE CARGO A PROVEEDOR
        uuid_mayusculas_notas_cargo = self.completo_notas_cargo['UUID'].str.upper()
        self.completo_notas_cargo['UUID'] = uuid_mayusculas_notas_cargo

        # # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.notas_cargo_proveedor_detallado, self.completo_notas_cargo, self.concesionario)


    
class Nota_credito_retenido():
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.nota_credito_proveedor_nombredoc = 'NCRFS.xlsx'
        self.cols_nota_credito_proveedor = ['UUID', 'Sucursal','Subtotal', 'Total','Estado']

# DOCUMENTO NCR
    @property
    def Ncr(self):
        self.nb_nota_credito_proveedor = pd.read_excel(os.path.join(self.variables.ruta_Trabajos_kwe,self.nota_credito_proveedor_nombredoc), sheet_name='Hoja2', usecols=self.cols_nota_credito_proveedor)
        self.nb_nota_credito_proveedor = self.nb_nota_credito_proveedor.query("`Estado` != 'Cancelado'")
        self.nb_nota_credito_proveedor = self.nb_nota_credito_proveedor.dropna(subset=['UUID'])
        self.nb_nota_credito_proveedor_pivote = self.nb_nota_credito_proveedor.pivot_table(index=['UUID','Sucursal'],values=['Subtotal', 'Total'], aggfunc='sum').reset_index()

        # self.nb_nota_credito_proveedor_sucursales = self.nb_nota_credito_proveedor.groupby('UUID')['Sucursal'].max().reset_index()

        # self.nb_nota_credito_proveedor_pivote = pd.merge(self.nb_nota_credito_proveedor_pivote, self.nb_nota_credito_proveedor_sucursales, on='UUID', how='left')
        # COMPLETO DE NOTAS DE CARGO A PROVEEDOR
        uuid_mayusculas_notas_cargo = self.nb_nota_credito_proveedor_pivote['UUID'].str.upper()
        self.nb_nota_credito_proveedor_pivote['UUID'] = uuid_mayusculas_notas_cargo

        self.variables.guardar_datos_dataframe(self.nota_credito_proveedor_nombredoc, self.nb_nota_credito_proveedor_pivote, self.concesionario)