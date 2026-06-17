"""
Controlador Principal - Lógica de negocio con validaciones
"""

import json
import os
from model.paciente import Paciente
from model.doctor import Doctor
from model.cita import Cita


class SistemaControlador:
    """Controlador principal - Gestiona todas las operaciones del sistema"""
    
    def __init__(self):
        self.pacientes = []
        self.doctores = []
        self.citas = []
        self.archivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'datos.json')
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar datos desde JSON"""
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.pacientes = [Paciente.from_dict(p) for p in data.get('pacientes', [])]
                self.doctores = [Doctor.from_dict(d) for d in data.get('doctores', [])]
                self.citas = [Cita.from_dict(c) for c in data.get('citas', [])]
        except:
            self.pacientes = []
            self.doctores = []
            self.citas = []
    
    def guardar_datos(self):
        """Guardar datos en JSON"""
        try:
            os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
            data = {
                'pacientes': [p.to_dict() for p in self.pacientes],
                'doctores': [d.to_dict() for d in self.doctores],
                'citas': [c.to_dict() for c in self.citas]
            }
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    # ===== CRUD PACIENTES =====
    
    def obtener_pacientes(self):
        return self.pacientes.copy()
    
    def buscar_paciente(self, cedula):
        for p in self.pacientes:
            if p.cedula == cedula:
                return p
        return None
    
    def registrar_paciente(self, nombres, apellidos, edad, cedula, telefono, direccion, email=""):
        """Registrar nuevo paciente con validación de edad >= 60"""
        
        # Validar que no exista
        if self.buscar_paciente(cedula):
            raise ValueError(f" Ya existe un paciente con cédula {cedula}")
        
        # Validar cédula (8 dígitos)
        if not cedula.isdigit() or len(cedula) != 8:
            raise ValueError(" La cédula debe tener 8 dígitos")
        
        # Validar edad (mayor o igual a 60)
        try:
            edad = int(edad)
            if edad < 60:
                raise ValueError(" El paciente debe ser mayor de 60 años (Adulto Mayor)")
            if edad > 120:
                raise ValueError(" La edad no puede ser mayor a 120 años")
        except ValueError:
            raise ValueError(" La edad debe ser un número válido")
        
        paciente = Paciente(nombres, apellidos, edad, cedula, telefono, direccion, email)
        self.pacientes.append(paciente)
        self.guardar_datos()
        return paciente
    
    def actualizar_paciente(self, cedula, nombres, apellidos, edad, telefono, direccion, email=""):
        """Actualizar paciente con validación de edad >= 60"""
        paciente = self.buscar_paciente(cedula)
        if not paciente:
            raise ValueError(" Paciente no encontrado")
        
        # Validar edad (mayor o igual a 60)
        try:
            edad = int(edad)
            if edad < 60:
                raise ValueError(" El paciente debe ser mayor de 60 años (Adulto Mayor)")
            if edad > 120:
                raise ValueError(" La edad no puede ser mayor a 120 años")
        except ValueError:
            raise ValueError(" La edad debe ser un número válido")
        
        paciente.nombres = nombres
        paciente.apellidos = apellidos
        paciente.edad = edad
        paciente.telefono = telefono
        paciente.direccion = direccion
        paciente.email = email
        
        self.guardar_datos()
        return paciente
    
    def eliminar_paciente(self, cedula):
        paciente = self.buscar_paciente(cedula)
        if not paciente:
            raise ValueError(" Paciente no encontrado")
        
        self.pacientes = [p for p in self.pacientes if p.cedula != cedula]
        self.guardar_datos()
        return True
    
    # ===== CRUD DOCTORES =====
    
    def obtener_doctores(self):
        return self.doctores.copy()
    
    def buscar_doctor(self, id_doctor):
        for d in self.doctores:
            if d.id_doctor == id_doctor:
                return d
        return None
    
    def registrar_doctor(self, nombres, apellidos, edad, cedula, id_doctor, especialidad, telefono):
        """Registrar nuevo doctor"""
        if self.buscar_doctor(id_doctor):
            raise ValueError(f" Ya existe un doctor con ID {id_doctor}")
        
        # Validar edad del doctor
        try:
            edad = int(edad)
            if edad < 25:
                raise ValueError(" El doctor debe tener al menos 25 años")
            if edad > 80:
                raise ValueError(" La edad del doctor no puede ser mayor a 80 años")
        except ValueError:
            raise ValueError(" La edad debe ser un número válido")
        
        doctor = Doctor(nombres, apellidos, edad, cedula, id_doctor, especialidad, telefono)
        self.doctores.append(doctor)
        self.guardar_datos()
        return doctor
    
    # ===== CRUD CITAS =====
    
    def obtener_citas(self):
        return self.citas.copy()
    
    def agendar_cita(self, cedula_paciente, id_doctor, fecha, hora, observaciones=""):
        """Agendar nueva cita - verifica que el paciente sea adulto mayor"""
        
        paciente = self.buscar_paciente(cedula_paciente)
        if not paciente:
            raise ValueError(" Paciente no encontrado")
        
        # Verificar que el paciente sea adulto mayor
        if paciente.edad < 60:
            raise ValueError(" Solo se pueden agendar citas para Adultos Mayores (60+ años)")
        
        if not self.buscar_doctor(id_doctor):
            raise ValueError(" Doctor no encontrado")
        
        nuevo_id = max([c.id for c in self.citas]) + 1 if self.citas else 1
        
        cita = Cita(nuevo_id, cedula_paciente, id_doctor, fecha, hora, observaciones)
        self.citas.append(cita)
        self.guardar_datos()
        return cita
    
    def completar_cita(self, id_cita):
        cita = next((c for c in self.citas if c.id == id_cita), None)
        if not cita:
            raise ValueError(" Cita no encontrada")
        cita.completar()
        self.guardar_datos()
        return cita
    
    def cancelar_cita(self, id_cita):
        cita = next((c for c in self.citas if c.id == id_cita), None)
        if not cita:
            raise ValueError(" Cita no encontrada")
        cita.cancelar()
        self.guardar_datos()
        return cita