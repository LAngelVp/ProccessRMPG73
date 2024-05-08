#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class Credito(Variables):
    def __init__(self):
        self.nombre_doc = 'CR.xlsx'
        self.concesionario = Concesionarios().concesionarioRioBravo
        path = os.path.join(Variables().ruta_Trabajos_kwrb, self.nombre_doc)
        df = pd.read_excel(path, sheet_name = 'Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        df2 = df[df.columns[0:52]].copy()
        df2.insert(loc=2, column = 'Clasificacion', value = 'CLIENTES GENERALES', allow_duplicates = False)

        n = df2[df2.Cliente.str.contains('KENWORTH')]
        concesionarios = n[n['Cliente'] != 'KENWORTH MEXICANA'].copy()
        concesionarios['Clasificacion'] = concesionarios['Clasificacion'].replace('CLIENTES GENERALES','CONCESIONARIOS')

        kenmex = df2[df2['Cliente'] == 'KENWORTH MEXICANA'].copy()
        kenmex['Clasificacion'] = kenmex['Clasificacion'].replace('CLIENTES GENERALES','KENMEX')

        paccarp = df2[df2['Cliente'] == 'PACCAR PARTS MEXICO'].copy()
        paccarp['Clasificacion'] = paccarp['Clasificacion'].replace('CLIENTES GENERALES','PACCAR PARTS')

        array_plm=['PACCAR FINANCIAL MEXICO', 'PACLEASE MEXICANA']
        plm = df2[df2.Cliente.str.contains('|'.join(array_plm))].copy()
        plm['Clasificacion'] = plm['Clasificacion'].replace('CLIENTES GENERALES', 'PLM')

        alesso = df2[df2['Cliente'] == 'ALESSO'].copy()
        alesso['Clasificacion'] = alesso['Clasificacion'].replace('CLIENTES GENERALES','ALESSO')

        arr_clientes_nogene = ['KENWORTH', 'PACCAR PARTS MEXICO','ALESSO','PACCAR FINANCIAL MEXICO','PACLEASE MEXICANA']
        clientesg = df2[~df2.Cliente.str.contains('|'.join(arr_clientes_nogene))].copy()

        # CONCATENAR LAS CLASIFICACIONES
        df_complete = pd.concat([concesionarios, kenmex, paccarp, plm, alesso, clientesg], join='inner').copy()

        # devolver las columnas de tipo fecha al formato "dia,mes,año"
        # EXCEPTO...
        # Las columnas de "fecha documento y fecha factura",
        # su formato debe de ser "mes,dia,año"
        for column_title in df_complete:
            if ('Fecha' in column_title):
                try:
                    df_complete[column_title] = (df_complete[column_title].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass
        columnas_bol=df_complete.select_dtypes(include=bool).columns.tolist()
        df_complete[columnas_bol] = df_complete[columnas_bol].astype(str)

        
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        Variables().guardar_datos_dataframe(self.nombre_doc, df_complete, self.concesionario)
        print(12)
        
        self.nombre_doc2 = 'CRG.xlsx'
        CreditoGlobal = df_complete.copy()
        CreditoGlobal.drop(["Clasificacion"], axis=1, inplace=True)
        CreditoGlobal["Mes"] = Variables().nombre_mes_actual_abreviado()

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        Variables().guardar_datos_dataframe(self.nombre_doc, CreditoGlobal, self.concesionario)