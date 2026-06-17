"""
Modelo Paciente
Representa a un adulto mayor
"""

from .persona import Persona


class Paciente(Persona):
    """Modelo de Paciente"""
    
    def __init__(self, nombres, apellidos, edad, cedula, 
                 direccion, telefono, email, alergias=None):
        super().__init__(nombres, apellidos, edad, cedula)
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.alergias = alergias or []
        self.historial = []
    
    def to_dict(self):
        return {
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'edad': self.edad,
            'cedula': self.cedula,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'alergias': self.alergias,
            'historial': self.historial
        }
    
    @classmethod
    def from_dict(cls, data):
        paciente = cls(
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            edad=data.get('edad'),
            cedula=data.get('cedula'),
            direccion=data.get('direccion'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            alergias=data.get('alergias', [])
        )
        paciente.historial = data.get('historial', [])
        return paciente