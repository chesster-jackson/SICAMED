"""
Modelo base Persona
Clase abstracta para pacientes y doctores
"""

from abc import ABC, abstractmethod


class Persona(ABC):
    """Clase base para personas del sistema"""
    
    def __init__(self, nombres, apellidos, edad, cedula):
        self.nombres = nombres
        self.apellidos = apellidos
        self.edad = edad
        self.cedula = cedula
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    
    @abstractmethod
    def to_dict(self):
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass