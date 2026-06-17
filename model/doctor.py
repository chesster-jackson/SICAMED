class Doctor:
    
    def __init__(self, nombres, apellidos, edad, cedula, id_doctor, especialidad, telefono):
        self.nombres = nombres
        self.apellidos = apellidos
        self.edad = edad
        self.cedula = cedula
        self.id_doctor = id_doctor
        self.especialidad = especialidad
        self.telefono = telefono
    #getter = property
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    #dentro del diccioario
    def to_dict(self):
        return {
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'edad': self.edad,
            'cedula': self.cedula,
            'id_doctor': self.id_doctor,
            'especialidad': self.especialidad,
            'telefono': self.telefono
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('nombres', ''),
            data.get('apellidos', ''),
            data.get('edad', 0),
            data.get('cedula', ''),
            data.get('id_doctor', ''),
            data.get('especialidad', ''),
            data.get('telefono', '')
        )