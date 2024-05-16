#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class PagosDeClientes(Variables):
    def __init__(self) -> None:
        super().__init__()
        #obtenemos el parth.
        #leemos el documento.
        
        self.variables = Variables()
        self.concesionario = Concesionarios().concesionarioSonora
        
        self.nombre_doc = 'PCS.xlsx'
        self.ruta = self.variables.customerPaymentGoals
        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        #copiamos la data para no afectar la original.

        #Eliminamos las columnas que no se van a ocupar.
        df.drop({'Hora Pago', 'Referencia', 'Días Plazo', 'DocumentoMSC', 'Observaciones Pago', 'Referencia Forma de Pago', 'Sucursal Responsable'}, axis=1, inplace=True)
        df = df.rename(columns={'Tipo Docto.':'Tipo Docto'})

        # damos formato a todas las cabeceras de las columnas.
        # recordar volver a la normalidad.
        df.columns = df.columns.str.replace(' ', '_')

        #insertamos columna de "Fecha Movimiento" y "Mes"
        df.insert(
            loc=4,
            column='Fecha_Movimiento',
            value=self.variables.date_movement_config_document(),
            allow_duplicates=True
        )
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_america(df, column_name)
                df = self.variables.global_date_format_dmy_mexican(df, column_name)
            else:
                pass
        
        
        # Recorremos todo el contenido de la columna de "Cuenta Bancaria".
        # si el contenido que encuentre es "digito", solo continuara.
        # si encuentra algo que no sea digito, lo remplazara por el digito 0.
        for dato in df['CuentaBancaria']:
            try:
                if (dato.isdigit() == True ):
                    continue
                else:
                    df['CuentaBancaria'] = df['CuentaBancaria'].replace(dato,0)
            except:
                pass

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        df["Objetivo"] = ""

        df.columns = df.columns.str.replace(' ', '_')
        # df_completo = df.query("~(Tipo_Docto == ['Factura de Egreso', 'Facturas de Activo Fijo'])")
        df_completo = df.copy()
        df_completo.columns = df_completo.columns.str.replace('_', ' ')

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df_completo, self.concesionario)
