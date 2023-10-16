#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from .Variables.ContenedorVariables import Variables
class ServioDetallado(Variables):
    def ServioDetalladoKWRB(self):
        path = os.path.join(Variables().ruta_Trabajo,"SDR.xlsx")
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # NOTE CREAMOS LAS 5 COLUMNAS DESPUES DE "CLIENTE"
        array_columns = ['ObjRefacc','ObjUBTRef','ObjMO', 'ObjUTBMO','Clasificacion Cliente']

        x = 3
        for i in array_columns:
            if (x <= 6):
                df.insert(
                    loc = x,
                    column = i,
                    value = 0,
                    allow_duplicates = False
                )
            else:
                df.insert(
                    loc = x,
                    column = i,
                    value = 'CLIENTES GENERALES',
                    allow_duplicates = False
                )
            x = x+1


        # NOTE CREAMOS LAS COLUMNAS DESPUES DE "VENDEDOR"
        array_columns2 = ['DepaVenta', 'Depa']
        y = 22
        for i in array_columns2:
            df.insert(
                loc = y,
                column = i,
                value = '',
                allow_duplicates = False
            )
            y = y+1


        # NOTE CLASIFICACIONES POR CLIENTE

        # NOTE FILTAMOS CI
        n = df['Cliente'].isnull()
        ci = df[n].copy()
        ci['Clasificacion Cliente'] = ci['Clasificacion Cliente'].replace('CLIENTES GENERALES', 'CI')
        df.drop(df[df['Cliente'].isnull()].index, inplace=True)


        # NOTE FILTRAMOS KENWORTH MENOS (KENWORTH MEXICANA)

        n = df[df.Cliente.str.contains('KENWORTH')]
        concesionarios = n[n['Cliente'] != 'KENWORTH MEXICANA'].copy()
        concesionarios['Clasificacion Cliente'] = concesionarios['Clasificacion Cliente'].replace('CLIENTES GENERALES', 'CONCESIONARIOS')

        # NOTE FILTRAMOS GARANTIA
        n = df['Cliente'] == 'KENWORTH MEXICANA'
        kenworth_m = df[n].copy()

        n = df['Cliente'] == 'ALESSO'
        alesso = df[n].copy()

        n = df['Cliente'] == 'PACCAR PARTS MEXICO'
        pcm = df[n].copy()

        # NOTE CONCATENAMOS LOS FILTROS
        garantia = pd.concat([kenworth_m, alesso, pcm], join = 'inner')
        garantia['Clasificacion Cliente'] = garantia['Clasificacion Cliente'].replace('CLIENTES GENERALES', 'GARANTIA')

        # NOTE FILTRAMOS PLM
        n = df['Cliente'] == 'PACCAR FINANCIAL MEXICO'
        pfm = df[n].copy()

        n = df['Cliente'] == 'PACLEASE MEXICANA'
        paclease = df[n].copy()

        # NOTE CONCATENAMOS LOS FILTROS
        plm = pd.concat([pfm,paclease], join='inner')
        plm['Clasificacion Cliente'] = plm['Clasificacion Cliente'].replace('CLIENTES GENERALES', 'PLM')


        # NOTE FILTRAMOS "CLIENTES GENERALES"
        arr = ['KENWORTH', 'PACCAR PARTS MEXICO','ALESSO','PACCAR FINANCIAL MEXICO','PACLEASE MEXICANA']

        clientes_generales = df[~df.Cliente.str.contains('|'.join(arr))].copy()
        ## NOTE NO LE REALIZO EL REMPLAZO EN LA CLASIFICACION, POR QUE YA LO TRAE POR DEFECTO


        # NOTE CONCATENAMOS LOS FILTROS GLOBALES
        df2 = pd.concat([ci, concesionarios, garantia, plm,clientes_generales], join='inner')

        # # NOTE CLASIFICACIONES DEL VENDEDOR

        # # Sucursal	A	A
        # # REYNOSA	Servicio	Servicio Reynosa
        # # NUEVO LAREDO (AEROPUERTO)	Servicio	Servicio NL Aereopuerto
        # # NUEVO LAREDO (MATRIZ)	Servicio	Servicio NL Matriz
        # # PIEDRAS NEGRAS	Servicio	Servicio Piedras Negras
        # # MATAMOROS	Servicio	Servicio Matamoros
        # # ![image.png](attachment:image.png)
        # # 
        # # NOTE FILTROS PARA SERVICIO, ESTO ES A TODA LA DATA SIN FILTRAR OTRA COLUMNA.
        n = (df2['Sucursal'] == 'REYNOSA')
        reynosa = df2[n].copy()
        reynosa['DepaVenta'] ='Servicio'
        reynosa['Depa'] = 'Servicio Reynosa'

        n = (df2['Sucursal'] == 'NUEVO LAREDO (AEROPUERTO)')
        nla = df2[n].copy()
        nla['DepaVenta'] = 'Servicio'
        nla['Depa'] = 'Servicio NL Aereopuerto'

        n = (df2['Sucursal'] == 'NUEVO LAREDO (MATRIZ)')
        nlm = df2[n].copy()
        nlm['DepaVenta'] = 'Servicio'
        nlm['Depa'] = 'Servicio NL Matriz'

        n = (df2['Sucursal'] == 'PIEDRAS NEGRAS')
        pn = df2[n].copy()
        pn['DepaVenta'] = 'Servicio'
        pn['Depa'] = 'Servicio Piedras Negras'

        n = (df2['Sucursal'] == 'MATAMOROS')
        mata = df2[n].copy()
        mata['DepaVenta'] = 'Servicio'
        mata['Depa'] = 'Servicio Matamoros'
        
        n = (df2['Sucursal'] == 'POZA RICA')
        PozaR = df2[n].copy()
        PozaR['DepaVenta'] = 'Servicio'
        PozaR['Depa'] = 'Servicio Poza Rica'

        dfServicio = pd.concat([reynosa, nla, nlm, pn, mata, PozaR], join='inner')

        # # NOTE FILTRAMOS LA COLUMNA DE 'TIPO SERVICIO' PARA CLASIFICAR LOS DEMAS DEPARTAMENTOS.

        # # FILTRO Servicio TM		
        # # Sucursal	A	A
        # # REYNOSA	Taller Movil	TM Reynosa
        # # NUEVO LAREDO (AEROPUERTO)	Taller Movil	TM NL Aereopuerto
        # # MATAMOROS	Taller Movil	TM Matamoros
        # # NUEVO LAREDO (MATRIZ)	Taller Movil	TM NL Matriz
        # # ![image.png](attachment:image.png)

        # # NOTE Cambiamos el titulo de la columna.
        dfServicio = dfServicio.rename(columns={ 'Tipo Servicio': 'Tipop', 'Número Orden':'NO','Unidad':'U'})

        # NOTE Mandamos a traer todo lo que sea TM

        a = ['TM' ,'Taller Movil']

        TM = dfServicio[dfServicio.Tipop.str.contains('|'.join(a), na=False)].copy()

        # NOTE Creamos las clasificaciones de TM
        n = (TM['Sucursal'] == 'REYNOSA')
        tm_reynosa = TM[n].copy()
        tm_reynosa['DepaVenta'] = 'Taller Movil'
        tm_reynosa['Depa'] = "TM Reynosa"

        n = (TM['Sucursal'] == 'NUEVO LAREDO (AEROPUERTO)')
        tm_aeropuerto = TM[n].copy()
        tm_aeropuerto['DepaVenta'] = 'Taller Movil'
        tm_aeropuerto['Depa'] = "TM NL Aereopuerto"

        n = (TM['Sucursal'] == 'MATAMOROS')
        tm_mata = TM[n].copy()
        tm_mata['DepaVenta'] = 'Taller Movil'
        tm_mata['Depa'] = "TM Matamoros"

        n = (TM['Sucursal'] == 'NUEVO LAREDO (MATRIZ)')
        tm_nlm = TM[n].copy()
        tm_nlm['DepaVenta'] = 'Taller Movil'
        tm_nlm['Depa'] = "TM NL Matriz"


        # NOTE Concatenamos las clasificaciones
        df_tm = pd.concat([tm_reynosa, tm_aeropuerto, tm_mata, tm_nlm], join = 'inner').copy()

        # # NOTE OBTENEMOS LA DATA DE LOS DOS TIPOS DE DEPARTAMENTOS
        df_Ser = dfServicio[~dfServicio.Tipop.str.contains('|'.join(a), na=False)].copy()

        df_Final = pd.concat([df_tm, df_Ser], join = 'inner').copy()

        # # NOTE Regresamos el titulo de la columna a su nombre original
        df_Final = df_Final.rename(columns={ 'Tipop': 'Tipo Servicio'})
        # NOTE Creamos la columna con la fecha actual
        df_Final.insert(
                loc = 10,
                column = 'Fecha Movimiento',
                value = Variables().date_movement_config_document(),
                allow_duplicates = False
            )


        # NOTE INTENTAMOS HACER LOS CAMBIOS DE FORMATO PARA LAS FECHAS EN PYTHON
        for column_title in df_Final:
            if ('Fecha' in column_title):
                try:
                    df_Final[column_title] = (df_Final[column_title].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass
        df_Final.insert(
            loc = 25,
            column = "Número Orden",
            value = 'OS' + df_Final['NO'].map(str).str.split('.').str[0],
            allow_duplicates = False
        )
        df_Final.insert(
            loc = 28,
            column = 'Unidad',
            value = 'UN-' + df_Final['U'].map(str).str.split('.').str[0],
            allow_duplicates = False
        )
        #------------
        #note creamos la clasificacion de la columna de area
        df_Final["Dias Laborales"] = "" # primero la columa de "dias laborales"
        df_Final.loc[(df_Final["DepaVenta"] == "Taller Movil"), "Area"] = "MO Taller Movil"
        df_Final.loc[(df_Final["DepaVenta"] == "Servicio"), "Area"] = "MO Servicio"
        # ----------------
        # NOTE ELIMINAMOS LAS COLUMNAS QUE NO SE OCUPAN
        df_Final.drop(['Hora Docto.','NO','U','Fecha Cancelación','Categoría','Id. Paquete','Paquete','Descripción Paquete','Cantidad Paquete','Saldo'], axis=1, inplace=True)
        
        columnas_bol=df_Final.select_dtypes(include=bool).columns.tolist()
        df_Final[columnas_bol] = df_Final[columnas_bol].astype(str)
        
        # NOTE EXPORTAMOS EL ARCHIVO
        df_Final.to_excel(os.path.join(Variables().ruta_procesados,f'KWRB_ServicioDetallado_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)