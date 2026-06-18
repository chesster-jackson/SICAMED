"""
Clase base Persona - Para que Paciente y Doctor hereden
"""

import re


class Persona:
    """Clase base para personas del sistema"""
    
    def __init__(self, nombres, apellidos, edad, cedula):
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__edad = edad
        self.__cedula = cedula
    
    # ===== GETTERS Y SETTERS PARA NOMBRES =====
    
    @property
    def nombres(self):
        return self.__nombres
    
    @nombres.setter
    def nombres(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Los nombres no pueden estar vacios")
        
        # Validar que solo tenga letras y espacios
        if not all(c.isalpha() or c.isspace() for c in valor):
            raise ValueError("Los nombres solo pueden contener letras y espacios")
        
        self.__nombres = valor.strip()
    
    # ===== GETTERS Y SETTERS PARA APELLIDOS =====
    
    @property
    def apellidos(self):
        return self.__apellidos
    
    @apellidos.setter
    def apellidos(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Los apellidos no pueden estar vacios")
        
        # Validar que solo tenga letras y espacios
        if not all(c.isalpha() or c.isspace() for c in valor):
            raise ValueError("Los apellidos solo pueden contener letras y espacios")
        
        self.__apellidos = valor.strip()
    
    # ===== GETTERS Y SETTERS PARA EDAD =====
    
    @property
    def edad(self):
        return self.__edad
    
    @edad.setter
    def edad(self, valor):
        try:
            valor = int(valor)
            if valor < 0 or valor > 120:
                raise ValueError("La edad debe estar entre 0 y 120")
            self.__edad = valor
        except ValueError:
            raise ValueError("La edad debe ser un numero valido")
    
    # ===== GETTERS Y SETTERS PARA CEDULA =====
    
    @property
    def cedula(self):
        return self.__cedula
    
    @cedula.setter
    def cedula(self, valor):
        if not valor or not valor.strip():
            raise ValueError("La cedula no puede estar vacia")
        
        # Validar formato: 123-123456-1234A
        # Permite: numeros, guiones y una letra al final
        patron = r'^\d{3}-\d{6}-\d{4}[A-Za-z]$'
        
        if not re.match(patron, valor.strip()):
            raise ValueError("Formato de cedula invalido. Debe ser: 123-123456-1234A")
        
        self.__cedula = valor.strip()
    
    # ===== PROPIEDAD NOMBRE COMPLETO =====
    
    @property
    def nombre_completo(self):
        return f"{self.__nombres} {self.__apellidos}"
    
    # ===== METODOS PARA JSON =====
    
    def to_dict(self):
        return {
            'nombres': self.__nombres,
            'apellidos': self.__apellidos,
            'edad': self.__edad,
            'cedula': self.__cedula
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('nombres', ''),
            data.get('apellidos', ''),
            data.get('edad', 0),
            data.get('cedula', '')
        )