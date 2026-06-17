"""
Modelo Paciente - Adulto Mayor (edad >= 60 años)
"""

class Paciente:
    """Modelo de Paciente con validación de edad mínima 60 años"""
    
    def __init__(self, nombres, apellidos, edad, cedula, telefono, direccion, email=""):
        self.nombres = nombres
        self.apellidos = apellidos
        self._edad = edad  # Usamos _edad para validar en el setter
        self.cedula = cedula
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
    
    @property
    def edad(self):
        return self._edad
    
    @edad.setter
    def edad(self, valor):
        """Validar que la edad sea mayor o igual a 60"""
        try:
            valor = int(valor)
            if valor < 60:
                raise ValueError(" La edad del adulto mayor debe ser mayor o igual a 60 años")
            if valor > 120:
                raise ValueError(" La edad no puede ser mayor a 120 años")
            self._edad = valor
        except ValueError:
            raise ValueError(" La edad debe ser un número válido")
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    
    def to_dict(self):
        return {
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'edad': self._edad,
            'cedula': self.cedula,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('nombres', ''),
            data.get('apellidos', ''),
            data.get('edad', 60),
            data.get('cedula', ''),
            data.get('telefono', ''),
            data.get('direccion', ''),
            data.get('email', '')
        )