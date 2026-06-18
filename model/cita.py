"""
Modelo Cita
"""

class Cita:
    """Modelo de Cita con atributos privados"""
    
    def __init__(self, id_cita, cedula_paciente, id_doctor, fecha, hora, observaciones=""):
        self.__id = id_cita
        self.__cedula_paciente = cedula_paciente
        self.__id_doctor = id_doctor
        self.__fecha = fecha
        self.__hora = hora
        self.__observaciones = observaciones
        self.__estado = "Pendiente"  # Pendiente, Completada, Cancelada
    
    # Getters (solo lectura para algunos atributos)
    @property
    def id(self):
        return self.__id
    
    @property
    def cedula_paciente(self):
        return self.__cedula_paciente
    
    @property
    def id_doctor(self):
        return self.__id_doctor
    
    @property
    def fecha(self):
        return self.__fecha
    
    @fecha.setter
    def fecha(self, valor):
        self.__fecha = valor
    
    @property
    def hora(self):
        return self.__hora
    
    @hora.setter
    def hora(self, valor):
        self.__hora = valor
    
    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor):
        self.__estado = valor
    
    # Metodos para cambiar estado
    def completar(self):
        """Cambia el estado a Completada"""
        self.__estado = "Completada"
    
    def cancelar(self):
        """Cambia el estado a Cancelada"""
        self.__estado = "Cancelada"
    
    # Convertir a diccionario para JSON
    def to_dict(self):
        return {
            'id': self.__id,
            'cedula_paciente': self.__cedula_paciente,
            'id_doctor': self.__id_doctor,
            'fecha': self.__fecha,
            'hora': self.__hora,
            'estado': self.__estado,
            'observaciones': self.__observaciones
        }
    
    # Crear Cita desde diccionario
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
        cita.__estado = data.get('estado', 'Pendiente')
        return cita