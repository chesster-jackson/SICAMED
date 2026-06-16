from model.persona import Persona

class Paciente(Persona):
    def __init__(self, nombres, apellidos, edad, cedula , direccion , telefono ):
        super().__init__(nombres, apellidos, edad, cedula)

        self._medicamentos = []
        self._enfermedades = []
        self._historial = []
        self._doctor = None
        self.direccion = direccion
        self.telefono = telefono


    def agregar_medicamento(self, medicamento):
        self._medicamentos.append(medicamento)
        

    def agregar_enfermedad(self, enfermedad):
        self._enfermedades.append(enfermedad)

    def agregar_historial(self, evento):
        self._historial.append(evento)

    def asignar_doctor(self, doctor):
        self._doctor = doctor

    @property
    def nombres(self):
        return self._nombres

    @nombres.setter
    def nombres(self, valor):
        if valor == "" or len(valor) < 2:
            print("Nombre inválido")
            return
        self._nombres = valor 

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        if valor < 0 or valor > 120:
            print(" Edad inválida")
            return
        self._edad = valor

    @property
    def cedula(self):
        return self._cedula

    @cedula.setter
    def cedula(self, valor):
        if valor == "":
            print("Cédula inválida")
            return
        self._cedula = valor

    @property
    def apellidos(self):
        return self._apellidos

    @apellidos.setter
    def apellidos(self, valor):
        if valor == "":
            print(" Apellido inválido")
            return
        self._apellidos = valor

    def obtener_datos(self):
        return {
            "nombres": self._nombres,
            "apellidos": self._apellidos,
            "edad": self._edad,
            "cedula": self._cedula,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "doctor": self._doctor.nombres if self._doctor else None,
            "medicamentos": [m.nombre for m in self._medicamentos],
            "enfermedades": self._enfermedades,
            "historial": self._historial
        }
