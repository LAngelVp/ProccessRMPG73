#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class OrdenesDeServicio(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.nombre_doc = 'OSE.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        
        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(' ', '_')
        df2 = df.copy()

        # ESTOS ARRAYS SON DE APOYO PARA LA CLASIFICACION DE LOS CLIENTES
        array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"] 

        # CREAMOS LA COLUMNA DE CLASIFICACION CLIENTE
        df2.insert(loc=5,column="Clasificacion_Cliente",value="CLIENTES GENERALES", allow_duplicates = False)

        #CLASIFICACION DEL CLIENTE (NORMAL)
        df2.loc[df2["Cliente"].str.contains("KENWORTH") & ~df2["Cliente"].str.contains("KENWORTH MEXICANA","KENWORTH DEL ESTE") & ~df2["Cliente"].str.contains("KENWORTH DEL ESTE"), "Clasificacion_Cliente"] = "CONCESIONARIOS"
        df2.loc[df2["Cliente"].str.contains("|".join(array_Garantia)),"Clasificacion_Cliente"] = "GARANTIA"
        df2.loc[df2["Cliente"].str.contains("|".join(array_PLM)),"Clasificacion_Cliente"] = "PLM"
        df2.loc[df2["Cliente"] == "KENWORTH DEL ESTE", "Clasificacion_Cliente"] = "CI"
        df2.loc[(df2["Cliente"].str.contains("SEGUROS")) | (df2["Cliente"].str.contains("SEGURO")) | (df2["Cliente"] == "GRUPO NACIONAL PROVINCIAL"), "Clasificacion_Cliente"] = "SEGUROS"

        # debemos de quitar garantia para hacer la clasificacion por tipo servicio
        QuitamosGarantia = df2.query("~(Clasificacion_Cliente == ['GARANTIA'])").copy()
        TomamosGarantia = df2.query("Clasificacion_Cliente == ['GARANTIA']").copy()

        #CLASIFICACION DEL CLIENTE POR "TIPO SERVICIO"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Externo"),"Clasificacion_Cliente"] = "RESCATES EXTERNOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Avalado"), "Clasificacion_Cliente"] = "RESCATES AVALADOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Servicio a Domicilio"), "Clasificacion_Cliente"] = "SERVICIO A DOMICILIO"

        # concatenamos el dataframe que no tiene garantia y ya esta clasificado por tipo servicio con el dataframe que si tiene lo de garantia
        claficicacion_tipo_servicio = pd.concat([QuitamosGarantia, TomamosGarantia], join="inner")

        # CONCATENAMOS LA COLUMNA DE NUMERO DE ORDEN y UNIDAD
        NumOrden = "OS" + claficicacion_tipo_servicio["Número_Orden"].map(str)
        Unidad = "UN-" + claficicacion_tipo_servicio["Unidad"].map(str)
        
        # INSERTAMOS LAS COLUMNAS EN SUS RESPECTIVOS LUGARES
        claficicacion_tipo_servicio.insert(0,"Num_Orden",NumOrden,allow_duplicates=True)
        claficicacion_tipo_servicio["Unidad"] = Unidad

        #MANDAMOS A LLAMAR A LA FUNCION
        claficicacion_tipo_servicio["Clasificacion_Cliente"] = claficicacion_tipo_servicio.apply(self.FiltroPorNumeroOrden, axis = 1)
        
        
        claficicacion_tipo_servicio.drop(["Número_Orden","Folio_Cotizaciones"], axis = 1, inplace=True)
        
        ultima_columna = claficicacion_tipo_servicio.columns.get_loc("Estado_Orden_Global")
        
        claficicacion_tipo_servicio = claficicacion_tipo_servicio.iloc[:,:ultima_columna + 1]
        
        Clasificacion_Venta = claficicacion_tipo_servicio["Clasificacion_Cliente"]

        claficicacion_tipo_servicio.insert(6,"Clasificacion_Venta",Clasificacion_Venta,allow_duplicates=False)
        

        for column_name in claficicacion_tipo_servicio.columns:
                if "fecha" in column_name.lower():
                    claficicacion_tipo_servicio = self.variables.global_date_format_america(claficicacion_tipo_servicio, column_name)
                else:
                    pass
        print(1)
        # TOMAMOS LA DATA QUE VAMOS A TRABAJAR CON LA FECHA A PARTIR DEL 2020
        df_FechaOrden = claficicacion_tipo_servicio[claficicacion_tipo_servicio['Fecha_Orden'] >= '2020-06-01']

        #SEPARAMOS LA DATA QUE NO TRABAJAREMOS PERO LA CONCATENAREMOS PARA HACER UN COMPLEMENTO DESPUES.
        df_SinFechaOrden = claficicacion_tipo_servicio[claficicacion_tipo_servicio["Fecha_Orden"] < '2020-06-01']

        # PRIMER FILTRO DESPUES DE LA FECHA ORDEN
        clasif_OlmecaMaya = df_FechaOrden.query("Cliente == ['PACCAR FINANCIAL MEXICO', 'PACLEASE MEXICANA'] and Tipo_Servicio == ['Servicio Preventivo', 'Servicio Correctivo'] and Sucursal == ['Veracruz', 'Villahermosa'] and MO >= 0 and MO <= 0.99 and Ref == 0 and Estado_Trabajo != ['Cancelado', 'Facturado']").copy()
        clasif_OlmecaMaya["Clasificacion_Cliente"] = "OLMECA MAYA"
        clasif_OlmecaMaya["Clasificacion_Venta"] = "OLMECA MAYA"

        clasif_OlmecaMaya_Negado = df_FechaOrden.query("~(Cliente == ['PACCAR FINANCIAL MEXICO', 'PACLEASE MEXICANA'] and Tipo_Servicio == ['Servicio Preventivo', 'Servicio Correctivo'] and Sucursal == ['Veracruz', 'Villahermosa'] and MO >= 0 and MO <= 0.99 and Ref == 0 and Estado_Trabajo != ['Cancelado', 'Facturado'])").copy()

        OlmecaMaya = pd.concat([clasif_OlmecaMaya, clasif_OlmecaMaya_Negado, df_SinFechaOrden], join="inner")

        # CLASIFICAMOS A VILLAHERMOSA
        # OCUPAMOS EL DATAFRAME DE OLMEA MAYA, VAMOS A IR DE MANERA DE CASCADA
        villahermosa = OlmecaMaya.query("Cliente == ['PACCAR FINANCIAL MEXICO', 'PACLEASE MEXICANA'] and Sucursal == ['Villahermosa'] and IPK == ['No']").copy()
        villahermosa["IPK"] = 'Sí'
        villahermosa_Negada = OlmecaMaya.query("~(Cliente == ['PACCAR FINANCIAL MEXICO', 'PACLEASE MEXICANA'] and Sucursal == ['Villahermosa'] and IPK == ['No'])")

        VillaHermosa = pd.concat([villahermosa, villahermosa_Negada], join="inner")

        # CLASIFICAR  A PLM EN CLASIFICACION VENTA
        clasificacion_venta_PLM = VillaHermosa.query("Cliente == ['PACCAR FINANCIAL MEXICO', 'PACLEASE MEXICANA'] and Clasificacion_Venta != ['OLMECA MAYA']").copy()
        clasificacion_venta_PLM["Clasificacion_Venta"] = "PLM"

        clasificacion_venta_PLM_Negada = VillaHermosa.query("~(Cliente == ['PACCAR FINANCIAL MEXICO', 'PACLEASE MEXICANA'] and Clasificacion_Venta != ['OLMECA MAYA'])").copy()

        ClasificacionVentaPLM = pd.concat([clasificacion_venta_PLM, clasificacion_venta_PLM_Negada], join="inner")
        
        # CLASIFICACION POR VERACRUZ
        veracruz = ClasificacionVentaPLM.query("Sucursal == ['Veracruz'] and Estado_Orden != ['Cancelada', 'Facturada'] and Orden_Reparación.str.contains('OLMECA MAYA')").copy()
        veracruz["Clasificacion_Cliente"] = "OLMECA MAYA"
        veracruz["Clasificacion_Venta"] = "OLMECA MAYA"

        veracruz_Negada = ClasificacionVentaPLM.query("~(Sucursal == ['Veracruz'] and Estado_Orden != ['Cancelada', 'Facturada'] and Orden_Reparación.str.contains('OLMECA MAYA'))").copy()


        Completo = pd.concat([veracruz, veracruz_Negada], join="inner")

        columna = Completo.pop("Subtotal_Ref_Sin_Facturar")
        Completo.insert(21, "Subtotal_Ref_Sin_Facturar", columna)

        Completo.insert(loc=25, column = 'Total OS Pde Fact', value = Completo[['MO', 'CM', 'TOT', 'Subtotal_Ref_Sin_Facturar']].fillna(0).sum(axis=1), allow_duplicates = False)

        Completo['Total OS Pde Fact'] = Completo['Total OS Pde Fact'].apply(lambda x: '{:.2f}'.format(x))
        Completo['Total OS Pde Fact'] = Completo['Total OS Pde Fact'].astype(float).fillna(0)

        Completo.columns = Completo.columns.str.replace('_', ' ')
        print(2)

        for column_name in Completo.columns:
            if "fecha" in column_name.lower():
                Completo = self.variables.global_date_format_dmy_mexican(Completo, column_name)
                print(Completo[column_name].dtype)
            else:
                pass
        print(3)
        columnas_bol=Completo.select_dtypes(include=bool).columns.tolist()
        Completo[columnas_bol] = Completo[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, Completo, self.concesionario)

    # CREAMOS LA FUNCION PARA LAS CLASIFICACIONES POR NUMERO DE ORDEN
    def FiltroPorNumeroOrden(self, row):
        try:
            if row["Número_Orden"] in [45827, 46745, 46957, 48745] and row["Sucursal"] == "Matriz Cordoba":
                return "GARANTIA"
            elif row["Número_Orden"] in [44034, 44330, 44662, 45250, 44895, 45286, 45295, 45622, 45627, 45707, 46246, 46316] and row["Sucursal"] != "Matriz Cordoba":
                return "GARANTIA"
            elif row["Número_Orden"] in [51, 61, 151, 159, 177, 200, 234, 376, 397, 450, 480, 496, 600, 641, 685] and row["Sucursal"] == "Villahermosa":
                return "GARANTIA"
            elif row["Número_Orden"] in [44757, 46087, 46098, 46273, 46321, 46339, 46395] and row["Sucursal"] == "Matriz Cordoba":
                return "SEGUROS"
            else:
                return row["Clasificacion_Cliente"]
        except:
            pass