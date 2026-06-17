"""
Modelo Cita
Representa una consulta médica programada
"""


class Cita:
    """Modelo de Cita"""
    
    def __init__(self, id, cedula_paciente, id_doctor,
                 fecha, hora, duracion, estado, observaciones=None):
        self.id = id
        self.cedula_paciente = cedula_paciente
        self.id_doctor = id_doctor
        self.fecha = fecha
        self.hora = hora
        self.duracion = duracion
        self.estado = estado
        self.observaciones = observaciones
    
    def to_dict(self):
        return {
            'id': self.id,
            'cedula_paciente': self.cedula_paciente,
            'id_doctor': self.id_doctor,
            'fecha': self.fecha,
            'hora': self.hora,
            'duracion': self.duracion,
            'estado': self.estado,
            'observaciones': self.observaciones
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            cedula_paciente=data.get('cedula_paciente'),
            id_doctor=data.get('id_doctor'),
            fecha=data.get('fecha'),
            hora=data.get('hora'),
            duracion=data.get('duracion'),
            estado=data.get('estado'),
            observaciones=data.get('observaciones')
        )