#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import*
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from .Variables.ContenedorVariables import Variables
class Refacciones(Variables):
    def RefaccionesKWRB(self):
        path = os.path.join(Variables().ruta_Trabajo,'RR.xlsx')

        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        
        df.drop(['% Margen', 'Meta Ventas Por Vendedor', 'Meta Margen Por Vendedor', 'Meta Cantidad Por Vendedor', 'Meta Ventas Por Sucursal', 'Meta Margen Por Sucursal', 'Meta Cantidad Por Sucursal', '% Comisión Por Margen', '% Comisión Por Ventas', 'Comisión Por Margen', 'Comisión Por Ventas', 'EsBonificacion', 'IdUsuario', 'IdPaquete', 'Paquete', 'Descripción Paquete', 'Cantidad Paquete', 'Subtotal Paquete', 'Potencial Total', 'Tipo de Cambio del día', 'OCCliente', '% Margen Sin Descuento'], axis=1, inplace=True)

        df_nuevo = df[df.columns[0:93]].copy()

        df_nuevo['Fecha'] = (df_nuevo['Fecha'].dt.strftime('%d/%m/%Y'))

        RefaccionesM = df_nuevo['DepartamentoDocto'] == 'REFACCIONES'
        df_REFACCIONESMost = df_nuevo[RefaccionesM].copy()

        RefaccionesS = df_nuevo['DepartamentoDocto'] == 'TALLER DE SERVICIO'
        df_REFACCIONESServ = df_nuevo[RefaccionesS].copy()


        # note CLASIFICACION "REFACCIONES MOSTRADOR"
        #### FILTRAMOS POR SUCURSALES PARA PONER SU CLASIFICACION.
        # Sucursal                      Departamento Venta              Depa
        # REYNOSA	                    | Mostrado Reynosa              | Mostrador
        # NUEVO LAREDO (AEROPUERTO)     | Mostrador NL Aeropuerto	    | Mostrador
        # TRP NUEVO LAREDO              | Mostrador TRP Nuevo Laredo    | Mostrador
        # TRP REYNOSA	                | Mostrador TRP Reynosa	        | Mostrador
        # PIEDRAS NEGRAS	            | Mostrador Piedras Negras      | Mostrador
        # MATAMOROS	                    | Mostrador Matamoros           | Mostrador
        # VALLE HERMOSO	                | Mostrador Valle Hermoso       | Mostrador
        # TRP NAVA	                    | Mostrador TRP Nava            | Mostrador
        # NUEVO LAREDO (MATRIZ)	        | Mostrador NL Matriz           | Mostrador
        # POZA RICA	                    | Mostrador Poza Rica           | Mostrador
        # TRP ACUÑA	                    | Mostrador TRP Acuña           | Mostrador

        ReynosaM_Depas = df_REFACCIONESMost['Sucursal'] == 'REYNOSA'
        Reynosa = df_REFACCIONESMost[ReynosaM_Depas].copy()
        Reynosa["Departamento Venta"] = "Mostrado Reynosa"
        Reynosa["Depa"] = "Mostrador"

        NuevoLaredoA_Depas = df_REFACCIONESMost['Sucursal'] == 'NUEVO LAREDO (AEROPUERTO)'
        NuevoLaredo_Aero = df_REFACCIONESMost[NuevoLaredoA_Depas].copy()
        NuevoLaredo_Aero["Departamento Venta"] = "Mostrador NL Aeropuerto"
        NuevoLaredo_Aero["Depa"] = "Mostrador"

        Trp_NuevoLaredo_Depas = df_REFACCIONESMost['Sucursal'] == 'TRP NUEVO LAREDO'
        NLaredo_TRP = df_REFACCIONESMost[Trp_NuevoLaredo_Depas].copy()
        NLaredo_TRP['Departamento Venta'] = 'Mostrador TRP Nuevo Laredo'
        NLaredo_TRP['Depa'] = 'Mostrador'

        trp_reynosa = df_REFACCIONESMost['Sucursal'] == 'TRP REYNOSA'
        trpReynosa = df_REFACCIONESMost[trp_reynosa].copy()
        trpReynosa['Departamento Venta'] = 'Mostrador TRP Reynosa'
        trpReynosa['Depa'] = 'Mostrador'

        piedras_negras = df_REFACCIONESMost['Sucursal'] == 'PIEDRAS NEGRAS'
        PiedrasNegras = df_REFACCIONESMost[piedras_negras].copy()
        PiedrasNegras['Departamento Venta'] = 'Mostrador Piedras Negras'
        PiedrasNegras['Depa'] = 'Mostrador'

        Matamoros = df_REFACCIONESMost['Sucursal'] == 'MATAMOROS'
        Matamoros_Depas = df_REFACCIONESMost[Matamoros].copy()
        Matamoros_Depas['Departamento Venta'] = 'Mostrador Matamoros'
        Matamoros_Depas['Depa'] = 'Mostrador'

        valle_hermoso = df_REFACCIONESMost['Sucursal'] == 'VALLE HERMOSO'
        ValleHermoso = df_REFACCIONESMost[valle_hermoso].copy()
        ValleHermoso['Departamento Venta'] = 'Mostrador Valle Hermoso'
        ValleHermoso['Depa'] = 'Mostrador'

        TRP_NAVA = df_REFACCIONESMost['Sucursal'] == 'TRP NAVA'
        TRPNAVA = df_REFACCIONESMost[TRP_NAVA].copy()
        TRPNAVA['Departamento Venta'] = 'Mostrador TRP Nava'
        TRPNAVA['Depa'] = 'Mostrador'

        nuevolaredom = df_REFACCIONESMost['Sucursal'] == 'NUEVO LAREDO (MATRIZ)'
        NuevoLaredoM = df_REFACCIONESMost[nuevolaredom].copy()
        NuevoLaredoM['Departamento Venta'] = 'Mostrador NL Matriz'
        NuevoLaredoM['Depa'] = 'Mostrador'

        POZA_RICA = df_REFACCIONESMost['Sucursal'] == 'POZA RICA'
        POZARICA = df_REFACCIONESMost[POZA_RICA].copy()
        POZARICA['Departamento Venta'] = 'Mostrador Poza Rica'
        POZARICA['Depa'] = 'Mostrador'


        TRP_ACUÑA = df_REFACCIONESMost['Sucursal'] == 'TRP ACUÑA'
        TRPACUÑA = df_REFACCIONESMost[TRP_ACUÑA].copy()
        TRPACUÑA['Departamento Venta'] = 'Mostrador TRP Acuña'
        TRPACUÑA['Depa'] = 'Mostrador'


        # comment CONCATENAMOS TODOS LOS FILTROS DE "REFACCIONES MOSTRADOR"
        DF_RMOSTRADOR = pd.concat([Reynosa, NuevoLaredo_Aero, NLaredo_TRP, trpReynosa, PiedrasNegras, Matamoros_Depas, ValleHermoso, TRPNAVA, NuevoLaredoM, POZARICA, TRPACUÑA], join = "inner")


        # note CLASIFICACION "REFACCIONES SERVICIO"

        # Sucursal    	            Departamento Venta         Depa
        # REYNOSA	                |Servicio Reynosa	       |Servicio
        # PIEDRAS NEGRAS	        |Servicio Piedras Negras   |Servicio
        # NUEVO LAREDO (AEROPUERTO) |Servicio NL Aeropuerto	   |Servicio
        # MATAMOROS	                |Servicio Matamoros	       |Servicio
        # NUEVO LAREDO (MATRIZ)	    |Servicio NL Matriz	       |Servicio

        REYNOSA_serv = df_REFACCIONESServ['Sucursal'] == 'REYNOSA'
        REYNOSAserv = df_REFACCIONESServ[REYNOSA_serv].copy()
        REYNOSAserv['Departamento Venta'] = 'Servicio Reynosa'
        REYNOSAserv['Depa'] = 'Servicio'

        PIEDRAS_NEGRAS_serv = df_REFACCIONESServ['Sucursal'] == 'PIEDRAS NEGRAS'
        PIEDRAS_NEGRASserv = df_REFACCIONESServ[PIEDRAS_NEGRAS_serv].copy()
        PIEDRAS_NEGRASserv['Departamento Venta'] = 'Servicio Piedras Negras'
        PIEDRAS_NEGRASserv['Depa'] = 'Servicio'

        NUEVO_LAREDO_Aero_serv = df_REFACCIONESServ['Sucursal'] == 'NUEVO LAREDO (AEROPUERTO)'
        NUEVOLAREDOAeroserv = df_REFACCIONESServ[NUEVO_LAREDO_Aero_serv].copy()
        NUEVOLAREDOAeroserv['Departamento Venta'] = 'Servicio NL Aeropuerto'
        NUEVOLAREDOAeroserv['Depa'] = 'Servicio'

        MATAMOROS_serv = df_REFACCIONESServ['Sucursal'] == 'MATAMOROS'
        MATAMOROSserv = df_REFACCIONESServ[MATAMOROS_serv].copy()
        MATAMOROSserv['Departamento Venta'] = 'Servicio Matamoros'
        MATAMOROSserv['Depa'] = 'Servicio'

        NUEVO_LAREDO_M = df_REFACCIONESServ['Sucursal'] == 'NUEVO LAREDO (MATRIZ)'
        NUEVOLAREDOMserv = df_REFACCIONESServ[NUEVO_LAREDO_M].copy()
        NUEVOLAREDOMserv['Departamento Venta'] = 'Servicio NL Matriz'
        NUEVOLAREDOMserv['Depa'] = 'Servicio'
        
        POZA_RICA = df_REFACCIONESServ['Sucursal'] == 'POZA RICA'
        POZARICA = df_REFACCIONESServ[POZA_RICA].copy()
        POZARICA['Departamento Venta'] = 'Servicio Poza Rica'
        POZARICA['Depa'] = 'Servicio'

        DF_RSERVICIO = pd.concat([REYNOSAserv, PIEDRAS_NEGRASserv, NUEVOLAREDOAeroserv, MATAMOROSserv, NUEVOLAREDOMserv, POZARICA], join = "inner")

        DF_RefaccionesCompleto = pd.concat([DF_RMOSTRADOR, DF_RSERVICIO], join = "inner")
        
        columnas_bol=DF_RefaccionesCompleto.select_dtypes(include=bool).columns.tolist()
        DF_RefaccionesCompleto[columnas_bol] = DF_RefaccionesCompleto[columnas_bol].astype(str)

        DF_RefaccionesCompleto.to_excel(os.path.join(Variables().ruta_procesados,f'KWRB_Refacciones_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)