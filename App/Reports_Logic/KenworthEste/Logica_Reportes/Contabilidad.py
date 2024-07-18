#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class FactSitic_document:
    def __init__(self) :
        self.compras_detallado_nombredoc = 'CDEFS.xlsx'
        self.notas_cargo_proveedor_detallado = 'NCPDFS.xlsx'
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.uso_columnas = ['Tipo Docto.','UUID','Sucursal','Subtotal','Total','Saldo']
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
    
class Nota_credito_retenido:
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
        # COMPLETO DE NOTAS DE CARGO A PROVEEDOR
        uuid_mayusculas_notas_cargo = self.nb_nota_credito_proveedor_pivote['UUID'].str.upper()
        self.nb_nota_credito_proveedor_pivote['UUID'] = uuid_mayusculas_notas_cargo
        self.variables.guardar_datos_dataframe(self.nota_credito_proveedor_nombredoc, self.nb_nota_credito_proveedor_pivote, self.concesionario)

class FactSat_document:
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.facturas_nombredoc = 'FFS.xlsx'
        self.notas_credito_nombredoc = 'NCFS.xlsx'
        self.columnas_seleccionadas = ['ESTATUS', 'TIPO', 'FECHA DE EMISIÓN', 'SERIE', 'FOLIO', 'UUID', 'UUID RELACIONADO', 'RFC', 'RAZÓN SOCIAL', 'USO DE CFDI', 'TOTAL IVA RETENIDO FINAL', 'ISR RETENIDO FINAL', 'IMPUESTO LOCAL RETENIDO FINAL', 'TOTAL FACTURADO FINAL', 'MONEDA', 'TIPO DE CAMBIO', 'MÉTODO DE PAGO', 'DESCRIPCION']
    @property
    def Facturas(self):
        self.nb_datos_completos_facturas = pd.read_excel(os.path.join(self.variables.ruta_Trabajos_kwe,self.facturas_nombredoc), usecols=None)
        # OBTENEMOS EL ENCABEZADO DE LAS COLUMNAS
        self.header = self.nb_datos_completos_facturas.iloc[2]
        self.nb_datos_completos_facturas.drop([0,1,2], inplace=True)
        # COLOCAMOS EL ENCABEZADO EN EL DATAFRAME
        self.nb_datos_completos_facturas.columns = self.header
        self.nb_datos_completos_facturas.reset_index(drop=True, inplace=True)
        # FILTRAMOS SOLO LAS FACTURAS VIGENTES
        self.nb_facturas_vigentes = self.nb_datos_completos_facturas[self.nb_datos_completos_facturas["ESTATUS"]=='Vigente']
        # DIVIDIMOS EL DOCUMENTO.
        self.nb_facturas_tiposmonedaMXN = self.nb_facturas_vigentes.iloc[:,21:41]
        self.nb_facturas_tipomonedaDolar = self.nb_facturas_vigentes.iloc[:,41:61]
        self.nb_contenido_principal = self.nb_facturas_vigentes.iloc[:,0:21]
        #REALIZAMOS LA OPERACION MATEMATICA ENTRE LOS TIPOS DE MONEDAS.
        self.nb_contenido_principal['TOTAL IVA RETENIDO FINAL'] = self.nb_facturas_tiposmonedaMXN['TOTAL IVA RETENIDO'] + self.nb_facturas_tipomonedaDolar['TOTAL IVA RETENIDO']
        self.nb_contenido_principal['ISR RETENIDO FINAL'] = self.nb_facturas_tiposmonedaMXN['ISR RETENIDO'] + self.nb_facturas_tipomonedaDolar['ISR RETENIDO']
        self.nb_contenido_principal['IMPUESTO LOCAL RETENIDO FINAL'] = self.nb_facturas_tiposmonedaMXN['IMPUESTO LOCAL RETENIDO'] + self.nb_facturas_tipomonedaDolar['IMPUESTO LOCAL RETENIDO']
        self.nb_contenido_principal['TOTAL FACTURADO FINAL'] = self.nb_facturas_tiposmonedaMXN['TOTAL FACTURADO'] + self.nb_facturas_tipomonedaDolar['TOTAL FACTURADO']
        # CREAMOS LA COLUMNA DE TIPO = FACTURA.
        self.nb_contenido_principal["TIPO"] = 'Factura'
        # RENOMBRAMOS LA COLUMNA DE DESCRIPCION POR SI NO SE LLAMA ASI.
        self.nb_contenido_principal.columns.values[1] = 'DESCRIPCION'
        # ESTRUCTURAMOS EL DOCUMENTO FINAL.
        # COLOCAMOS UN '-' A LO QUE SE ENCUENTRE VACIO EN EL DOCUMENTO.
        self.nb_contenido_principal = self.nb_contenido_principal.fillna('-')
        self.completo = self.nb_contenido_principal[self.columnas_seleccionadas]
        # CREAMOS LA COLUMNA DEL MES.
        self.completo['MES'] = self.variables.nombre_mes_actual_abreviado()
        # CREAMOS LA COLUMNA DE SUCURSAL VACIA.
        self.completo['SUCURSAL'] = ''
        # CREAMOS LA COLUMNA DE FECHA CON PRIMERO DEL MES SIEMPRE.
        self.completo["FECHA INICIO DEL MES"] = self.variables.date_movement_config_document().replace(day=1)
        # DAMOS FORMATO A LAS FECHAS
        print(self.completo['FECHA DE EMISIÓN'].dtype)
        self.completo["FECHA DE EMISIÓN"] = self.completo['FECHA DE EMISIÓN'].str.split('T').str[0]
        fecha_emision = pd.to_datetime(self.completo['FECHA DE EMISIÓN']).dt.strftime('%d/%m/%Y')
        for column_name in self.completo.columns:
                if "fecha" in column_name.lower():
                    self.completo = self.variables.global_date_format_america(self.completo, column_name)
                    self.completo = self.variables.global_date_format_dmy_mexican(self.completo, column_name)
                else:
                    pass
        self.completo['FECHA DE EMISIÓN'] = fecha_emision
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.facturas_nombredoc, self.completo, self.concesionario)
    @property
    def Nota_de_credito(self):
        self.nb_notas_credito_datos_completos = pd.read_excel(os.path.join(self.variables.ruta_Trabajos_kwe,self.notas_credito_nombredoc), usecols=None)
        # OBTENEMOS EL ENCABEZADO DE LAS COLUMNAS
        self.header = self.nb_notas_credito_datos_completos.iloc[2]
        self.nb_notas_credito_datos_completos.drop([0,1,2], inplace=True)
        # COLOCAMOS EL ENCABEZADO EN EL DATAFRAME
        self.nb_notas_credito_datos_completos.columns = self.header
        self.nb_notas_credito_datos_completos.reset_index(drop=True, inplace=True)
        # FILTRAMOS SOLO LAS FACTURAS VIGENTES
        self.nb_notas_credito_vigentes = self.nb_notas_credito_datos_completos[self.nb_notas_credito_datos_completos["ESTATUS"]=='Vigente']
        # DIVIDIMOS EL DOCUMENTO.
        self.nb_notas_credito_tiposmonedaMXN = self.nb_notas_credito_vigentes.iloc[:,21:41]
        self.nb_notas_credito_tipomonedaDolar = self.nb_notas_credito_vigentes.iloc[:,41:61]
        self.nb_contenido_principal = self.nb_notas_credito_vigentes.iloc[:,0:21]
        #REALIZAMOS LA OPERACION MATEMATICA ENTRE LOS TIPOS DE MONEDAS.
        self.nb_contenido_principal['TOTAL IVA RETENIDO FINAL'] = self.nb_notas_credito_tiposmonedaMXN['TOTAL IVA RETENIDO'] + self.nb_notas_credito_tipomonedaDolar['TOTAL IVA RETENIDO']
        self.nb_contenido_principal['ISR RETENIDO FINAL'] = self.nb_notas_credito_tiposmonedaMXN['ISR RETENIDO'] + self.nb_notas_credito_tipomonedaDolar['ISR RETENIDO']
        self.nb_contenido_principal['IMPUESTO LOCAL RETENIDO FINAL'] = self.nb_notas_credito_tiposmonedaMXN['IMPUESTO LOCAL RETENIDO'] + self.nb_notas_credito_tipomonedaDolar['IMPUESTO LOCAL RETENIDO']
        self.nb_contenido_principal['TOTAL FACTURADO FINAL'] = self.nb_notas_credito_tiposmonedaMXN['TOTAL FACTURADO'] + self.nb_notas_credito_tipomonedaDolar['TOTAL FACTURADO']
        # CREAMOS LA COLUMNA DE TIPO = FACTURA.
        self.nb_contenido_principal["TIPO"] = 'NotaCredito'
        # RENOMBRAMOS LA COLUMNA DE DESCRIPCION POR SI NO SE LLAMA ASI.
        self.nb_contenido_principal.columns.values[1] = 'DESCRIPCION'
        # ESTRUCTURAMOS EL DOCUMENTO FINAL.
        # COLOCAMOS UN '-' A LO QUE SE ENCUENTRE VACIO EN EL DOCUMENTO.
        self.nb_contenido_principal = self.nb_contenido_principal.fillna('-')
        self.completo = self.nb_contenido_principal[self.columnas_seleccionadas]
        # CREAMOS LA COLUMNA DEL MES.
        self.completo['MES'] = self.variables.nombre_mes_actual_abreviado()
        # CREAMOS LA COLUMNA DE SUCURSAL VACIA.
        self.completo['SUCURSAL'] = ''
        # CREAMOS LA COLUMNA DE FECHA CON PRIMERO DEL MES SIEMPRE.
        self.completo["FECHA INICIO DEL MES"] = self.variables.date_movement_config_document().replace(day=1)
        # DAMOS FORMATO A LAS FECHAS
        print(self.completo['FECHA DE EMISIÓN'].dtype)
        self.completo["FECHA DE EMISIÓN"] = self.completo['FECHA DE EMISIÓN'].str.split('T').str[0]
        fecha_emision = pd.to_datetime(self.completo['FECHA DE EMISIÓN']).dt.strftime('%d/%m/%Y')
        for column_name in self.completo.columns:
                if "fecha" in column_name.lower():
                    self.completo = self.variables.global_date_format_america(self.completo, column_name)
                    self.completo = self.variables.global_date_format_dmy_mexican(self.completo, column_name)
                else:
                    pass
        self.completo['FECHA DE EMISIÓN'] = fecha_emision
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.notas_credito_nombredoc, self.completo, self.concesionario)

        
                


