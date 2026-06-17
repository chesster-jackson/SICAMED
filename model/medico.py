from paciente import Persona 

class Medico(Persona):
    def __init__(self, nombre, apellido, telefono, especialidad):
        super().__init__(nombre, apellido, telefono)
        self.especialidad = especialidad
        self.citas = []

lista_medicos = [] 

def eliminar_paciente_logica(paciente, numero_expediente):
    if numero_expediente == paciente.numero_expediente:
        return True
    return False

def atender_paciente_logica(paciente, numero_expediente):
    if numero_expediente == paciente.numero_expediente:
        return True
    return False