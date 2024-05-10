#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import*
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class Refacciones(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()
        self.nombre_doc = 'RS.xlsx'

        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)

        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        df.drop(['% Margen', 'Meta Ventas Por Vendedor', 'Meta Margen Por Vendedor', 'Meta Cantidad Por Vendedor', 'Meta Ventas Por Sucursal', 'Meta Margen Por Sucursal', 'Meta Cantidad Por Sucursal', '% Comisión Por Margen', '% Comisión Por Ventas', 'Comisión Por Margen', 'Comisión Por Ventas', 'EsBonificacion', 'IdUsuario', 'IdPaquete', 'Paquete', 'Descripción Paquete', 'Cantidad Paquete', 'Subtotal Paquete', 'Potencial Total', 'Tipo de Cambio del día', 'OCCliente', '% Margen Sin Descuento'], axis=1, inplace=True)
        df= df[df.columns[0:93]].copy()

        df["Departamento Venta"] = ""
        df["Depa"] = ""

        #COMMENT: clasificacion de los vendedores
        #COMMENT: sucursal cananea - mostrador
        df.loc[(df["Vendedor"] == "BELTRAN ALVIDREZ LOURDES LIZETH") & (df["Sucursal"] == "Cananea"),"Departamento Venta"] = "Mostrador Cananea"
        df.loc[(df["Vendedor"] == "OMAR DELGADO ZARCO") & (df["Sucursal"] == "Cananea"),"Departamento Venta"] = "Mostrador Cananea"
        df.loc[(df["Vendedor"] == "LOPEZ HERNANDEZ OSCAR") & (df["Sucursal"] == "Cananea"),"Departamento Venta"] = "Mostrador Cananea"
        df.loc[(df["Vendedor"] == "TALLER HERMOSILLO") & (df["Sucursal"] == "Cananea"),"Departamento Venta"] = "Mostrador Cananea"

        df.loc[(df["Vendedor"] == "BELTRAN ALVIDREZ LOURDES LIZETH") & (df["Sucursal"] == "Cananea"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "OMAR DELGADO ZARCO") & (df["Sucursal"] == "Cananea"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "LOPEZ HERNANDEZ OSCAR") & (df["Sucursal"] == "Cananea"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "TALLER HERMOSILLO") & (df["Sucursal"] == "Cananea"),"Depa"] = "Mostrador"
        
        #COMMENT: sucursal hermosillo - mostrador
        df.loc[(df["Vendedor"] == "BALDENEGRO ARVAYO MIGUEL BAUDELIO") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Mostrador Hermosillo"
        df.loc[(df["Vendedor"] == "GOMEZ CHINCHILLAS ANGEL ALFONSO") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Mostrador Hermosillo"
        df.loc[(df["Vendedor"] == "BELEM CECILIA MARCIAL LARES") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Mostrador Hermosillo"
        df.loc[(df["Vendedor"] == "LOPEZ HERNANDEZ OSCAR") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Mostrador Hermosillo"
        df.loc[(df["Vendedor"] == "HECTOR DUARTE RENDÓN") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Mostrador Hermosillo"
        df.loc[(df["Vendedor"] == "LOPEZ SANCHEZ JORGE RENNE") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Mostrador Hermosillo"
        df.loc[(df["Vendedor"] == "SERGIO MEDINA GOMEZ") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Mostrador Hermosillo"

        df.loc[(df["Vendedor"] == "BALDENEGRO ARVAYO MIGUEL BAUDELIO") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "GOMEZ CHINCHILLAS ANGEL ALFONSO") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "BELEM CECILIA MARCIAL LARES") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "LOPEZ HERNANDEZ OSCAR") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "HECTOR DUARTE RENDÓN") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "LOPEZ SANCHEZ JORGE RENNE") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "SERGIO MEDINA GOMEZ") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Mostrador"

        #COMMENT: sucursal navojoa - mostrador
        df.loc[(df["Vendedor"] == "JOSE LUIS RUELAS CHAVEZ") & (df["Sucursal"] == "Navojoa"),"Departamento Venta"] = "Mostrador Navojoa"
        df.loc[(df["Vendedor"] == "URIEL PORTILLO ESQUER") & (df["Sucursal"] == "Navojoa"),"Departamento Venta"] = "Mostrador Navojoa"
        df.loc[(df["Vendedor"] == "JORGE EDUARDO MONTOYA CAMPILLO") & (df["Sucursal"] == "Navojoa"),"Departamento Venta"] = "Mostrador Navojoa"
        df.loc[(df["Vendedor"] == "JOEL GUTIERREZ BAJECA") & (df["Sucursal"] == "Navojoa"),"Departamento Venta"] = "Mostrador Navojoa"

        df.loc[(df["Vendedor"] == "JOSE LUIS RUELAS CHAVEZ") & (df["Sucursal"] == "Navojoa"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "URIEL PORTILLO ESQUER") & (df["Sucursal"] == "Navojoa"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "JORGE EDUARDO MONTOYA CAMPILLO") & (df["Sucursal"] == "Navojoa"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "JOEL GUTIERREZ BAJECA") & (df["Sucursal"] == "Navojoa"),"Depa"] = "Mostrador"

        #COMMENT: sucursal Nogales - mostrador
        df.loc[(df["Vendedor"] == "RENE ALEJANDRO ACOSTA VALENZUELA") & (df["Sucursal"] == "Nogales"),"Departamento Venta"] = "Mostrador Nogales"
        df.loc[(df["Vendedor"] == "JUAB CARLOS JARAMILLO ARMENTA") & (df["Sucursal"] == "Nogales"),"Departamento Venta"] = "Mostrador Nogales"
        df.loc[(df["Vendedor"] == "EDGAR GERALDO GUTIERREZ BACASEGUA") & (df["Sucursal"] == "Nogales"),"Departamento Venta"] = "Mostrador Nogales"
        df.loc[(df["Vendedor"] == "TALLER HERMOSILLO") & (df["Sucursal"] == "Nogales"),"Departamento Venta"] = "Mostrador Nogales"

        df.loc[(df["Vendedor"] == "RENE ALEJANDRO ACOSTA VALENZUELA") & (df["Sucursal"] == "Nogales"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "JUAB CARLOS JARAMILLO ARMENTA") & (df["Sucursal"] == "Nogales"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "EDGAR GERALDO GUTIERREZ BACASEGUA") & (df["Sucursal"] == "Nogales"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "TALLER HERMOSILLO") & (df["Sucursal"] == "Nogales"),"Depa"] = "Mostrador"

        #COMMENT: sucursal Nogales Centro - mostrador
        df.loc[(df["Vendedor"] == "RODRIGO ANTONIO QUIÑONES NUÑEZ") & (df["Sucursal"] == "Nogales Centro"),"Departamento Venta"] = "Mostrador Nogales Centro"
        df.loc[(df["Vendedor"] == "LILIANA HAYDEE FONTES BARRON") & (df["Sucursal"] == "Nogales Centro"),"Departamento Venta"] = "Mostrador Nogales Centro"
        df.loc[(df["Vendedor"] == "IVAN IBARRA NAVARRO") & (df["Sucursal"] == "Nogales Centro"),"Departamento Venta"] = "Mostrador Nogales Centro"

        df.loc[(df["Vendedor"] == "RODRIGO ANTONIO QUIÑONES NUÑEZ") & (df["Sucursal"] == "Nogales Centro"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "LILIANA HAYDEE FONTES BARRON") & (df["Sucursal"] == "Nogales Centro"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "IVAN IBARRA NAVARRO") & (df["Sucursal"] == "Nogales Centro"),"Depa"] = "Mostrador"

        #COMMENT: sucursal Obregon - mostrador
        df.loc[(df["Vendedor"] == "MANUEL BELTRAN") & (df["Sucursal"] == "Obregon"),"Departamento Venta"] = "Mostrador Obregon"
        df.loc[(df["Vendedor"] == "VICENTE TREJO ORDORICA") & (df["Sucursal"] == "Obregon"),"Departamento Venta"] = "Mostrador Obregon"
        df.loc[(df["Vendedor"] == "MEDINA OCHOA FRANCISCO JAVIER") & (df["Sucursal"] == "Obregon"),"Departamento Venta"] = "Mostrador Obregon"
        df.loc[(df["Vendedor"] == "ELISEO MAZO JAQUES") & (df["Sucursal"] == "Obregon"),"Departamento Venta"] = "Mostrador Obregon"
        df.loc[(df["Vendedor"] == "ACOSTA AVILA JORGE ANTONIO") & (df["Sucursal"] == "Obregon"),"Departamento Venta"] = "Mostrador Obregon"
        df.loc[(df["Vendedor"] == "JORGE EDUARDO MONTOYA CAMPILLO") & (df["Sucursal"] == "Obregon"),"Departamento Venta"] = "Mostrador Obregon"

        df.loc[(df["Vendedor"] == "MANUEL BELTRAN") & (df["Sucursal"] == "Obregon"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "VICENTE TREJO ORDORICA") & (df["Sucursal"] == "Obregon"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "MEDINA OCHOA FRANCISCO JAVIER") & (df["Sucursal"] == "Obregon"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "ELISEO MAZO JAQUES") & (df["Sucursal"] == "Obregon"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "ACOSTA AVILA JORGE ANTONIO") & (df["Sucursal"] == "Obregon"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "JORGE EDUARDO MONTOYA CAMPILLO") & (df["Sucursal"] == "Obregon"),"Depa"] = "Mostrador"
        
        #COMMENT: sucursal Perisur - mostrador
        df.loc[(df["Vendedor"] == "LOPEZ SANCHEZ JORGE RENNE") & (df["Sucursal"] == "Perisur"),"Departamento Venta"] = "Mostrador Perisur"
        df.loc[(df["Vendedor"] == "HECTOR DUARTE RENDÓN") & (df["Sucursal"] == "Perisur"),"Departamento Venta"] = "Mostrador Perisur"
        df.loc[(df["Vendedor"] == "JORGE VALENCIA [PERISUR]]") & (df["Sucursal"] == "Perisur"),"Departamento Venta"] = "Mostrador Perisur"
        df.loc[(df["Vendedor"] == "PIRI OQUITA RAMON") & (df["Sucursal"] == "Perisur"),"Departamento Venta"] = "Mostrador Perisur"
        df.loc[(df["Vendedor"] == "TALLER HERMOSILLO") & (df["Sucursal"] == "Perisur"),"Departamento Venta"] = "Mostrador Perisur"
        df.loc[(df["Vendedor"] == "TOMAS CORONADO") & (df["Sucursal"] == "Perisur"),"Departamento Venta"] = "Mostrador Perisur"

        df.loc[(df["Vendedor"] == "LOPEZ SANCHEZ JORGE RENNE") & (df["Sucursal"] == "Perisur"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "HECTOR DUARTE RENDÓN") & (df["Sucursal"] == "Perisur"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "JORGE VALENCIA [PERISUR]]") & (df["Sucursal"] == "Perisur"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "PIRI OQUITA RAMON") & (df["Sucursal"] == "Perisur"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "TALLER HERMOSILLO") & (df["Sucursal"] == "Perisur"),"Depa"] = "Mostrador"
        df.loc[(df["Vendedor"] == "TOMAS CORONADO") & (df["Sucursal"] == "Perisur"),"Depa"] = "Mostrador"
        
        #COMMENT: sucursal Obregon - taller
        df.loc[(df["Vendedor"] == "TALLER OBREGON") & (df["Sucursal"] == "Obregon"),"Departamento Venta"] = "Taller Obregon"
        df.loc[(df["Vendedor"] == "TALLER OBREGON") & (df["Sucursal"] == "Obregon"),"Depa"] = "Taller"
        
        #COMMENT: sucursal Nogales - Taller
        df.loc[(df["Vendedor"] == "TALLER NOGALES") & (df["Sucursal"] == "Nogales"),"Departamento Venta"] = "Taller Nogales"
        df.loc[(df["Vendedor"] == "TALLER NOGALES") & (df["Sucursal"] == "Nogales"),"Depa"] = "Taller"
        
        #COMMENT: sucaursa Hermosillo - Taller
        df.loc[(df["Vendedor"] == "TALLER HERMOSILLO") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Taller Hermosillo"
        df.loc[(df["Vendedor"] == "TALLER HERMOSILLO") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Taller"
        
        #COMMENT: sucursal Hermosillo - Carroceria
        df.loc[(df["Vendedor"] == "CARROCERIA HERMOSILLO") & (df["Sucursal"] == "Hermosillo"),"Departamento Venta"] = "Carroceria Hermosillo"
        df.loc[(df["Vendedor"] == "CARROCERIA HERMOSILLO") & (df["Sucursal"] == "Hermosillo"),"Depa"] = "Carroceria"

        for i in df:
            if ("fecha" in i.lower()):
                try:
                    df[i] = df[i].dt.strftime("%d/%m/%Y")
                except:
                    pass
        
        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)
