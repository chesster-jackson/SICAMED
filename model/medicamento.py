"""
Modelo Medicamento
Representa medicamentos recetados
"""


class Medicamento:
    """Modelo de Medicamento"""
    
    def __init__(self, id_medicamento, nombre, dosis, 
                 frecuencia, indicaciones):
        self.id_medicamento = id_medicamento
        self.nombre = nombre
        self.dosis = dosis
        self.frecuencia = frecuencia
        self.indicaciones = indicaciones
    
    def to_dict(self):
        return {
            'id_medicamento': self.id_medicamento,
            'nombre': self.nombre,
            'dosis': self.dosis,
            'frecuencia': self.frecuencia,
            'indicaciones': self.indicaciones
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id_medicamento=data.get('id_medicamento'),
            nombre=data.get('nombre'),
            dosis=data.get('dosis'),
            frecuencia=data.get('frecuencia'),
            indicaciones=data.get('indicaciones')
        )