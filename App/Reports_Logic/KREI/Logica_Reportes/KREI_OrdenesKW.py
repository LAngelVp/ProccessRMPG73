#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class  OrdenesServicioKWESTEKREI(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()
        self.array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        self.array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]
        self.array_excepto_clientes = ["KENWORTH","PACCAR PARTS MEXICO", "PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA", "DISTRIBUIDORA MEGAMAK", "SEGUROS", "SEGURO", "GRUPO NACIONAL PROVINCIAL"]
    def OrdenesKWESTE_KREI(self):
        self.nombre_doc = 'OSEKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        dfKWESTE = pd.read_excel(path, sheet_name="Hoja2")
        dfKWESTE = dfKWESTE.replace(to_replace = ";", value = "_", regex = True)
        # remplazamos los espacios en los titulos por cuestiones de normatividad
        dfKWESTE.columns = dfKWESTE.columns.str.replace(" ", "_")
        # creacion de la columna de clasificacion
        dfKWESTE.insert(loc=5,column="Clasificacion_Cliente",value="CLIENTES GENERALES", allow_duplicates = False)
        # Clasificacion kweste
        dfKWESTE.loc[dfKWESTE["Cliente"].str.contains("KENWORTH") & ~dfKWESTE["Cliente"].str.contains("KENWORTH MEXICANA"), "Clasificacion_Cliente"] = "CONCESIONARIOS"
        dfKWESTE.loc[dfKWESTE["Cliente"].str.contains("|".join(self.array_Garantia)), "Clasificacion_Cliente"] = "GARANTIA"
        dfKWESTE.loc[dfKWESTE["Cliente"].str.contains("|".join(self.array_PLM)), "Clasificacion_Cliente"] = "PLM"
        dfKWESTE.loc[dfKWESTE["Cliente"] == "KENWORTH DEL ESTE", "Clasificacion_Cliente"] = "CI"
        dfKWESTE.loc[(dfKWESTE["Cliente"] == "PACCAR FINANCIAL MEXICO") | (dfKWESTE["Cliente"] == "PACLEASE MEXICANA"), "Clasificacion_Cliente"] = "PLM"
        dfKWESTE.loc[(dfKWESTE["Cliente"].str.contains('SEGUROS')) | (dfKWESTE["Cliente"].str.contains('SEGURO')) | (dfKWESTE["Cliente"] == 'GRUPO NACIONAL PROVINCIAL'), "Clasificacion_Cliente" ]= "SEGUROS"
        #dfKWESTE.loc[~dfKWESTE["Cliente"].str.contains("|".join(array_excepto_clientes)), "Clasificacion_Cliente"] = "CLIENTES GENERALES"

        # ponemos todas las columnas de fecha en formato fecha
        for column_name in dfKWESTE.columns:
                if "fecha" in column_name.lower():
                    dfKWESTE = self.variables.global_date_format_america(dfKWESTE, column_name)
                    dfKWESTE = self.variables.global_date_format_dmy_mexican(dfKWESTE, column_name)
                else:
                    pass

        dfKWESTE = dfKWESTE.rename(columns={ 'Número_Orden': 'num', 'Unidad':'UNI', 'Subtotal_Ref_Sin_Facturar':'sub' })
        dfKWESTE.insert(loc = 0,column = 'OS',value = 'OS',allow_duplicates = False)
        dfKWESTE.insert(loc = 2, column = 'Num Orden', value = dfKWESTE["OS"].map(str) + "" + dfKWESTE["num"].map(str), allow_duplicates = False)
        dfKWESTE.insert(loc = 3,column = 'UN',value = 'UN-',allow_duplicates = False)
        dfKWESTE.insert(loc = 5, column = 'Unidad', value = dfKWESTE["UN"].map(str) + "" + dfKWESTE["UNI"].map(str), allow_duplicates = True)
        dfKWESTE.drop(['OS', 'num', 'UN', 'UNI'], axis = 1, inplace=True)
        columna = dfKWESTE.pop("sub")
        dfKWESTE.insert(20, "sub", columna)
        dfKWESTE.insert(loc=24, column = 'Total OS Pde Fact', value = dfKWESTE[['MO', 'CM', 'TOT', 'sub']].fillna(0).sum(axis=1), allow_duplicates = False)

        dfKWESTE['Total OS Pde Fact'] = dfKWESTE['Total OS Pde Fact'].apply(lambda x: '{:.2f}'.format(x))
        dfKWESTE['Total OS Pde Fact'] = dfKWESTE['Total OS Pde Fact'].astype(float).fillna(0)

        dfKWESTE['Total OS Pde Fact'] = pd.to_numeric(dfKWESTE['Total OS Pde Fact'], errors='coerce').fillna(0)
        dfKWESTE = dfKWESTE.rename(columns={'sub' : 'Subtotal_Ref_Sin_Facturar'})

        ultima_columna = dfKWESTE.columns.get_loc("TipoUnidad")
        
        dfKWESTE = dfKWESTE.iloc[:,:ultima_columna + 1]

        # egresamos el titulo de las columnas a su formato original
        dfKWESTE.columns = dfKWESTE.columns.str.replace("_", " ")
        
        dfKWESTE.insert(0,"Concesionario","KW ESTE", allow_duplicates=False)
        dfKWESTE['Cantidad Trabajos'] = 1

        columnas_bol=dfKWESTE.select_dtypes(include=bool).columns.tolist()
        dfKWESTE[columnas_bol] = dfKWESTE[columnas_bol].astype(str)


        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, dfKWESTE, self.concesionario)
    
    def OrdenesKWSUR_KREI(self):
        self.nombre_doc = 'OSSKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        dfKWS = pd.read_excel(path, sheet_name="Hoja2")
        dfKWSUR = dfKWS.replace(to_replace = ";", value = "_", regex = True)
        # remplazamos los espacios en los titulos por cuestiones de normatividad
        dfKWSUR.columns = dfKWSUR.columns.str.replace(" ", "_")
        # creacion de la columna de clasificacion
        dfKWSUR.insert(loc=5,column="Clasificacion_Cliente",value="CLIENTES GENERALES", allow_duplicates = False)

        # Clasificacion kwsur
        dfKWSUR.loc[dfKWSUR["Cliente"].str.contains("KENWORTH") & ~dfKWSUR["Cliente"].str.contains("KENWORTH MEXICANA"), "Clasificacion_Cliente"] = "CONCESIONARIOS"
        dfKWSUR.loc[dfKWSUR["Cliente"].str.contains("|".join(self.array_Garantia)), "Clasificacion_Cliente"] = "GARANTIA"
        dfKWSUR.loc[dfKWSUR["Cliente"].str.contains("|".join(self.array_PLM)), "Clasificacion_Cliente"] = "PLM"
        dfKWSUR.loc[dfKWSUR["Cliente"] == "KENWORTH DEL SUR", "Clasificacion_Cliente"] = "CI"
        dfKWSUR.loc[(dfKWSUR["Cliente"] == "PACCAR FINANCIAL MEXICO") | (dfKWSUR["Cliente"] == "PACLEASE MEXICANA"), "Clasificacion_Cliente"] = "PLM"
        dfKWSUR.loc[(dfKWSUR["Cliente"].str.contains('SEGUROS')) | (dfKWSUR["Cliente"].str.contains('SEGURO')) | (dfKWSUR["Cliente"] == 'GRUPO NACIONAL PROVINCIAL'), "Clasificacion_Cliente" ]= "SEGUROS"
        #dfKWSUR.loc[dfKWSUR["Cliente"].str.contains("|".join(array_excepto_clientes)), "Clasificacion_Cliente"] = "CLIENTES GENERALES"

        # ponemos todas las columnas de fecha en formato fecha
        for column_name in dfKWSUR.columns:
                if "fecha" in column_name.lower():
                    dfKWSUR = self.variables.global_date_format_america(dfKWSUR, column_name)
                    dfKWSUR = self.variables.global_date_format_dmy_mexican(dfKWSUR, column_name)
                else:
                    pass


        dfKWSUR = dfKWSUR.rename(columns={ 'Número_Orden': 'num', 'Unidad':'UNI', 'Subtotal_Ref_Sin_Facturar':'sub' })
        dfKWSUR.insert(loc = 0,column = 'OS',value = 'OS',allow_duplicates = False)
        dfKWSUR.insert(loc = 2, column = 'Num Orden', value = dfKWSUR["OS"].map(str) + "" + dfKWSUR["num"].map(str), allow_duplicates = False)
        dfKWSUR.insert(loc = 3,column = 'UN',value = 'UN-',allow_duplicates = False)
        dfKWSUR.insert(loc = 5, column = 'Unidad', value = dfKWSUR["UN"].map(str) + "" + dfKWSUR["UNI"].map(str), allow_duplicates = True)
        dfKWSUR.drop(['OS', 'num', 'UN', 'UNI'], axis = 1, inplace=True)
        columna = dfKWSUR.pop("sub")
        dfKWSUR.insert(20, "sub", columna)
        dfKWSUR.insert(loc=24, column = 'Total OS Pde Fact', value = dfKWSUR[['MO', 'CM', 'TOT', 'sub']].fillna(0).sum(axis=1), allow_duplicates = False)

        dfKWSUR['Total OS Pde Fact'] = dfKWSUR['Total OS Pde Fact'].apply(lambda x: '{:.2f}'.format(x))
        dfKWSUR['Total OS Pde Fact'] = dfKWSUR['Total OS Pde Fact'].astype(float).fillna(0)

        dfKWSUR['Total OS Pde Fact'] = pd.to_numeric(dfKWSUR['Total OS Pde Fact'], errors='coerce').fillna(0)
        dfKWSUR = dfKWSUR.rename(columns={'sub' : 'Subtotal_Ref_Sin_Facturar'})

        ultima_columna = dfKWSUR.columns.get_loc("TipoUnidad")
        
        dfKWSUR = dfKWSUR.iloc[:,:ultima_columna + 1]

        # egresamos el titulo de las columnas a su formato original
        dfKWSUR.columns = dfKWSUR.columns.str.replace("_", " ")

        dfKWSUR.insert(0,"Concesionario","KW SUR", allow_duplicates=False)
        dfKWSUR['Cantidad Trabajos'] = 1
        columnas_bol=dfKWSUR.select_dtypes(include=bool).columns.tolist()
        dfKWSUR[columnas_bol] = dfKWSUR[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, dfKWSUR, self.concesionario)