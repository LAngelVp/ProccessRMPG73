import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
import xlrd
import locale
from time import sleep

class VentasPerdidas(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()

        self.documentos_ventasperdidas_sucursal = [
            "VPMATRIZ.xls",
            "VPTREBOL.xls",
            "VPVERACRUZ.xls",
            "VPORIZABA.xls",
            "VPTEHUACAN.xls",
            "VPVILLAHERMOSA.xls",
            "VPCOATZACOALCOS.xls",
            "VPMERIDA.xls",
            "VPOAXACA.xls",
            "VPTUXTLA1.xls",
            "VPTUXTLA2.xls",
        ]
        
        # Asegúrate de que 'ruta_ventasperdidas' sea una propiedad de la clase
        self.ruta_ventasperdidas = None
        # Obtener la ruta base donde se almacenan los archivos
        self.ruta_base = self.variables.ruta_Trabajos_kwe
        
    def comprobar_existencia_ventasperdidas(self):
        # Buscar si ya existe un archivo con ventas perdidas
        for ventasperdidas in os.listdir(self.variables.ruta_exitosos_kwe):
            if "ventasperdidas" in ventasperdidas:
                self.ruta_ventasperdidas = os.path.join(self.variables.ruta_exitosos_kwe, ventasperdidas)

        # Comprobar si el archivo "ventasperdidas.xls" ya existe
        if self.ruta_ventasperdidas is not None:
            if os.path.exists(self.ruta_ventasperdidas):
                # Si el archivo existe, leer el archivo existente
                self.df_final = pd.read_excel(self.ruta_ventasperdidas)
                print(f"Archivo 'ventasperdidas.xls' encontrado y cargado.")
            else:
                print("El archivo 'ventasperdidas.xls' no existe en la ruta esperada.")
                self.df_final = self.crear_ventas_perdidas_iniciales()
        else:
            # Si no se ha encontrado el archivo en el directorio, crear uno nuevo
            print("No se encontró el archivo 'ventasperdidas.xls'. Creando archivo nuevo.")
            self.df_final = self.crear_ventas_perdidas_iniciales()
            
    def crear_ventas_perdidas_iniciales(self):
        # Método para crear el DataFrame con los datos iniciales si no existe el archivo
        sucursales = [
            "Coatzacoalcos", "Villahermosa", "Veracruz", "Oaxaca", "Tehuacan", "Merida", 
            "Trebol", "Matriz Cordoba", "Tuxtla1", "Orizaba", "Tuxtla2"
        ]
        dfs = []
        for sucursal in sucursales:
            data = {
                "VP": [0, 0],
                "Venta Perdida": ["-", "-"],
                "Id. Cliente": [0, 0],
                "Nombre Cliente": ["-", "-"],
                "Núm. Artículo": ["-", "-"],
                "Artículo": ["-", "-"],
                "Motivo": ["NO EXIST EN SUCURSAL (MOVTO)", "NO EXIST EN SUCURSAL (MOVTO)"],
                "Cantidad": [0, 0],
                "Fecha": [Variables().date_movement_config_document(), Variables().date_movement_config_document()],
                "Hora": [Variables().date_movement_config_document(), Variables().date_movement_config_document()],
                "Comentario": ["-", "-"],
                "Usuario": ["-", "-"],
                "Departamento": ["Refacciones", "Servicio"],
                "Sucursal": [sucursal, sucursal],
                "Programa": ["Ventas Perdidas", "Ventas Perdidas"],
                "Tipo de Inventario": ["Refacciones", "Refacciones"],
                "Precio": [0, 0],
                "Clasificación": ["E", "E"],
                "Desc. Clasificación": ["Sin Eventos", "Sin Eventos"],
                "Costo": [0, 0],
                "Total": [0, 0],
                "Id. Competidor": [0, 0],
                "Competidor": ["-", "-"],
                "Precio Competidor": [0, 0],
                "Moneda Competidor": ["-", "-"]
            }
            df_sucursal = pd.DataFrame(data)
            dfs.append(df_sucursal)
            
        df_final_vacios = pd.concat(dfs, ignore_index=True)
        hora = pd.to_datetime(df_final_vacios["Hora"])
        df_final_vacios["Hora"] = hora.dt.strftime('%H:%M:%S %p').astype(str)
        df_final_vacios["Mes"] = df_final_vacios["Fecha"].apply(lambda x:self.variables.nombre_mes_base_columna(x))
                
        for column_name in df_final_vacios.columns:
            if "fecha" in column_name.lower():
                df_final_vacios = self.variables.global_date_format_dmy_mexican(df_final_vacios, column_name)

        return df_final_vacios
            
    def venta_perdida_matriz(self):
        documento = "VPMATRIZ.xls"
        self.comprobar_documento(documento)
    def venta_perdida_trebol(self):
        documento = "VPTREBOL.xls"
        self.comprobar_documento(documento)
    def venta_perdida_veracruz(self):
        documento = "VPVERACRUZ.xls"
        self.comprobar_documento(documento)
    def venta_perdida_orizaba(self):
        documento = "VPORIZABA.xls"
        self.comprobar_documento(documento)
    def venta_perdida_tehuacan(self):
        documento = "VPTEHUACAN.xls"
        self.comprobar_documento(documento)
    def venta_perdida_villahermosa(self):
        documento = "VPVILLAHERMOSA.xls"
        self.comprobar_documento(documento)
    def venta_perdida_coatzacoalcos(self):
        documento = "VPCOATZACOALCOS.xls"
        self.comprobar_documento(documento)
    def venta_perdida_merida(self):
        documento = "VPMERIDA.xls"
        self.comprobar_documento(documento)
    def venta_perdida_oaxaca(self):
        documento = "VPOAXACA.xls"
        self.comprobar_documento(documento)
    def venta_perdida_tuxtla1(self):
        documento = "VPTUXTLA1.xls"
        self.comprobar_documento(documento)
    def venta_perdida_tuxtla2(self):
        documento = "VPTUXTLA2.xls"
        self.comprobar_documento(documento)
    def comprobar_documento(self, documento):
        self.comprobar_existencia_ventasperdidas()
        ruta_completa = os.path.join(self.ruta_base, documento)

        # Verificar si el archivo existe en la ruta
        if os.path.exists(ruta_completa):
            # Procesar el archivo actual
            df = self.proceso(documento)

            if df is not None:
                # Concatenar el DataFrame procesado al DataFrame final
                print(f'documento concatenado {documento}')
                self.df_final = pd.concat([self.df_final, df], ignore_index=True)

        # Si hemos procesado algún archivo, guardar el resultado final solo una vez al final
        if not self.df_final.empty:
            # Establecer la localización en español
            print(f'documento completo y guardado {documento}')
            self.variables.guardar_xls("ventasperdidas.xls", self.df_final, self.concesionario)
        
    def proceso(self, nombre_documento):
        self.nombre_doc = nombre_documento
        path = os.path.join(self.variables.ruta_Trabajos_kwe, self.nombre_doc)

        # Leer el archivo Excel
        df = pd.read_excel(path, sheet_name=0)

        if df.empty:
            return None

        # Reemplazar los puntos y comas por guiones
        df = df.replace(to_replace=";", value="-", regex=True)
        df = df.drop(df.index[-1])  # Eliminar la última fila

        # Convertir la columna "Hora" a formato adecuado
        hora = pd.to_datetime(df["Hora"])
        df["Hora"] = hora.dt.strftime('%I:%M:%S %p').astype(str)

        # Procesar las columnas de fechas
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_america(df, column_name)

        df["Mes"] = df["Fecha"].apply(lambda x:self.variables.nombre_mes_base_columna(x))
        
        df.insert(0, "VP", 1, allow_duplicates=False)

        # Concatenar la columna "Venta Perdida"
        col_venta_perdida_concat = "VP-" + df["Venta Perdida"].astype(int).astype(str)
        df["Venta Perdida"] = col_venta_perdida_concat

        # Cargar la información de vendedores
        vendedores = pd.read_json(os.path.join(self.variables.help_directory, "VendedoresVP.json"))
        df.insert(12, column="Departamento", value="", allow_duplicates=False)

        # Mapear los departamentos
        df["Departamento"] = df['Usuario'].map(vendedores.set_index('Usuario')['Departamento'])

        # Reconvertir las fechas
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_dmy_mexican(df, column_name)

        # Convertir columnas booleanas a texto
        columnas_bol = df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        return df  # Devolver el DataFrame procesado
