class Cita:
    def __init__(self, paciente, medico, fecha, hora, diagnostico, resultado):
        self.paciente = paciente   
        self.medico = medico      
        self.fecha = fecha
        self.hora = hora
        self.diagnostico = diagnostico
        self.resultado = resultado

lista_citas = []

def agendar_cita(paciente, medico_asignado, fecha, hora, diagnostico, resultado):
    nueva_cita = Cita(paciente, medico_asignado, fecha, hora, diagnostico, resultado)
    lista_citas.append(nueva_cita)
    return nueva_cita

def eliminar_cita(lista_citas, fecha, hora):
    for cita in lista_citas:
        if cita.fecha == fecha and cita.hora == hora:
            lista_citas.remove(cita)
            return True
    return False