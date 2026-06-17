"""
SICAMED - Sistema de Gestión del Adulto Mayor
"""

from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__, 
            template_folder='view/templates',
            static_folder='view/static')

app.config['SECRET_KEY'] = 'dev-key-2026'


# ===== RUTAS DE VISTAS =====

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registrar_paciente')
def registrar_paciente():
    return render_template('registrar_paciente.html')


@app.route('/registrar_doctor')
def registrar_doctor():
    return render_template('registrar_doctor.html')


@app.route('/buscar_paciente')
def buscar_paciente():
    return render_template('buscar_paciente.html')


@app.route('/actualizar_paciente')
def actualizar_paciente():
    return render_template('actualizar_paciente.html')


@app.route('/historial')
def historial():
    return render_template('historial.html')


@app.route('/citas')
def citas():
    return render_template('citas.html')


# ===== API PARA GUARDAR Y LEER DATOS =====

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'datos.json')


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


# ===== API ENDPOINTS =====

@app.route('/api/pacientes', methods=['GET'])
def get_pacientes():
    """Obtener todos los pacientes"""
    data = load_data()
    return jsonify(data['pacientes'])


@app.route('/api/pacientes', methods=['POST'])
def create_paciente():
    """Crear nuevo paciente"""
    data = load_data()
    nuevo = request.json
    
    # Verificar si ya existe
    for p in data['pacientes']:
        if p['cedula'] == nuevo['cedula']:
            return jsonify({'error': 'Paciente ya existe'}), 400
    
    data['pacientes'].append(nuevo)
    save_data(data)
    return jsonify(nuevo), 201


@app.route('/api/pacientes/<cedula>', methods=['GET'])
def get_paciente(cedula):
    """Obtener paciente por cédula"""
    data = load_data()
    for p in data['pacientes']:
        if p['cedula'] == cedula:
            return jsonify(p)
    return jsonify({'error': 'Paciente no encontrado'}), 404


@app.route('/api/pacientes/<cedula>', methods=['PUT'])
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


@app.route('/api/pacientes/<cedula>', methods=['DELETE'])
def delete_paciente(cedula):
    """Eliminar paciente"""
    data = load_data()
    data['pacientes'] = [p for p in data['pacientes'] if p['cedula'] != cedula]
    save_data(data)
    return jsonify({'message': 'Paciente eliminado'})


@app.route('/api/doctores', methods=['GET'])
def get_doctores():
    """Obtener todos los doctores"""
    data = load_data()
    return jsonify(data['doctores'])


@app.route('/api/doctores', methods=['POST'])
def create_doctor():
    """Crear nuevo doctor"""
    data = load_data()
    nuevo = request.json
    
    # Verificar si ya existe
    for d in data['doctores']:
        if d['id_doctor'] == nuevo['id_doctor']:
            return jsonify({'error': 'Doctor ya existe'}), 400
    
    data['doctores'].append(nuevo)
    save_data(data)
    return jsonify(nuevo), 201


@app.route('/api/citas', methods=['GET'])
def get_citas():
    """Obtener todas las citas"""
    data = load_data()
    return jsonify(data['citas'])


@app.route('/api/citas', methods=['POST'])
def create_cita():
    """Crear nueva cita"""
    data = load_data()
    nueva = request.json
    
    # Generar ID automático
    if data['citas']:
        max_id = max([c['id'] for c in data['citas']])
        nueva['id'] = max_id + 1
    else:
        nueva['id'] = 1
    
    data['citas'].append(nueva)
    save_data(data)
    return jsonify(nueva), 201


@app.route('/api/citas/<int:id>', methods=['DELETE'])
def delete_cita(id):
    """Eliminar cita"""
    data = load_data()
    data['citas'] = [c for c in data['citas'] if c['id'] != id]
    save_data(data)
    return jsonify({'message': 'Cita eliminada'})


if __name__ == '__main__':
    print("🚀 Servidor iniciado en http://localhost:5000")
    print("📁 Archivo de datos: data/datos.json")
    app.run(debug=True, host='0.0.0.0', port=5000)