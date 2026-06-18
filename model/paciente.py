"""
Modelo Paciente - Hereda de Persona
"""

from model.persona import Persona


class Paciente(Persona):
    """Clase Paciente que hereda de Persona"""
    
    def __init__(self, nombres, apellidos, edad, cedula, telefono, direccion, email=""):
        # Llamar al constructor de la clase padre
        super().__init__(nombres, apellidos, edad, cedula)
        
        # Atributos privados propios de Paciente
        self.__telefono = telefono
        self.__direccion = direccion
        self.__email = email
        self.__historial = []  # Lista de citas del paciente
    
    # Getter y setter para telefono
    @property
    def telefono(self):
        return self.__telefono
    
    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor.strip() if valor else ""
    
    # Getter y setter para direccion
    @property
    def direccion(self):
        return self.__direccion
    
    @direccion.setter
    def direccion(self, valor):
        self.__direccion = valor.strip() if valor else ""
    
    # Getter y setter para email
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, valor):
        self.__email = valor.strip() if valor else ""
    
    # Getter para historial (solo lectura)
    @property
    def historial(self):
        return self.__historial
    
    # Metodo para agregar cita al historial
    def agregar_cita(self, cita):
        self.__historial.append(cita)
    
    # Convertir a diccionario para JSON
    def to_dict(self):
        return {
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'edad': self.edad,
            'cedula': self.cedula,
            'telefono': self.__telefono,
            'direccion': self.__direccion,
            'email': self.__email,
            'historial': self.__historial
        }
    
    # Crear Paciente desde diccionario
    @classmethod
    def from_dict(cls, data):
        paciente = cls(
            data.get('nombres', ''),
            data.get('apellidos', ''),
            data.get('edad', 60),
            data.get('cedula', ''),
            data.get('telefono', ''),
            data.get('direccion', ''),
            data.get('email', '')
        )
        paciente.__historial = data.get('historial', [])
        return paciente