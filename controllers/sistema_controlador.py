"""
Controlador Principal - Logica de negocio con validaciones
"""

import json
import os
import re
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
    
    # ===== PERSISTENCIA EN JSON =====
    
    def cargar_datos(self):
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Cargar pacientes filtrando None
                self.pacientes = []
                for p in data.get('pacientes', []):
                    paciente = Paciente.from_dict(p)
                    if paciente is not None:
                        self.pacientes.append(paciente)
                
                # Cargar doctores filtrando None
                self.doctores = []
                for d in data.get('doctores', []):
                    doctor = Doctor.from_dict(d)
                    if doctor is not None:
                        self.doctores.append(doctor)
                
                # Cargar citas filtrando None
                self.citas = []
                for c in data.get('citas', []):
                    cita = Cita.from_dict(c)
                    if cita is not None:
                        self.citas.append(cita)
        except:
            self.pacientes = []
            self.doctores = []
            self.citas = []
    
    def guardar_datos(self):
        try:
            os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
            data = {
                'pacientes': [p.to_dict() for p in self.pacientes if p is not None],
                'doctores': [d.to_dict() for d in self.doctores if d is not None],
                'citas': [c.to_dict() for c in self.citas if c is not None]
            }
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    # ===== VALIDACIONES DE TELÉFONO =====
    
    def validar_telefono_unico(self, telefono, excluir_cedula=None, excluir_id_doctor=None):
        
        if not telefono:  # Si el teléfono está vacío, es opcional
            return True
        
        # Buscar en pacientes
        for p in self.pacientes:
            if p.telefono == telefono:
                # Si estamos excluyendo un paciente y es el mismo, permitir
                if excluir_cedula and p.cedula == excluir_cedula:
                    continue
                return False
        
        # Buscar en doctores
        for d in self.doctores:
            if d.telefono == telefono:
                # Si estamos excluyendo un doctor y es el mismo, permitir
                if excluir_id_doctor and d.id_doctor == excluir_id_doctor:
                    continue
                return False
        
        return True
    
    def validar_telefono_con_mensaje(self, telefono, excluir_cedula=None, excluir_id_doctor=None):
        """
        Valida el teléfono y retorna mensaje descriptivo
        Retorna (bool, mensaje)
        """
        if not telefono:  # Teléfono opcional
            return True, "Teléfono opcional"
        
        # Validar que solo tenga números
        if not telefono.isdigit():
            return False, " El teléfono solo debe contener números"
        
        # Validar longitud mínima (8 dígitos)
        if len(telefono) < 8:
            return False, " El teléfono debe tener al menos 8 dígitos"
        
        # Validar longitud máxima (15 dígitos)
        if len(telefono) > 8:
            return False, " El teléfono no puede tener más de 8 dígitos"
        
        # Validar que no esté duplicado
        if not self.validar_telefono_unico(telefono, excluir_cedula, excluir_id_doctor):
            return False, " Este número de teléfono ya está registrado en el sistema"
        
        return True, " Teléfono válido"
    
    # ===== PACIENTES =====
    
    def obtener_pacientes(self):
        """Retorna lista de pacientes filtrando None"""
        return [p for p in self.pacientes if p is not None]
    
    def buscar_paciente(self, cedula):
        for p in self.pacientes:
            if p is not None and p.cedula == cedula:
                return p
        return None
    
    def registrar_paciente(self, nombres, apellidos, edad, cedula, telefono, direccion, email=""):
        """Registrar paciente - Validación completa"""
        
        # Validar que no exista como paciente
        if self.buscar_paciente(cedula):
            raise ValueError(f" Ya existe un paciente con cédula {cedula}")
        
        # Validar que no exista como doctor
        if self.buscar_doctor_by_cedula(cedula):
            raise ValueError(f" La cédula {cedula} ya está registrada como doctor")
        
        # Validar formato de cédula
        patron = r'^\d{3}-\d{6}-\d{4}[A-Za-z]$'
        if not re.match(patron, cedula):
            raise ValueError(" Formato de cédula inválido. Debe ser: 123-123456-1234A")
        
        # Validar nombres (solo letras y espacios)
        if not all(c.isalpha() or c.isspace() for c in nombres):
            raise ValueError("Los nombres solo pueden contener letras y espacios")
        
        if not all(c.isalpha() or c.isspace() for c in apellidos):
            raise ValueError(" Los apellidos solo pueden contener letras y espacios")
        
        # Validar edad
        try:
            edad = int(edad)
            if edad < 60:
                raise ValueError("El paciente debe ser mayor de 60 años (Adulto Mayor)")
            if edad > 120:
                raise ValueError(" La edad no puede ser mayor a 120 años")
        except ValueError:
            raise ValueError(" La edad debe ser un número válido")
        
        #  VALIDAR TELÉFONO ÚNICO
        if telefono:
            es_valido, mensaje = self.validar_telefono_con_mensaje(telefono)
            if not es_valido:
                raise ValueError(mensaje)
        
        paciente = Paciente(nombres, apellidos, edad, cedula, telefono, direccion, email)
        self.pacientes.append(paciente)
        self.guardar_datos()
        return paciente
    
    def actualizar_paciente(self, cedula, nombres, apellidos, edad, telefono, direccion, email=""):
        """Actualizar paciente - Con validaciones"""
        paciente = self.buscar_paciente(cedula)
        if not paciente:
            raise ValueError(" Paciente no encontrado")
        
        # Validar nombres (solo letras y espacios)
        if not all(c.isalpha() or c.isspace() for c in nombres):
            raise ValueError("Los nombres solo pueden contener letras y espacios")
        
        if not all(c.isalpha() or c.isspace() for c in apellidos):
            raise ValueError(" Los apellidos solo pueden contener letras y espacios")
        
        # VALIDAR TELÉFONO ÚNICO (excluyendo al mismo paciente)
        if telefono:
            es_valido, mensaje = self.validar_telefono_con_mensaje(telefono, excluir_cedula=cedula)
            if not es_valido:
                raise ValueError(mensaje)
        
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
            raise ValueError("Paciente no encontrado")
        
        self.pacientes = [p for p in self.pacientes if p is not None and p.cedula != cedula]
        self.guardar_datos()
        return True
    
    # ===== DOCTORES =====
    
    def obtener_doctores(self):
        """Retorna lista de doctores filtrando None"""
        return [d for d in self.doctores if d is not None]
    
    def buscar_doctor(self, id_doctor):
        for d in self.doctores:
            if d is not None and d.id_doctor == id_doctor:
                return d
        return None
    
    def buscar_doctor_by_cedula(self, cedula):
        """Buscar doctor por cédula"""
        for d in self.doctores:
            if d is not None and d.cedula == cedula:
                return d
        return None
    
    def registrar_doctor(self, nombres, apellidos, edad, cedula, id_doctor, especialidad, telefono):
        """Registrar doctor - Validación completa"""
        
        if self.buscar_doctor(id_doctor):
            raise ValueError(f" Ya existe un doctor con ID {id_doctor}")
        
        # Validar que la cédula no pertenezca a un paciente
        if self.buscar_paciente(cedula):
            raise ValueError(f" La cédula {cedula} ya está registrada como paciente")
        
        # Validar que la cédula no pertenezca a otro doctor
        if self.buscar_doctor_by_cedula(cedula):
            raise ValueError(f" Ya existe un doctor con cédula {cedula}")
        
        # Validar nombres (solo letras y espacios)
        if not all(c.isalpha() or c.isspace() for c in nombres):
            raise ValueError(" Los nombres solo pueden contener letras y espacios")
        
        if not all(c.isalpha() or c.isspace() for c in apellidos):
            raise ValueError(" Los apellidos solo pueden contener letras y espacios")
        
        # Validar formato de cédula
        patron = r'^\d{3}-\d{6}-\d{4}[A-Za-z]$'
        if not re.match(patron, cedula):
            raise ValueError(" Formato de cédula inválido. Debe ser: 123-123456-1234A")
        
        # Validar edad (18 años mínimo)
        try:
            edad = int(edad)
            if edad < 18:
                raise ValueError(" El doctor debe tener al menos 18 años")
            if edad > 80:
                raise ValueError(" La edad del doctor no puede ser mayor a 80 años")
        except ValueError:
            raise ValueError(" La edad debe ser un número válido")
        
        #  VALIDAR TELÉFONO ÚNICO
        if telefono:
            es_valido, mensaje = self.validar_telefono_con_mensaje(telefono)
            if not es_valido:
                raise ValueError(mensaje)
        
        doctor = Doctor(nombres, apellidos, edad, cedula, id_doctor, especialidad, telefono)
        self.doctores.append(doctor)
        self.guardar_datos()
        return doctor
    
    def actualizar_doctor(self, id_doctor, nombres, apellidos, edad, cedula, especialidad, telefono):
        """Actualizar datos de un doctor - Con validaciones"""
        doctor = self.buscar_doctor(id_doctor)
        if not doctor:
            raise ValueError(" Doctor no encontrado")
        
        # Validar nombres (solo letras y espacios)
        if not all(c.isalpha() or c.isspace() for c in nombres):
            raise ValueError(" Los nombres solo pueden contener letras y espacios")
        
        if not all(c.isalpha() or c.isspace() for c in apellidos):
            raise ValueError(" Los apellidos solo pueden contener letras y espacios")
        
        # Validar formato de cédula
        patron = r'^\d{3}-\d{6}-\d{4}[A-Za-z]$'
        if not re.match(patron, cedula):
            raise ValueError(" Formato de cédula inválido. Debe ser: 123-123456-1234A")
        
        # Validar que la nueva cédula no pertenezca a un paciente
        if self.buscar_paciente(cedula):
            raise ValueError(f" La cédula {cedula} ya está registrada como paciente")
        
        # Validar que la nueva cédula no pertenezca a otro doctor
        otro_doctor = self.buscar_doctor_by_cedula(cedula)
        if otro_doctor and otro_doctor.id_doctor != id_doctor:
            raise ValueError(f"Ya existe un doctor con cédula {cedula}")
        
        # 🔥 VALIDAR TELÉFONO ÚNICO (excluyendo al mismo doctor)
        if telefono:
            es_valido, mensaje = self.validar_telefono_con_mensaje(telefono, excluir_id_doctor=id_doctor)
            if not es_valido:
                raise ValueError(mensaje)
        
        try:
            edad = int(edad)
            if edad < 18:
                raise ValueError(" El doctor debe tener al menos 18 años")
            if edad > 80:
                raise ValueError("La edad del doctor no puede ser mayor a 80 años")
        except ValueError:
            raise ValueError("La edad debe ser un número válido")
        
        doctor.nombres = nombres
        doctor.apellidos = apellidos
        doctor.edad = edad
        doctor.cedula = cedula
        doctor.especialidad = especialidad
        doctor.telefono = telefono
        
        self.guardar_datos()
        return doctor
    
    def eliminar_doctor(self, id_doctor):
        doctor = self.buscar_doctor(id_doctor)
        if not doctor:
            raise ValueError("Doctor no encontrado")
        
        self.doctores = [d for d in self.doctores if d is not None and d.id_doctor != id_doctor]
        self.guardar_datos()
        return True
    
    # ===== CITAS =====
    
    def obtener_citas(self):
        """Retorna lista de citas filtrando None"""
        return [c for c in self.citas if c is not None]
    
    def agendar_cita(self, cedula_paciente, id_doctor, fecha, hora, observaciones=""):
        paciente = self.buscar_paciente(cedula_paciente)
        if not paciente:
            raise ValueError("Paciente no encontrado")
        
        if paciente.edad < 60:
            raise ValueError(" Solo se pueden agendar citas para Adultos Mayores (60+ años)")
        
        if not self.buscar_doctor(id_doctor):
            raise ValueError(" Doctor no encontrado")
        
        # Validación 1: No puede haber 2 citas iguales
        for c in self.citas:
            if c is not None and (c.cedula_paciente == cedula_paciente and 
                c.id_doctor == id_doctor and 
                c.fecha == fecha and 
                c.hora == hora):
                raise ValueError("Ya existe una cita agendada con el mismo paciente, doctor, fecha y hora")
        
        # Validación 2: No puede haber citas con el mismo doctor a la misma hora
        for c in self.citas:
            if c is not None and (c.id_doctor == id_doctor and 
                c.fecha == fecha and 
                c.hora == hora):
                raise ValueError(f" El doctor ya tiene una cita agendada para el {fecha} a las {hora}")
        
        nuevo_id = max([c.id for c in self.citas if c is not None]) + 1 if self.citas else 1
        
        cita = Cita(nuevo_id, cedula_paciente, id_doctor, fecha, hora, observaciones)
        self.citas.append(cita)
        self.guardar_datos()
        return cita
    
    def completar_cita(self, id_cita):
        cita = next((c for c in self.citas if c is not None and c.id == id_cita), None)
        if not cita:
            raise ValueError("Cita no encontrada")
        cita.completar()
        self.guardar_datos()
        return cita
    
    def cancelar_cita(self, id_cita):
        cita = next((c for c in self.citas if c is not None and c.id == id_cita), None)
        if not cita:
            raise ValueError("Cita no encontrada")
        cita.cancelar()
        self.guardar_datos()
        return cita
    
    def eliminar_cita(self, id_cita):
        cita = next((c for c in self.citas if c is not None and c.id == id_cita), None)
        if not cita:
            raise ValueError("Cita no encontrada")
        self.citas = [c for c in self.citas if c is not None and c.id != id_cita]
        self.guardar_datos()
        return True
    
    # ===== ESTADISTICAS =====
    
    def contar_pacientes(self):
        return len([p for p in self.pacientes if p is not None])
    
    def contar_doctores(self):
        return len([d for d in self.doctores if d is not None])
    
    def contar_citas(self):
        return len([c for c in self.citas if c is not None])