#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
class TrabajosPorEstado(Variables):
    def __init__(self):
        # obtenemos el path.
        # leemos el documento.
        exceptoKenworth=["KENWORTH MEXICANA", "KENWORTH DEL ESTE"]
        registros_excluir = ['KENWORTH', 'PACCAR PARTS MEXICO','ALESSO','PACCAR FINANCIAL MEXICO','PACLEASE MEXICANA']
        registroos_tallerMovil = ['TM', 'Taller Movil']
        registroos_exceptoTipoServicio = ['Rescate Avalado','Rescate Carretero','TM', 'Taller Movil']
        excepto_estadoTrabajo = ["Facturado", "Cancelado"]
        #------------------------------------------------------
        self.nombre_doc = 'TER.xlsx'
        path = os.path.join(Variables().ruta_Trabajo, self.nombre_doc)
        df = pd.read_excel(path, sheet_name = "Hoja2")

        df1 = df.copy()

        df1 = df1.rename(columns={'Fecha Trabajo':'FT','Cliente Trabajo':'Cliente','Número Orden':'NO', 'Unidad':'U', 'Estado Trabajo':'ET', 'Estado Reclamo':'ER'})

        df1 = df1.replace(to_replace=';', value='-', regex=True)

        df1.insert(loc=19, column="Número Orden", value = "OS" + df1["NO"].map(str), allow_duplicates = False)
        df1.insert(loc = 23, column = "Unidad", value = "UN-" + df1["U"].map(str), allow_duplicates = False)
        df1.insert(loc = 5,column = 'Clasificacion Cliente',value = 'CLIENTES GENERALES',allow_duplicates = False)

        kenworths_concesionarios = df1.query("Cliente.str.contains('KENWORTH') and not Cliente.str.contains('|'.join(@exceptoKenworth))", local_dict={'exceptoKenworth': exceptoKenworth}).copy()
        kenworths_concesionarios["Clasificacion Cliente"] = "CONCESIONARIOS"

        garantia=df1.query("Cliente == ['KENWORTH MEXICANA', 'ALESSO', 'PACCAR PARTS MEXICO']").copy()
        garantia["Clasificacion Cliente"] = "GARANTIA"

        plm = df1.query("Cliente == ['PACCAR FINANCIAL MEXICO', 'PACLEASE MEXICANA']").copy()
        plm["Clasificacion Cliente"] = "PLM"

        ci = df1.query("Cliente == ['KENWORTH DEL ESTE']").copy()
        ci["Clasificacion Cliente"] = "CI"

        clientesGenerales = df1.query("~Cliente.str.contains('|'.join(@registros_excluir))", local_dict={'registros_excluir': registros_excluir}).copy()
        clientesGenerales["Clasificacion Cliente"] = "CLIENTES GENERALES"

        df_clasificado_cliente = pd.concat([kenworths_concesionarios,garantia,plm,ci,clientesGenerales], join="inner").copy()

        df_clasificado_cliente = df_clasificado_cliente.rename(columns={'Clasificacion Cliente':'CL','Tipo Servicio':'Tipop'})
        df_exceptoGarantia = df_clasificado_cliente.query("CL != ['GARANTIA']")
        df_soloGarantia = df_clasificado_cliente.query("CL == ['GARANTIA']")

        
        
        df_rescateAvalado = df_exceptoGarantia.query("Tipop == ['Rescate Avalado']").copy()
        df_rescateAvalado["CL"] = "RESCATES AVALADOS"
        df_rescateCarretero = df_exceptoGarantia.query("Tipop == ['Rescate Carretero']").copy()
        df_rescateCarretero["CL"] = "RESCATES CARRETEROS"
        df_tallerMovil = df_exceptoGarantia.query("Tipop.str.contains('|'.join(@registroos_tallerMovil))", local_dict={'registroos_tallerMovil': registroos_tallerMovil}).copy()
        df_tallerMovil["CL"] = "TALLER MOVIL"

        df_noClasificadosTipoServicio = df_exceptoGarantia.query("~Tipop.str.contains('|'.join(@registroos_exceptoTipoServicio))", local_dict={'registroos_exceptoTipoServicio': registroos_exceptoTipoServicio})

        
        df_filtro_estadoTrabajo_conDatos = df_soloGarantia.query("~ET.str.contains('|'.join(@excepto_estadoTrabajo))", local_dict={'excepto_estadoTrabajo': excepto_estadoTrabajo})
        df_filtro_estadoTrabajo_excepto = df_soloGarantia.query("ET.str.contains('|'.join(@excepto_estadoTrabajo))", local_dict={'excepto_estadoTrabajo': excepto_estadoTrabajo})


        df_filtro_estadoReclamo_Vacias = df_filtro_estadoTrabajo_conDatos.query("ER.isna()").copy()
        df_filtro_estadoReclamo_noVacias = df_filtro_estadoTrabajo_conDatos.query("ER.notna()")
        df_filtro_estadoReclamo_Vacias["ER"]="Sin Tramitar"
        df_Estado_ReclamoCompleto = pd.concat([df_filtro_estadoReclamo_Vacias,df_filtro_estadoReclamo_noVacias], join="inner")

        df_Estado_Trabajo_GarantiaFiltrada = pd.concat([df_Estado_ReclamoCompleto, df_filtro_estadoTrabajo_excepto], join="inner")

        df_clasificadoPorTiposervicio = pd.concat([df_Estado_Trabajo_GarantiaFiltrada,df_rescateAvalado,df_rescateCarretero,df_tallerMovil,df_noClasificadosTipoServicio], join="inner")

        df_clasificadoPorTiposervicio.insert(loc = 3,column = "Hoy",value = Variables().fechaInsertar,allow_duplicates = False)
        df_clasificadoPorTiposervicio['FT'] = pd.to_datetime(df_clasificadoPorTiposervicio.FT, format='%d/%m/%Y')
        df_clasificadoPorTiposervicio['Hoy'] = pd.to_datetime(df_clasificadoPorTiposervicio.Hoy, format='%d/%m/%Y')
        df_clasificadoPorTiposervicio.insert(loc = 4,column = 'Antigüedad',value = df_clasificadoPorTiposervicio['Hoy'] - df_clasificadoPorTiposervicio['FT'],allow_duplicates = False)
        df_clasificadoPorTiposervicio['Antigüedad'] = pd.to_numeric(df_clasificadoPorTiposervicio['Antigüedad'].dt.days, downcast='integer')
        df_clasificadoPorTiposervicio.drop(['Hoy','NO','U'], axis=1, inplace=True)
        df_clasificadoPorTiposervicio = df_clasificadoPorTiposervicio.rename(columns={'FT':'Fecha Trabajo','Cliente':'Cliente Trabajo','CL':'Clasificacion Cliente','ET':'Estado Trabajo','ER':'Estado Reclamo','Tipop':'Tipo Servicio'})

        for column_title in df_clasificadoPorTiposervicio:
            if ('Fecha' in column_title):
                try:
                    df_clasificadoPorTiposervicio[column_title] = (df_clasificadoPorTiposervicio[column_title].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass
            
        columnas_bol=df_clasificadoPorTiposervicio.select_dtypes(include=bool).columns.tolist()
        df_clasificadoPorTiposervicio[columnas_bol] = df_clasificadoPorTiposervicio[columnas_bol].astype(str)
        
        if (os.path.basename(Variables().comprobar_reporte_documento_rutas(self.nombre_doc)).split(".")[1] == self.nombre_doc.split(".")[1]):
            df_clasificadoPorTiposervicio.to_excel(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), index=False )
        else:
            df_clasificadoPorTiposervicio.to_csv(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), encoding="utf-8", index=False )
