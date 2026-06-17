class Medicamento:
    def __init__(self, nombre,cantidad_stock):
        self.nombre = nombre
        self.__indicaciones = []
        self._cantidad_stock = cantidad_stock


    
    def agregar_indicacion(self, enfermedad, dosis, frecuencia, duracion):
        indicacion = {
            "enfermedad": enfermedad,
            "dosis": dosis,
            "frecuencia": frecuencia,
            "duracion": duracion
        }
        self.__indicaciones.append(indicacion)


    def mostrar_indicaciones(self):
        for i in self.__indicaciones:
            print(i)

    #getter retornamos la cntidad del stock
    @property
    def cantidad_stock(self):
        return self._cantidad_stock

    #m validar que no sea egativo
    @cantidad_stock.setter
    def cantidad_stock(self, valor):
        if not isinstance(valor, int) or valor < 0:
            print(" El stock no puede ser negativo")
            return
        
        self._cantidad_stock = valor

    def aumentar_stock(self, cantidad):
        if cantidad <= 0:
            print(" cantidad inválida")
            return
        
        self._cantidad_stock += cantidad
        
    def reducir_stock(self, cantidad):
        if cantidad <= 0:
            print(" cantidad inválida")
            return

        if self._cantidad_stock < cantidad:
            print(" no hay suficiente stock")
            return

        self._cantidad_stock -= cantidad