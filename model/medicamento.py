class Medicamento:
    def __init__(self, nombre, dosis, precio, stock):
        self.nombre = nombre
        self.dosis = dosis
        self.precio = float(precio)  
        self.stock = int(stock)

inventario_medicamentos = []

def agregar_medicamento_logica(nombre, dosis, precio, stock):
    nuevo_medicamento = Medicamento(nombre, dosis, precio, stock)
    inventario_medicamentos.append(nuevo_medicamento)
    return nuevo_medicamento

def eliminar_medicamento_logica(nombre_a_buscar):
    for med in inventario_medicamentos:
        if med.nombre.lower() == nombre_a_buscar.lower():
            inventario_medicamentos.remove(med)
            return True
    return False