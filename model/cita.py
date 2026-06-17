class Cita:
<<<<<<< HEAD
    
    def __init__(self, id_cita, cedula_paciente, id_doctor, fecha, hora, observaciones=""):
        self.id = id_cita
        self.cedula_paciente = cedula_paciente
        self.id_doctor = id_doctor
        self.fecha = fecha
        self.hora = hora
        self.observaciones = observaciones
        self.estado = "Pendiente"
    
    def completar(self):
        self.estado = "Completada"
    
    def cancelar(self):
        self.estado = "Cancelada"
    #diccionario entrada
    def to_dict(self):
        return {
            'id': self.id,
            'cedula_paciente': self.cedula_paciente,
            'id_doctor': self.id_doctor,
            'fecha': self.fecha,
            'hora': self.hora,
            'estado': self.estado,
            'observaciones': self.observaciones
        }
    #diccionario salid
    @classmethod
    def from_dict(cls, data):
        cita = cls(
            data.get('id', 0),
            data.get('cedula_paciente', ''),
            data.get('id_doctor', ''),
            data.get('fecha', ''),
            data.get('hora', ''),
            data.get('observaciones', '')
        )
        cita.estado = data.get('estado', 'Pendiente')
        return cita
=======
    def __init__(self, paciente, medico, fecha, hora, diagnostico, resultado):
        self.paciente = paciente   
        self.medico = medico      
        self.fecha = fecha
        self.hora = hora
        self.diagnostico = diagnostico
        self.resultado = resultado

lista_citas = []

def agendar_cita(paciente, medico_asignado, fecha, hora, diagnostico, resultado):
    nueva_cita = Cita(paciente, medico_asignado, fecha, hora, diagnostico, resultado)
    lista_citas.append(nueva_cita)
    return nueva_cita

def eliminar_cita(lista_citas, fecha, hora):
    for cita in lista_citas:
        if cita.fecha == fecha and cita.hora == hora:
            lista_citas.remove(cita)
            return True
    return False
>>>>>>> 76efdd5c945283f0c69e8bf29128fc8f97a0019d
