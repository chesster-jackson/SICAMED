"""
Controlador Principal del Sistema
Maneja todas las rutas y la lógica de negocio
"""

from flask import Blueprint, render_template, request, jsonify
from model.paciente import Paciente
from model.doctor import Doctor
from model.cita import Cita
import json
import os

sistema_bp = Blueprint('sistema', __name__)

# Ruta del archivo de datos
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'datos.json')


def load_data():
    """Cargar datos desde JSON"""
    if not os.path.exists(DATA_FILE):
        return {'pacientes': [], 'doctores': [], 'citas': []}
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    """Guardar datos en JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ===== RUTAS DE VISTAS =====

@sistema_bp.route('/')
def index():
    """Dashboard principal"""
    return render_template('index.html')


@sistema_bp.route('/registrar_paciente')
def registrar_paciente():
    """Vista de registro de paciente"""
    return render_template('registrar_paciente.html')


@sistema_bp.route('/registrar_doctor')
def registrar_doctor():
    """Vista de registro de doctor"""
    return render_template('registrar_doctor.html')


@sistema_bp.route('/buscar_paciente')
def buscar_paciente():
    """Vista de búsqueda de paciente"""
    return render_template('buscar_paciente.html')


@sistema_bp.route('/actualizar_paciente')
def actualizar_paciente():
    """Vista de actualización de paciente"""
    return render_template('actualizar_paciente.html')


@sistema_bp.route('/historial')
def historial():
    """Vista de historial clínico"""
    return render_template('historial.html')


@sistema_bp.route('/citas')
def citas():
    """Vista de citas"""
    return render_template('citas.html')


# ===== API ENDPOINTS =====

@sistema_bp.route('/api/pacientes', methods=['GET'])
def get_pacientes():
    """Obtener todos los pacientes"""
    data = load_data()
    return jsonify(data['pacientes'])


@sistema_bp.route('/api/pacientes/<cedula>', methods=['GET'])
def get_paciente(cedula):
    """Obtener paciente por cédula"""
    data = load_data()
    for p in data['pacientes']:
        if p['cedula'] == cedula:
            return jsonify(p)
    return jsonify({'error': 'Paciente no encontrado'}), 404


@sistema_bp.route('/api/pacientes', methods=['POST'])
def create_paciente():
    """Crear nuevo paciente"""
    data = load_data()
    nuevo_paciente = request.json
    
    # Verificar si ya existe
    for p in data['pacientes']:
        if p['cedula'] == nuevo_paciente['cedula']:
            return jsonify({'error': 'Paciente ya existe'}), 400
    
    data['pacientes'].append(nuevo_paciente)
    save_data(data)
    return jsonify(nuevo_paciente), 201


@sistema_bp.route('/api/pacientes/<cedula>', methods=['PUT'])
def update_paciente(cedula):
    """Actualizar paciente"""
    data = load_data()
    paciente_actualizado = request.json
    
    for i, p in enumerate(data['pacientes']):
        if p['cedula'] == cedula:
            data['pacientes'][i] = paciente_actualizado
            save_data(data)
            return jsonify(paciente_actualizado)
    
    return jsonify({'error': 'Paciente no encontrado'}), 404


@sistema_bp.route('/api/pacientes/<cedula>', methods=['DELETE'])
def delete_paciente(cedula):
    """Eliminar paciente"""
    data = load_data()
    data['pacientes'] = [p for p in data['pacientes'] if p['cedula'] != cedula]
    save_data(data)
    return jsonify({'message': 'Paciente eliminado'})


@sistema_bp.route('/api/doctores', methods=['GET'])
def get_doctores():
    """Obtener todos los doctores"""
    data = load_data()
    return jsonify(data['doctores'])


@sistema_bp.route('/api/doctores', methods=['POST'])
def create_doctor():
    """Crear nuevo doctor"""
    data = load_data()
    nuevo_doctor = request.json
    
    for d in data['doctores']:
        if d['id_doctor'] == nuevo_doctor['id_doctor']:
            return jsonify({'error': 'Doctor ya existe'}), 400
    
    data['doctores'].append(nuevo_doctor)
    save_data(data)
    return jsonify(nuevo_doctor), 201


@sistema_bp.route('/api/citas', methods=['GET'])
def get_citas():
    """Obtener todas las citas"""
    data = load_data()
    return jsonify(data['citas'])


@sistema_bp.route('/api/citas', methods=['POST'])
def create_cita():
    """Crear nueva cita"""
    data = load_data()
    nueva_cita = request.json
    
    # Generar ID automático
    if data['citas']:
        max_id = max([c['id'] for c in data['citas']])
        nueva_cita['id'] = max_id + 1
    else:
        nueva_cita['id'] = 1
    
    data['citas'].append(nueva_cita)
    save_data(data)
    return jsonify(nueva_cita), 201