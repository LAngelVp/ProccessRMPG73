#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
#importamos librerias
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class PagosClientes(Variables):
    def __init__(self):

        self.nombre_doc = 'PCR.xlsx'
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.ruta = os.path.join(Variables().ruta_deapoyo, "JsonObjetivos.json")
        

        self.columnas_objetivo = []
        self.objetivos = pd.DataFrame()
        #obtenemos el parth.
        #leemos el documento.
        path = os.path.join(Variables().ruta_Trabajos_kwrb, self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        #copiamos la data para no afectar la original.
        d = df.copy()

        #Eliminamos las columnas que no se van a ocupar.
        d.drop({'Hora Pago', 'Referencia', 'Días Plazo', 'DocumentoMSC', 'Observaciones Pago', 'Referencia Forma de Pago', 'Sucursal Responsable'}, axis=1, inplace=True)
        #d = d.rename(columns={'Tipo_Docto.':'Tipo Docto'})

        # damos formato a todas las cabeceras de las columnas.
        # recordar volver a la normalidad.
        d.columns = d.columns.str.replace(' ', '_')

        #insertamos columna de "Fecha Movimiento"
        d.insert(
            loc=4,
            column='Fecha_Movimiento',
            value=Variables().date_movement_config_document(),
            allow_duplicates=False
            )

        # Recorremos todo el contenido de la columna de "Cuenta Bancaria".
        # si el contenido que encuentre es "digito", solo continuara.
        # si encuentra algo que no sea digito, lo remplazara por el digito 0.
        for dato in d['CuentaBancaria']:
            try:
                if (dato.isdigit() == True ):
                    continue
                else:
                    d['CuentaBancaria'] = d['CuentaBancaria'].replace(dato,0)
            except:
                pass

        # creamos un ciclo en donde recorra todas las cabeceras y si encuentra,
        # "Sucursal_Factura", creaa una columna despues con el nombre de "CLASS_SUCURSAL".
        x = 0
        for columnas in d:
            if (columnas == 'Sucursal_Factura' ):
                d.insert(
                loc = (x + 1),
                column = 'CLASS_SUCURSAL',
                value = 'OTROS',
                allow_duplicates = False
                )
                break
            else:
                pass
            x = x + 1

        # creamos la columna de objetivo al final del data con los valores de 0.
        d['Objetivo'] = 0

        #--------------------------------Dividimos el dataframe en "CREDITO Y CONTADO"-----------------------------------

        credito = d["Forma_Pago_Factura"] == "Crédito"
        contado = d["Forma_Pago_Factura"] == "Contado"

        #---------------------------------Comenzamos a clasificar el apartado de CREDITO------------------------------

        # NOTA DE CARGO
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Tipo_Docto."] == "Nota de cargo"),
            "CLASS_SUCURSAL",
        ] = "12 NOTA DE CARGO"
        d.loc[
            (credito)
            & (d["Cliente_Pago"] == "RECICLADORA INDUSTRIAL DE ACUMULADORES"),
            "CLASS_SUCURSAL",
        ] = "12 NOTA DE CARGO"

        # PACLEASE
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Cliente_Pago"].isin(["PACLEASE MEXICANA","PACCAR FINANCIAL MEXICO"]))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "11 PACLEASE"

        # PACCAR PARTS
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Cliente_Pago"].str.contains("PACCAR PARTS MEXICO"))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO", "ADMINISTRACION"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "09 GARANTIAS PACCAR PARTS"

        # ALESSO
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Cliente_Pago"].str.contains("ALESSO"))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO", "ADMINISTRACION"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "08 ALESSO"

        # KENMEX
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Cliente_Pago"].str.contains("KENWORTH MEXICANA"))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO", "ADMINISTRACION"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "07 GARANTIAS KENMEX"

        # CLIENTE ESPECIAL
        d.loc[
            (credito)
            & (d["Id_Cliente_Pago"].isin([552,799,1357,1362,1171,1170,1169,1517,557,1259,1514]))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "05 CLIENTE ESPECIAL"

        # PIEDRAS NEGRAS
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "GUADALUPE JUAREZ")
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "04 PIEDRAS NEGRAS"

        # MATAMOROS
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "ELIZABETH GONZALEZ FERNANDEZ")
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "03 MATAMOROS"

        # REYNOSA
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "ALEYDA DE LA CRUZ MENDOZA")
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "02 REYNOSA"

        # NUEVO LAREDO
        d.loc[
            (credito)
            & (d["Usuario_Aplicó"].isin(["LESLY MARTINEZ MARTINEZ PARTIDA","VIVIAN IVETTE ROJO GARCIA"]))
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "01 NUEVO LAREDO"

        #---------------------------------------Terminamos con el apartado de CREDITO---------------------------------

        #---------------------------------------Comenzamos con "CONTADO"------------------------------

        # CONTADO
        d.loc[
            (contado)
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"])),
            "CLASS_SUCURSAL",
        ] = "06 CONTADO"

        #---------------------------------------Terminamos con "CONTADO"------------------------------

        data = self.fila_objetivo(d)

        for fecha in data:
            if ("Fecha" in fecha):
                try:
                    data[fecha] = pd.to_datetime(data[fecha] , errors = 'coerce')
                    data[fecha] = (data[fecha].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass

        columnas_bol=data.select_dtypes(include=bool).columns.tolist()
        data[columnas_bol] = data[columnas_bol].astype(str)

        if os.path.exists(self.ruta):
            try:
                df_json = pd.read_json(self.ruta)
                for indice, fila in df_json.iterrows():
                    sucursal_json = fila["Sucursal"]
                    objetivo_json = fila["Objetivo"]

                    # Verificar si la sucursal del JSON coincide con la sucursal en df

                    if sucursal_json in data["CLASS_SUCURSAL"].values.tolist():
                        # Actualizar el valor de "Objetivos" en data
                        data.loc[data["CLASS_SUCURSAL"] == sucursal_json, "Objetivo"] = objetivo_json
                    
                    else:
                        pass
            except:
                pass
        
        # damos formato a todas las cabeceras de las columnas.
        # recordar volver a la normalidad.
        data.columns = data.columns.str.replace('_', ' ')


        
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        Variables().guardar_datos_dataframe(self.nombre_doc, data, self.concesionario)

        #---------------------------Terminamos de filtrar contado-------------------------

    def fila_objetivo(self, dataframe_completo):
        for i in dataframe_completo.columns:
            nombre_columna = i
            if (dataframe_completo[nombre_columna].dtypes == "object") and (nombre_columna == "Usuario_Aplicó"):
                self.objetivos[nombre_columna] = ['DANIA VARGAS ROSAS']

            elif (dataframe_completo[nombre_columna].dtypes == "object") and (nombre_columna == "CLASS_SUCURSAL"):
                self.objetivos[nombre_columna] = ['Objetivo']

            elif (dataframe_completo[nombre_columna].dtypes == "object") and (nombre_columna == "Departamento"):
                self.objetivos[nombre_columna] = ['KWRB']

            elif (dataframe_completo[nombre_columna].dtypes == "int64"):
                self.objetivos[nombre_columna] = ['0']

            elif (dataframe_completo[nombre_columna].dtypes == "float64"):
                self.objetivos[nombre_columna] = ['0.0']

            elif (nombre_columna == "Mes"):
                self.objetivos[nombre_columna] = Variables().nombre_mes()

            elif (nombre_columna == "Fecha_Pago") or (nombre_columna == "Fecha_Movimiento"):
                self.objetivos[nombre_columna] = [Variables().date_movement_config_document()]

            else:
                self.objetivos[nombre_columna] = ['']

        DataFrameConObjetivo = pd.concat([dataframe_completo, self.objetivos], join="inner")
        return DataFrameConObjetivo