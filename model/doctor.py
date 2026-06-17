"""
Modelo Doctor
Representa a un profesional médico
"""

from .persona import Persona


class Doctor(Persona):
    """Modelo de Doctor"""
    
    def __init__(self, nombres, apellidos, edad, cedula,
                 id_doctor, especialidad, telefono, email):
        super().__init__(nombres, apellidos, edad, cedula)
        self.id_doctor = id_doctor
        self.especialidad = especialidad
        self.telefono = telefono
        self.email = email
        self.citas = []
    
    def to_dict(self):
        return {
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'edad': self.edad,
            'cedula': self.cedula,
            'id_doctor': self.id_doctor,
            'especialidad': self.especialidad,
            'telefono': self.telefono,
            'email': self.email,
            'citas': self.citas
        }
    
    @classmethod
    def from_dict(cls, data):
        doctor = cls(
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            edad=data.get('edad'),
            cedula=data.get('cedula'),
            id_doctor=data.get('id_doctor'),
            especialidad=data.get('especialidad'),
            telefono=data.get('telefono'),
            email=data.get('email')
        )
        doctor.citas = data.get('citas', [])
        return doctor