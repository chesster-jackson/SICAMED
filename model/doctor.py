from model.persona import Persona
class Doctor(Persona):
    def __init__(self, nombres, apellidos, edad, cedula, especialidad, id_doctor):
        super().__init__(nombres, apellidos, edad, cedula)
        
        self.especialidad = especialidad
        self.id_doctor = id_doctor

    @property
    def especialidad_doctor(self):
        return self._especialidad

    @especialidad_doctor.setter
    def especialidad_doctor(self, valor):
        if valor == "" or not valor.replace(" ", "").isalpha():
            print(" Especialidad inválida (solo letras)")
            return

        self._especialidad = valor