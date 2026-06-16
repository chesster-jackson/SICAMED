from model.cita import Cita
from model.paciente import Paciente
from model.doctor import Doctor
from model.persona import Persona

class Sistema:
    def __init__(self):
        self.pacientes = {}   
        self.doctores = {}    
        self.citas = []       

    # AGREGAR PACIENTE
    def agregar_paciente(self, paciente):
        if paciente.cedula in self.pacientes:
            print(" Paciente ya existe")
            return
        
        self.pacientes[paciente.cedula] = paciente
        print(" Paciente agregado")

    #  BUSCAR PACIENTE
    def buscar_paciente(self, cedula):
        return self.pacientes.get(cedula)

    #  BUSCAR O CREAR PACIENTE
    def buscar_o_crear_paciente(self, nombres, apellidos, edad, cedula, direccion, telefono):
        paciente = self.buscar_paciente(cedula)

        if paciente:
            print(" Paciente encontrado")
            return paciente

        nuevo = Paciente(nombres, apellidos, edad, cedula, direccion, telefono)
        self.pacientes[cedula] = nuevo
        print(" Paciente creado")
        return nuevo

    #  AGREGAR DOCTOR
    def agregar_doctor(self, doctor):
        if doctor.id_doctor in self.doctores:
            print(" Doctor ya existe")
            return
        
        self.doctores[doctor.id_doctor] = doctor
        print(" Doctor agregado")

    #  ASIGNAR DOCTOR
    def asignar_doctor(self, cedula, id_doctor):
        paciente = self.buscar_paciente(cedula)
        doctor = self.doctores.get(id_doctor)

        if not paciente or not doctor:
            print(" Error paciente o doctor")
            return

        paciente.asignar_doctor(doctor)
        print(" Doctor asignado")

    #  CREAR CITA
    def crear_cita(self, cedula, id_doctor, fecha):
        paciente = self.buscar_paciente(cedula)
        doctor = self.doctores.get(id_doctor)

        if not paciente or not doctor:
            print(" Error al craer cita ")
            return

        # validar que doctor no esté ocupado
        for c in self.citas:
            if c.fecha == fecha and c.doctor.id_doctor == id_doctor:
                print(" Doctor ocupado ")
                return

        nueva = Cita(paciente, doctor, fecha)
        self.citas.append(nueva)

        paciente.agregar_historial(
            f"Cita el {fecha} con Dr {doctor._nombres} {doctor._apellidos}")

    #  VER CITAS
    def ver_citas(self):
        for c in self.citas:
            print(f"Fecha : {c.fecha},Nombre: {c.paciente.nombres},Cita con:{c.doctor.especialidad} , DR {c.doctor._nombres} {c.doctor._apellidos}")

    #  ASIGNAR MEDICAMENTO
    def asignar_medicamento(self, cedula, medicamento):
        paciente = self.buscar_paciente(cedula)

        if not paciente:
            print(" Paciente no existe ")
            return

        paciente.agregar_medicamento(medicamento)
        print(" Medicamento asignado ")

    #  ADMINISTRAR MEDICAMENTO
    def administrar_medicamento(self, cedula, nombre,cantidad):
        paciente = self.buscar_paciente(cedula)

        if not paciente:
            print(" Paciente no existe ")
            return

        for m in paciente._medicamentos:
            if m.nombre == nombre:
                if m.cantidad_stock <= 0:
                    print(" No hay medicamento ")
                    return

                m.reducir_stock(cantidad)
                paciente.agregar_historial(f"Se administró {m.nombre}")
                print(" Medicamento administrado ")
                print(f"Quedan {m.cantidad_stock} unidades")
                return

    #  ALERTAS
    def alertas(self, cedula):
        paciente = self.buscar_paciente(cedula)

        if not paciente:
            return

        for m in paciente._medicamentos:
            if m.cantidad_stock <= 2:
                print(f" {m.nombre} bajo stock ")
