#########################
# DESARROLLADOR
# LUIS ANGEL VALLEJO PEREZ
#########################
#importamos librerias
import os
import pandas as pd
from datetime import *
from .Variables.ContenedorVariables import Variables
class PagosClientes(Variables):
    def Pagos_Clientes_KWRB(self):

        self.ruta = os.path.join(Variables().ruta_deapoyo, "JsonObjetivos.json")
        

        self.columnas_objetivo = []
        self.objetivos = pd.DataFrame()
        fecha = Variables().fechaHoy()
        fechainsertar = str(fecha)
        #obtenemos el parth.
        #leemos el documento.
        path = os.path.join(Variables().ruta_Trabajo,'PCR.xlsx')
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        #copiamos la data para no afectar la original.
        df1 = df.copy()

        #Eliminamos las columnas que no se van a ocupar.
        df1.drop({'Hora Pago', 'Referencia', 'Días Plazo', 'DocumentoMSC', 'Observaciones Pago', 'Referencia Forma de Pago', 'Sucursal Responsable'}, axis=1, inplace=True)
        df1 = df1.rename(columns={'Tipo Docto.':'Tipo Docto'})

        # damos formato a todas las cabeceras de las columnas.
        # recordar volver a la normalidad.
        df1.columns = df1.columns.str.replace(' ', '_')

        #insertamos columna de "Fecha Movimiento"
        df1.insert(
            loc=4,
            column='Fecha_Movimiento',
            value=Variables().fechaInsertar,
            allow_duplicates=False
            )

        # Recorremos todo el contenido de la columna de "Cuenta Bancaria".
        # si el contenido que encuentre es "digito", solo continuara.
        # si encuentra algo que no sea digito, lo remplazara por el digito 0.
        for dato in df1['CuentaBancaria']:
            try:
                if (dato.isdigit() == True ):
                    continue
                else:
                    df1['CuentaBancaria'] = df1['CuentaBancaria'].replace(dato,0)
            except:
                pass

        # creamos un ciclo en donde recorra todas las cabeceras y si encuentra,
        # "Sucursal_Factura", creaa una columna despues con el nombre de "Class_Sucursal".
        x = 0
        for columnas in df1:
            if (columnas == 'Sucursal_Factura' ):
                df1.insert(
                loc = (x + 1),
                column = 'Class_Sucursal',
                value = 'OTROS',
                allow_duplicates = False
                )
                break
            else:
                pass
            x = x + 1

        # creamos la columna de objetivo al final del data con los valores de 0.
        df1['Objetivo'] = 0

        #--------------------------------Dividimos el dataframe en "CREDITO Y CONTADO"-----------------------------------

        # creamos una variable auxiliar donde se almacenara lo que sea credito.
        df_auxiliar_credito = df1['Forma_Pago_Factura'] == 'Crédito'
        # creamos un data que sea solo del filtro "Credito".
        df_credito = df1[df_auxiliar_credito].copy()
        # creamos una variable auxiliar que almacene lo de contado.
        df_auxiliar_contado = df1.Forma_Pago_Factura == 'Contado'
        # creamos el dataframe que sea de "Contado".
        df_contado = df1[df_auxiliar_contado].copy()

        #---------------------------------Comenzamos a clasificar el apartado de CREDITO------------------------------

        # creamos un data en donde se almacenen todos los registros solicitados.
        df_clientes_espececiales = df_credito.loc[df_credito.Id_Cliente_Pago.isin([1170, 1259, 1362, 1514, 1580, 552, 557, 1171, 1169, 1517])]
        #-------------------------------------------------
        # modificamos los valores que estan en la columna de "Class_Sucursal" del data de credito.
        df_clientes_espececiales.Class_Sucursal = df_clientes_espececiales.Class_Sucursal.replace({'OTROS':'05 CLIENTE ESPECIAL'})

        # creamos un data con todo el contenido que no sea lo que se especifica, con el objetivo de solo modificar,
        # por partes y concatenarlo mas adelante.
        df_sin_clientes_especiales = df_credito[~df_credito.Id_Cliente_Pago.isin([1170, 1259, 1362, 1514, 1580, 552, 557, 1171, 1169, 1517])]

        # concatenamos los dos dataframe para volver a tener lo mismo que en comienzo (EL TOTAL DE REGISTROS DE CREDITO).
        df_clientes_especiales_FILTRADOS = pd.concat([df_sin_clientes_especiales, df_clientes_espececiales], join='inner')

        # NUEVO LAREDO
        # realizamos la clasificacion de "NUEVO LAREDO"...
        # cabe mencionar que se obtendran dataframes de todos los registros del vendedor "lesly y vivian"
        df_NL1 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['VIVIAN IVETTE ROJO GARCIA', 'LESLY MARTINEZ MARTINEZ PARTIDA'] and Class_Sucursal == '05 CLIENTE ESPECIAL'")
        df_NL2 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['VIVIAN IVETTE ROJO GARCIA', 'LESLY MARTINEZ MARTINEZ PARTIDA'] and Class_Sucursal == 'OTROS' and FormaPagoDelPago == ['CHEQUE','DEPÓSITO','EFECTIVO','TARJETA']")
        # realizamos la clasificacion de todos los registros que van a ser "nuevo laredo".
        df_NL2.Class_Sucursal = df_NL2.Class_Sucursal.replace({'OTROS':'01 NUEVO LAREDO'})
        df_NL3 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['VIVIAN IVETTE ROJO GARCIA', 'LESLY MARTINEZ MARTINEZ PARTIDA'] and Class_Sucursal == 'OTROS' and FormaPagoDelPago != ['CHEQUE','DEPÓSITO','EFECTIVO', 'TARJETA']")
        # creamos el dataframe de todo lo que es "lesly y vivian"
        df_NUEVO_LAREDO = pd.concat([df_NL1,df_NL2,df_NL3], join="inner")

        # REYNOSA
        # realizamos la clasificacion de toda la data de "reynosa"...
        # cabe mencionar que se obtendran dataframes de todos los registros del vendedor "aleyda"
        df_R1 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['ALEYDA DE LA CRUZ MENDOZA'] and Class_Sucursal == 'OTROS' and FormaPagoDelPago == ['CHEQUE', 'DEPÓSITO', 'EFECTIVO', 'TARJETA']")
        df_R1.Class_Sucursal = df_R1.Class_Sucursal.replace({'OTROS':'02 REYNOSA'})
        df_R2 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['ALEYDA DE LA CRUZ MENDOZA'] and Class_Sucursal == '05 CLIENTE ESPECIAL'")
        df_R3 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['ALEYDA DE LA CRUZ MENDOZA'] and Class_Sucursal == 'OTROS' and FormaPagoDelPago != ['CHEQUE', 'DEPÓSITO', 'EFECTIVO', 'TARJETA']")
        df_REYNOSA = pd.concat([df_R1, df_R2, df_R3], join="inner")

        # PIEDRAS NEGRAS
        # realizamos la clasificacion de toda la data de "piedras negras"...
        # cabe mencionar que se obtendran dataframes de todos los registros del vendedor "guadalupe"
        df_PN1 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['GUADALUPE JUAREZ'] and Class_Sucursal == 'OTROS' and FormaPagoDelPago == ['CHEQUE', 'DEPÓSITO', 'EFECTIVO', 'TARJETA']")
        df_PN1.Class_Sucursal = df_PN1.Class_Sucursal.replace({'OTROS':'04 PIEDRAS NEGRAS'})
        df_PN2 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['GUADALUPE JUAREZ'] and Class_Sucursal == '05 CLIENTE ESPECIAL'")
        df_PN3 = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó == ['GUADALUPE JUAREZ'] and Class_Sucursal == 'OTROS' and FormaPagoDelPago != ['CHEQUE', 'DEPÓSITO', 'EFECTIVO', 'TARJETA']")
        df_PIEDRAS_NEGRAS = pd.concat([df_PN1, df_PN2, df_PN3], join="inner")

        # ahora tenemos que obtener todo lo que sea credito pero sin los vendedores (lesly, vivian, aleyda y guadalupe)...
        # esto se realiza con el siguiente codigo...
        df_Sin_Vendedores_Credito = df_clientes_especiales_FILTRADOS.query("Usuario_Aplicó != ['VIVIAN IVETTE ROJO GARCIA', 'LESLY MARTINEZ MARTINEZ PARTIDA', 'ALEYDA DE LA CRUZ MENDOZA', 'GUADALUPE JUAREZ']")
        # posteriormente, tenemos que volver a recrear el dataframe de credito, pero ahora con todas las clasificaciones.
        #haciendolo de la siguiente manera...
        df_Con_Vendedores_Credito = pd.concat([df_NUEVO_LAREDO, df_REYNOSA, df_PIEDRAS_NEGRAS,df_Sin_Vendedores_Credito], join="inner")

        # clasificamos los "ids clientes 892 y 58"
        df_892 = df_Con_Vendedores_Credito.query("Id_Cliente_Pago == [892] and FormaPagoDelPago == ['DEPÓSITO', 'CHEQUE', 'EFECTIVO', 'TARJETA', 'CLIENTES', 'CLIENTES-PROV DLLS']")
        df_892.Class_Sucursal = df_892.Class_Sucursal.map({"OTROS":"07 GARANTIAS KENMEX", 
                                                            "04 PIEDRAS NEGRAS":"07 GARANTIAS KENMEX",
                                                            "02 REYNOSA":"07 GARANTIAS KENMEX",
                                                            "01 NUEVO LAREDO":"07 GARANTIAS KENMEX",
                                                            "05 CLIENTE ESPECIAL":"07 GARANTIAS KENMEX"})
        df_58 = df_Con_Vendedores_Credito.query("Id_Cliente_Pago == [58] and FormaPagoDelPago == ['DEPÓSITO', 'CHEQUE', 'EFECTIVO', 'TARJETA', 'CLIENTES', 'CLIENTES-PROV DLLS']")
        df_58.Class_Sucursal = df_58.Class_Sucursal.map({"OTROS":"08 ALESSO", 
                                                            "04 PIEDRAS NEGRAS":"08 ALESSO",
                                                            "02 REYNOSA":"08 ALESSO",
                                                            "01 NUEVO LAREDO":"08 ALESSO",
                                                            "05 CLIENTE ESPECIAL":"08 ALESSO"})
        df_Sin_892_58 = df_Con_Vendedores_Credito.query("Id_Cliente_Pago == [892, 58] and FormaPagoDelPago != ['DEPÓSITO', 'CHEQUE', 'EFECTIVO', 'TARJETA', 'CLIENTES', 'CLIENTES-PROV DLLS']")
        df_892_58_Clasificado = pd.concat([df_892, df_58, df_Sin_892_58], join="inner")

        # del dataframe "df_con_vendedores_credito" debo de quitar todo lo que es "892 y 58"

        # clasificamos el "id 1099"
        df_1099 = df_Con_Vendedores_Credito.query("Id_Cliente_Pago == [1099] and Tipo_Docto == ['Factura'] and FormaPagoDelPago == ['DEPÓSITO']")
        df_1099.Class_Sucursal = df_1099.Class_Sucursal.map({"OTROS":"09 GARANTIAS PACCAR PARTS",
                                                            "04 PIEDRAS NEGRAS":"09 GARANTIAS PACCAR PARTS",
                                                            "02 REYNOSA":"09 GARANTIAS PACCAR PARTS",
                                                            "01 NUEVO LAREDO":"09 GARANTIAS PACCAR PARTS",
                                                            "05 CLIENTE ESPECIAL":"09 GARANTIAS PACCAR PARTS",
                                                            "07 GARANTIAS KENMEX":"09 GARANTIAS PACCAR PARTS",
                                                            "08 ALESSO": "09 GARANTIAS PACCAR PARTS"})
        df_Sin_1099 = df_Con_Vendedores_Credito.query("Id_Cliente_Pago == [1099] and Tipo_Docto != ['Factura'] or Id_Cliente_Pago == [1099] and Tipo_Docto == ['Factura'] and FormaPagoDelPago != ['DEPÓSITO']")
        df_1099_Clasificado = pd.concat([df_1099,df_Sin_1099], join="inner")

        # clasificamos 1098 y 1100
        df_1098_1100 = df_Con_Vendedores_Credito.query("Id_Cliente_Pago == [1098, 1100] and Tipo_Docto == ['Factura'] and Departamento == ['REFACCIONES', 'TALLER DE SERVICIO']")
        df_1098_1100.Class_Sucursal = df_1098_1100.Class_Sucursal.map({"OTROS":"10 PACLEASE",
                                                                    "04 PIEDRAS NEGRAS":"10 PACLEASE",
                                                                    "02 REYNOSA":"10 PACLEASE",
                                                                    "01 NUEVO LAREDO":"10 PACLEASE",
                                                                    "05 CLIENTE ESPECIAL":"10 PACLEASE",
                                                                    "07 GARANTIAS KENMEX":"10 PACLEASE",
                                                                    "08 ALESSO": "10 PACLEASE",
                                                                    "09 GARANTIAS PACCAR PARTS":"10 PACLEASE"})
        df_Sin_1098_1100 = df_Con_Vendedores_Credito.query("Id_Cliente_Pago == [1098,1100] and Tipo_Docto != ['Factura'] or Id_Cliente_Pago == [1098,1100] and Tipo_Docto == ['Factura'] and Departamento != ['REFACCIONES', 'TALLER DE SERVICIO']")
        df_1098_1100_Clasificaco = pd.concat([df_1098_1100, df_Sin_1098_1100], join="inner")

        # Ya es momento de concatenar lo que es de credito.
        # para ello tenemos que eliminar de df_Con_Vendedores_Credito los filtros o data que ya filtramos.
        df_sin_clasificaciones_idCliente = df_Con_Vendedores_Credito.query("Id_Cliente_Pago != [892, 58, 1099, 1098, 1100]")
        # AHORA concatenamos todos los id_cliente para juntarlo con el data donde se eliminaron.
        df_con_idclientes_clasificados = pd.concat([df_892_58_Clasificado,df_1099_Clasificado,df_1098_1100_Clasificaco,df_sin_clasificaciones_idCliente ], join="inner")

        #---------------------------------------Terminamos con el apartado de CREDITO---------------------------------



        #---------------------------------------Comenzamos con "CONTADO"------------------------------

        df_06contado = df_contado.query("Tipo_Docto == ['Factura'] and Departamento == ['REFACCIONES','TALLER DE SERVICIO'] and FormaPagoDelPago == ['ANTICIPO', 'CHEQUE', 'DEPÓSITO', 'EFECTIVO', 'TARJETA']")
        df_06contado.Class_Sucursal = df_06contado.Class_Sucursal.map({"OTROS":"06 CONTADO",
                                                                    "04 PIEDRAS NEGRAS":"06 CONTADO",
                                                                    "02 REYNOSA":"06 CONTADO",
                                                                    "01 NUEVO LAREDO":"06 CONTADO",
                                                                    "05 CLIENTE ESPECIAL":"06 CONTADO",
                                                                    "07 GARANTIAS KENMEX":"06 CONTADO",
                                                                    "08 ALESSO": "06 CONTADO",
                                                                    "09 GARANTIAS PACCAR PARTS":"06 CONTADO",
                                                                    "10 PACLEASE":"06 CONTADO"})
        # obtenemos la inversa del filtro de "06 contado".
        df_sin_06contado = df_contado.query("Tipo_Docto == ['Factura'] and Departamento == ['REFACCIONES','TALLER DE SERVICIO'] and FormaPagoDelPago != ['ANTICIPO', 'CHEQUE', 'DEPÓSITO', 'EFECTIVO', 'TARJETA'] or Tipo_Docto != ['Factura'] or Tipo_Docto == ['Factura'] and Departamento != ['REFACCIONES','TALLER DE SERVICIO']")
        # concatenamos los dos filtros para armar la cantidad de data original pero ya filtrada.
        df_06contado_filtrado = pd.concat([df_06contado,df_sin_06contado], join="inner")

        #---------------------------Terminamos de filtrar contado-------------------------

        #---------------------------Concatenamos contado y credito------------------------b

        # concatenamos las dos clasificaciones "credito y contado"
        df_Credito_Contado = pd.concat([df_con_idclientes_clasificados, df_06contado_filtrado], join="inner")

        #-----------------------------------clasificamos "credito y contado" con "Nota de cargo"-------------------

        df_nota_cargo = df_Credito_Contado.query("Tipo_Docto == ['Nota de cargo'] and FormaPagoDelPago == ['DEPÓSITO']")
        df_nota_cargo.Class_Sucursal = df_nota_cargo.Class_Sucursal.map({"OTROS":"11 NOTA DE CARGO",
                                                                        "04 PIEDRAS NEGRAS":"11 NOTA DE CARGO",
                                                                        "02 REYNOSA":"11 NOTA DE CARGO",
                                                                        "01 NUEVO LAREDO":"11 NOTA DE CARGO",
                                                                        "05 CLIENTE ESPECIAL":"11 NOTA DE CARGO",
                                                                        "07 GARANTIAS KENMEX":"11 NOTA DE CARGO",
                                                                        "08 ALESSO": "11 NOTA DE CARGO",
                                                                        "09 GARANTIAS PACCAR PARTS":"11 NOTA DE CARGO",
                                                                        "10 PACLEASE":"11 NOTA DE CARGO",
                                                                        "06 CONTADO":"11 NOTA DE CARGO"})
        df_sin_nota_cargo = df_Credito_Contado.query("Tipo_Docto == ['Nota de cargo'] and FormaPagoDelPago != ['DEPÓSITO'] or Tipo_Docto != ['Nota de cargo']")

        # concatenamos los dos Dataframe de "Nota de cargo"

        df_notacargo_clasificado = pd.concat([df_nota_cargo,df_sin_nota_cargo], join="inner")

        for i in df_notacargo_clasificado.columns:
            nombre_columna = i
            if (df_notacargo_clasificado[nombre_columna].dtypes == "object") and (nombre_columna == "Usuario_Aplicó"):
                self.objetivos[nombre_columna] = ['DANIA VARGAS ROSAS']
            elif (df_notacargo_clasificado[nombre_columna].dtypes == "object") and (nombre_columna == "Class_Sucursal"):
                self.objetivos[nombre_columna] = ['Objetivo']
            elif (df_notacargo_clasificado[nombre_columna].dtypes == "object") and (nombre_columna == "Departamento"):
                self.objetivos[nombre_columna] = ['KWRB']
            elif (df_notacargo_clasificado[nombre_columna].dtypes == "int64"):
                self.objetivos[nombre_columna] = ['0']
            elif (df_notacargo_clasificado[nombre_columna].dtypes == "float64"):
                self.objetivos[nombre_columna] = ['0.0']
            elif (nombre_columna == "Fecha_Pago") or (nombre_columna == "Fecha_Movimiento"):
                self.objetivos[nombre_columna] = [fechainsertar]
            else:
                self.objetivos[nombre_columna] = ['']

        DataFrameConObjetivo = pd.concat([df_notacargo_clasificado, self.objetivos], join="inner")

        for fecha in DataFrameConObjetivo:
            if ("Fecha" in fecha):
                try:
                    DataFrameConObjetivo[fecha] = pd.to_datetime(DataFrameConObjetivo[fecha] , errors = 'coerce')
                    DataFrameConObjetivo[fecha] = (DataFrameConObjetivo[fecha].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass

        
        
        columnas_bol=DataFrameConObjetivo.select_dtypes(include=bool).columns.tolist()
        DataFrameConObjetivo[columnas_bol] = DataFrameConObjetivo[columnas_bol].astype(str)

        if os.path.exists(self.ruta):
            try:
                df_json = pd.read_json(self.ruta)
                for indice, fila in df_json.iterrows():
                    sucursal_json = fila["Sucursal"]
                    objetivo_json = fila["Objetivo"]

                    # Verificar si la sucursal del JSON coincide con la sucursal en df

                    if sucursal_json in DataFrameConObjetivo["Class_Sucursal"].values.tolist():
                        # Actualizar el valor de "Objetivos" en DataFrameConObjetivo
                        DataFrameConObjetivo.loc[DataFrameConObjetivo["Class_Sucursal"] == sucursal_json, "Objetivo"] = objetivo_json
                    
                    else:
                        pass
            except:
                pass
        
        # damos formato a todas las cabeceras de las columnas.
        # recordar volver a la normalidad.
        DataFrameConObjetivo.columns = DataFrameConObjetivo.columns.str.replace('_', ' ')
        

        DataFrameConObjetivo.to_excel(os.path.join(Variables().ruta_procesados,f'PAGOS_KWRB_SRD_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)