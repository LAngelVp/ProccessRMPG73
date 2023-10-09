import datetime
# contenedor de la fecha movimiento
class ContenedorVariable:
    def __init__(self, fecha_movimiento = None):
        if fecha_movimiento is None:
            self.fecha_movimiento = datetime.date.today()
        else:
            self.fecha_movimiento = fecha_movimiento
    def mostrar_fechaMovimiento(self):
        return self.fecha_movimiento
    def modificar_fechaMovimiento(self, fecha_movimiento):
        self.fecha_movimiento = fecha_movimiento
        return self.fecha_movimiento
    
class ClaseParaAsignarFechaMovimiento():
    def asignacion_fecha_movimiento_hacia_contenedor(self, contenedor, nueva_fecha):
        contenedor.modificar_fechaMovimiento(nueva_fecha)

class ClaseMostradora:
    def mostrar_fecha_desde_contenedor(self, contenedor):
        fecha = contenedor.mostrar_fechaMovimiento()
        print(f"La fecha almacenada es: {fecha}")

#FechaMovimiento("2020-12-20").modificar_fechaMovimiento("2021-02-24")