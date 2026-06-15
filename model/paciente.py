class Persona:
    def __init__(self, nombre, apellido, telefono=None, cedula=None):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.cedula = cedula

class Paciente(Persona):
    def __init__(self, nombre, apellido, edad, numero_expediente, genero, telefono=None, cedula=None):
        super().__init__(nombre, apellido, telefono, cedula)
        self.edad = int(edad)
        self.numero_expediente = numero_expediente
        self.genero = genero

lista_pacientes = []

def registrar_paciente_en_sistema(nombre, apellido, edad, numero_expediente, genero):
    nuevo_paciente = Paciente(nombre, apellido, edad, numero_expediente, genero)
    lista_pacientes.append(nuevo_paciente)
    return nuevo_paciente