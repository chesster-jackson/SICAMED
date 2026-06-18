"""
Modelo Doctor - Hereda de Persona
"""

from model.persona import Persona


class Doctor(Persona):
    """Clase Doctor que hereda de Persona"""
    
    def __init__(self, nombres, apellidos, edad, cedula, id_doctor, especialidad, telefono):
        # Llamar al constructor de la clase padre
        super().__init__(nombres, apellidos, edad, cedula)
        
        # Atributos privados propios de Doctor
        self.__id_doctor = id_doctor
        self.__especialidad = especialidad
        self.__telefono = telefono
        self.__citas = []  # Lista de citas del doctor
    
    # Getter y setter para id_doctor
    @property
    def id_doctor(self):
        return self.__id_doctor
    
    @id_doctor.setter
    def id_doctor(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El ID del doctor no puede estar vacio")
        self.__id_doctor = valor.strip()
    
    # Getter y setter para especialidad
    @property
    def especialidad(self):
        return self.__especialidad
    
    @especialidad.setter
    def especialidad(self, valor):
        if not valor or not valor.strip():
            raise ValueError("La especialidad no puede estar vacia")
        self.__especialidad = valor.strip()
    
    # Getter y setter para telefono
    @property
    def telefono(self):
        return self.__telefono
    
    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor.strip() if valor else ""
    
    # Getter para citas (solo lectura)
    @property
    def citas(self):
        return self.__citas
    
    # Metodo para agregar cita al doctor
    def agregar_cita(self, cita):
        self.__citas.append(cita)
    
    # Convertir a diccionario para JSON
    def to_dict(self):
        return {
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'edad': self.edad,
            'cedula': self.cedula,
            'id_doctor': self.__id_doctor,
            'especialidad': self.__especialidad,
            'telefono': self.__telefono,
            'citas': self.__citas
        }
    
    # Crear Doctor desde diccionario
    @classmethod
    def from_dict(cls, data):
        doctor = cls(
            data.get('nombres', ''),
            data.get('apellidos', ''),
            data.get('edad', 0),
            data.get('cedula', ''),
            data.get('id_doctor', ''),
            data.get('especialidad', ''),
            data.get('telefono', '')
        )
        doctor.__citas = data.get('citas', [])
        return doctor