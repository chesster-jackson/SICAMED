"""
Modelo Cita
"""

class Cita:
    """Modelo de Cita"""
    
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