/**
 * SICAMED - Sistema de Gestión del Adulto Mayor
 * JavaScript con validaciones y carga de datos
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🩺 SICAMED - Sistema iniciado');

    // ============================================================
    // 1. DETECTAR PÁGINA ACTIVA
    // ============================================================
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentPath.includes(href) && href !== '#') {
            link.classList.add('active');
        }
    });

    // ============================================================
    // 2. CARGAR PACIENTES Y DOCTORES EN SELECTS DE CITAS
    // ============================================================
    async function cargarPacientesYDoctores() {
        try {
            // Cargar pacientes
            const respPacientes = await fetch('/api/pacientes');
            const pacientes = await respPacientes.json();
            
            const selectPaciente = document.querySelector('#pacienteCita');
            if (selectPaciente) {
                selectPaciente.innerHTML = '<option value="">Seleccionar paciente...</option>';
                pacientes.forEach(p => {
                    const option = document.createElement('option');
                    option.value = p.cedula;
                    option.textContent = `${p.nombres} ${p.apellidos} - ${p.cedula}`;
                    selectPaciente.appendChild(option);
                });
            }
            
            // Cargar doctores
            const respDoctores = await fetch('/api/doctores');
            const doctores = await respDoctores.json();
            
            const selectDoctor = document.querySelector('#doctorCita');
            if (selectDoctor) {
                selectDoctor.innerHTML = '<option value="">Seleccionar doctor...</option>';
                doctores.forEach(d => {
                    const option = document.createElement('option');
                    option.value = d.id_doctor;
                    option.textContent = `Dr. ${d.nombres} ${d.apellidos} - ${d.especialidad}`;
                    selectDoctor.appendChild(option);
                });
            }
            
            // Cargar doctores en filtro de historial
            const filtroDoctor = document.querySelector('#filtroDoctor');
            if (filtroDoctor) {
                filtroDoctor.innerHTML = '<option value="">Todos los médicos</option>';
                doctores.forEach(d => {
                    const option = document.createElement('option');
                    option.value = d.id_doctor;
                    option.textContent = `Dr. ${d.nombres} ${d.apellidos}`;
                    filtroDoctor.appendChild(option);
                });
            }
            
        } catch (error) {
            console.error('Error cargando datos:', error);
        }
    }
    
    cargarPacientesYDoctores();

    // ============================================================
    // 3. REGISTRAR PACIENTE
    // ============================================================
    const formPaciente = document.querySelector('#formRegistroPaciente');
    if (formPaciente) {
        formPaciente.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            let isValid = true;
            let firstInvalid = null;
            
            const requiredFields = this.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                const value = field.value.trim();
                if (!value) {
                    field.classList.add('is-invalid');
                    field.classList.remove('is-valid');
                    isValid = false;
                    if (!firstInvalid) firstInvalid = field;
                } else {
                    field.classList.remove('is-invalid');
                    field.classList.add('is-valid');
                }
            });
            
            const edadInput = document.querySelector('#edad');
            if (edadInput && edadInput.value) {
                const edad = parseInt(edadInput.value);
                if (edad < 60 || edad > 120) {
                    edadInput.classList.add('is-invalid');
                    edadInput.classList.remove('is-valid');
                    isValid = false;
                    if (!firstInvalid) firstInvalid = edadInput;
                }
            }
            
            const cedulaInput = document.querySelector('#cedula');
            if (cedulaInput && cedulaInput.value) {
                const cedula = cedulaInput.value.trim();
                if (!/^\d{8}$/.test(cedula)) {
                    cedulaInput.classList.add('is-invalid');
                    cedulaInput.classList.remove('is-valid');
                    isValid = false;
                    if (!firstInvalid) firstInvalid = cedulaInput;
                }
            }
            
            if (!isValid) {
                mostrarAlerta('Por favor, complete todos los campos correctamente.', 'danger');
                if (firstInvalid) firstInvalid.focus();
                return;
            }
            
            const paciente = {
                nombres: document.querySelector('#nombres').value.trim(),
                apellidos: document.querySelector('#apellidos').value.trim(),
                edad: parseInt(document.querySelector('#edad').value),
                cedula: document.querySelector('#cedula').value.trim(),
                direccion: document.querySelector('#direccion').value.trim(),
                telefono: document.querySelector('#telefono').value.trim() || '',
                email: document.querySelector('#email').value.trim() || '',
                alergias: [],
                historial: []
            };
            
            try {
                const response = await fetch('/api/pacientes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(paciente)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    mostrarAlerta('✅ Paciente registrado correctamente.', 'success');
                    formPaciente.reset();
                    formPaciente.querySelectorAll('.is-valid').forEach(el => el.classList.remove('is-valid'));
                    cargarPacientesYDoctores(); // Recargar selects
                } else {
                    mostrarAlerta('❌ ' + (result.error || 'Error al guardar'), 'danger');
                }
            } catch (error) {
                mostrarAlerta('❌ Error de conexión con el servidor', 'danger');
            }
        });
    }

    // ============================================================
    // 4. REGISTRAR DOCTOR
    // ============================================================
    const formDoctor = document.querySelector('#formRegistroDoctor');
    if (formDoctor) {
        formDoctor.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            let isValid = true;
            let firstInvalid = null;
            
            const requiredFields = this.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                const value = field.value.trim();
                if (!value) {
                    field.classList.add('is-invalid');
                    field.classList.remove('is-valid');
                    isValid = false;
                    if (!firstInvalid) firstInvalid = field;
                } else {
                    field.classList.remove('is-invalid');
                    field.classList.add('is-valid');
                }
            });
            
            const edadInput = document.querySelector('#edadDoctor');
            if (edadInput && edadInput.value) {
                const edad = parseInt(edadInput.value);
                if (edad < 25 || edad > 80) {
                    edadInput.classList.add('is-invalid');
                    edadInput.classList.remove('is-valid');
                    isValid = false;
                    if (!firstInvalid) firstInvalid = edadInput;
                }
            }
            
            if (!isValid) {
                mostrarAlerta('Por favor, complete todos los campos correctamente.', 'danger');
                if (firstInvalid) firstInvalid.focus();
                return;
            }
            
            const doctor = {
                nombres: document.querySelector('#nombreDoctor').value.trim(),
                apellidos: document.querySelector('#apellidoDoctor').value.trim(),
                edad: parseInt(document.querySelector('#edadDoctor').value),
                cedula: document.querySelector('#cedulaDoctor').value.trim(),
                id_doctor: document.querySelector('#idDoctor').value.trim(),
                especialidad: document.querySelector('#especialidad').value,
                telefono: document.querySelector('#telefonoDoctor').value.trim() || '',
                email: document.querySelector('#emailDoctor').value.trim() || '',
                citas: []
            };
            
            try {
                const response = await fetch('/api/doctores', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(doctor)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    mostrarAlerta('✅ Doctor registrado correctamente.', 'success');
                    formDoctor.reset();
                    formDoctor.querySelectorAll('.is-valid').forEach(el => el.classList.remove('is-valid'));
                    cargarPacientesYDoctores(); // Recargar selects
                } else {
                    mostrarAlerta('❌ ' + (result.error || 'Error al guardar'), 'danger');
                }
            } catch (error) {
                mostrarAlerta('❌ Error de conexión con el servidor', 'danger');
            }
        });
    }

    // ============================================================
    // 5. BUSCAR PACIENTE - MOSTRAR DATOS
    // ============================================================
    const formBuscar = document.querySelector('#formBuscarPaciente');
    if (formBuscar) {
        formBuscar.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const cedulaInput = document.querySelector('#cedulaBuscar');
            if (!cedulaInput || !cedulaInput.value.trim()) {
                cedulaInput.classList.add('is-invalid');
                mostrarAlerta('Ingrese una cédula para buscar.', 'warning');
                return;
            }
            
            const cedula = cedulaInput.value.trim();
            if (!/^\d{8}$/.test(cedula)) {
                cedulaInput.classList.add('is-invalid');
                mostrarAlerta('La cédula debe tener 8 dígitos.', 'warning');
                return;
            }
            
            cedulaInput.classList.remove('is-invalid');
            
            try {
                const response = await fetch(`/api/pacientes/${cedula}`);
                const paciente = await response.json();
                
                if (response.ok) {
                    // Mostrar datos en la tarjeta
                    document.querySelector('#nombreMostrado').textContent = `${paciente.nombres} ${paciente.apellidos}`;
                    document.querySelector('#cedulaMostrada').textContent = paciente.cedula;
                    document.querySelector('#edadMostrada').textContent = `${paciente.edad} años`;
                    document.querySelector('#telefonoMostrado').textContent = paciente.telefono || 'No registrado';
                    document.querySelector('#direccionMostrada').textContent = paciente.direccion || 'No registrada';
                    document.querySelector('#emailMostrado').textContent = paciente.email || 'No registrado';
                    
                    mostrarAlerta('✅ Paciente encontrado.', 'success');
                } else {
                    // Limpiar datos
                    document.querySelector('#nombreMostrado').textContent = '---';
                    document.querySelector('#cedulaMostrada').textContent = '---';
                    document.querySelector('#edadMostrada').textContent = '---';
                    document.querySelector('#telefonoMostrado').textContent = '---';
                    document.querySelector('#direccionMostrada').textContent = '---';
                    document.querySelector('#emailMostrado').textContent = '---';
                    mostrarAlerta('❌ Paciente no encontrado.', 'danger');
                }
            } catch (error) {
                mostrarAlerta('❌ Error de conexión con el servidor', 'danger');
            }
        });
    }

    // ============================================================
    // 6. ACTUALIZAR PACIENTE - CARGAR Y GUARDAR DATOS
    // ============================================================
    const formBuscarActualizar = document.querySelector('#formBuscarActualizar');
    if (formBuscarActualizar) {
        formBuscarActualizar.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const cedulaInput = document.querySelector('#cedulaActualizar');
            if (!cedulaInput || !cedulaInput.value.trim()) {
                cedulaInput.classList.add('is-invalid');
                mostrarAlerta('Ingrese una cédula para buscar.', 'warning');
                return;
            }
            
            const cedula = cedulaInput.value.trim();
            if (!/^\d{8}$/.test(cedula)) {
                cedulaInput.classList.add('is-invalid');
                mostrarAlerta('La cédula debe tener 8 dígitos.', 'warning');
                return;
            }
            
            cedulaInput.classList.remove('is-invalid');
            
            try {
                const response = await fetch(`/api/pacientes/${cedula}`);
                const paciente = await response.json();
                
                if (response.ok) {
                    // Cargar datos en el formulario
                    document.querySelector('#nombrePacienteEdit').textContent = `${paciente.nombres} ${paciente.apellidos}`;
                    document.querySelector('#cedulaPacienteEdit').textContent = paciente.cedula;
                    document.querySelector('#nombresEdit').value = paciente.nombres;
                    document.querySelector('#apellidosEdit').value = paciente.apellidos;
                    document.querySelector('#edadEdit').value = paciente.edad;
                    document.querySelector('#cedulaEdit').value = paciente.cedula;
                    document.querySelector('#direccionEdit').value = paciente.direccion || '';
                    document.querySelector('#telefonoEdit').value = paciente.telefono || '';
                    document.querySelector('#emailEdit').value = paciente.email || '';
                    
                    mostrarAlerta('✅ Paciente cargado para actualizar.', 'success');
                } else {
                    mostrarAlerta('❌ Paciente no encontrado.', 'danger');
                }
            } catch (error) {
                mostrarAlerta('❌ Error de conexión con el servidor', 'danger');
            }
        });
    }

    // ============================================================
    // 7. ACTUALIZAR PACIENTE - GUARDAR CAMBIOS
    // ============================================================
    const formActualizar = document.querySelector('#formActualizarPaciente');
    if (formActualizar) {
        formActualizar.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const cedula = document.querySelector('#cedulaEdit').value;
            if (!cedula) {
                mostrarAlerta('Primero busque un paciente.', 'warning');
                return;
            }
            
            const paciente = {
                nombres: document.querySelector('#nombresEdit').value.trim(),
                apellidos: document.querySelector('#apellidosEdit').value.trim(),
                edad: parseInt(document.querySelector('#edadEdit').value),
                cedula: cedula,
                direccion: document.querySelector('#direccionEdit').value.trim(),
                telefono: document.querySelector('#telefonoEdit').value.trim(),
                email: document.querySelector('#emailEdit').value.trim(),
                alergias: [],
                historial: []
            };
            
            try {
                const response = await fetch(`/api/pacientes/${cedula}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(paciente)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    mostrarAlerta('✅ Paciente actualizado correctamente.', 'success');
                } else {
                    mostrarAlerta('❌ ' + (result.error || 'Error al actualizar'), 'danger');
                }
            } catch (error) {
                mostrarAlerta('❌ Error de conexión con el servidor', 'danger');
            }
        });
    }

    // ============================================================
    // 8. AGENDAR CITA
    // ============================================================
    const formCita = document.querySelector('#formAgendarCita');
    if (formCita) {
        formCita.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            let isValid = true;
            let firstInvalid = null;
            
            const requiredFields = this.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                const value = field.value.trim();
                if (!value) {
                    field.classList.add('is-invalid');
                    field.classList.remove('is-valid');
                    isValid = false;
                    if (!firstInvalid) firstInvalid = field;
                } else {
                    field.classList.remove('is-invalid');
                    field.classList.add('is-valid');
                }
            });
            
            if (!isValid) {
                mostrarAlerta('Por favor, seleccione paciente, doctor, fecha y hora.', 'danger');
                if (firstInvalid) firstInvalid.focus();
                return;
            }
            
            const cita = {
                cedula_paciente: document.querySelector('#pacienteCita').value,
                id_doctor: document.querySelector('#doctorCita').value,
                fecha: document.querySelector('#fechaCita').value,
                hora: document.querySelector('#horaCita').value,
                duracion: parseInt(document.querySelector('#duracionCita').value),
                estado: 'pendiente',
                observaciones: document.querySelector('#observacionesCita').value.trim() || ''
            };
            
            try {
                const response = await fetch('/api/citas', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(cita)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    mostrarAlerta('✅ Cita agendada correctamente.', 'success');
                    formCita.reset();
                    formCita.querySelectorAll('.is-valid').forEach(el => el.classList.remove('is-valid'));
                } else {
                    mostrarAlerta('❌ ' + (result.error || 'Error al guardar'), 'danger');
                }
            } catch (error) {
                mostrarAlerta('❌ Error de conexión con el servidor', 'danger');
            }
        });
    }

    // ============================================================
    // 9. CARGAR HISTORIAL
    // ============================================================
    async function cargarHistorial() {
        try {
            const response = await fetch('/api/citas');
            const citas = await response.json();
            
            const tbody = document.querySelector('#tablaHistorial');
            if (!tbody) return;
            
            if (citas.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center text-muted py-4">
                            <i class="bi bi-inbox fs-3 d-block mb-2"></i>
                            No hay citas registradas
                        </td>
                    </tr>
                `;
                return;
            }
            
            // Obtener pacientes y doctores para mostrar nombres
            const respPacientes = await fetch('/api/pacientes');
            const pacientes = await respPacientes.json();
            const respDoctores = await fetch('/api/doctores');
            const doctores = await respDoctores.json();
            
            tbody.innerHTML = '';
            citas.forEach(c => {
                const paciente = pacientes.find(p => p.cedula === c.cedula_paciente);
                const doctor = doctores.find(d => d.id_doctor === c.id_doctor);
                
                const estados = {
                    'pendiente': 'badge bg-warning',
                    'confirmada': 'badge bg-success',
                    'completada': 'badge bg-info',
                    'cancelada': 'badge bg-danger'
                };
                
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><span class="fw-semibold">${c.fecha}</span></td>
                    <td>${paciente ? `${paciente.nombres} ${paciente.apellidos}` : c.cedula_paciente}</td>
                    <td>${doctor ? `Dr. ${doctor.nombres} ${doctor.apellidos}` : c.id_doctor}</td>
                    <td>${c.observaciones || 'Sin diagnóstico'}</td>
                    <td>${c.duracion} min</td>
                    <td><span class="${estados[c.estado] || 'badge bg-secondary'} rounded-pill">${c.estado}</span></td>
                `;
                tbody.appendChild(tr);
            });
            
        } catch (error) {
            console.error('Error cargando historial:', error);
        }
    }
    
    cargarHistorial();

    // ============================================================
    // 10. LIMPIAR VALIDACIONES AL ESCRIBIR
    // ============================================================
    document.querySelectorAll('input, select, textarea').forEach(field => {
        field.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                this.classList.remove('is-invalid');
            }
        });
    });

    // ============================================================
    // 11. FUNCIÓN PARA MOSTRAR ALERTAS
    // ============================================================
    function mostrarAlerta(mensaje, tipo = 'success') {
        const alertasViejas = document.querySelectorAll('.alerta-flotante');
        alertasViejas.forEach(el => el.remove());
        
        const colores = {
            success: 'bg-success text-white',
            danger: 'bg-danger text-white',
            warning: 'bg-warning text-dark',
            info: 'bg-info text-white'
        };
        
        const iconos = {
            success: 'bi-check-circle',
            danger: 'bi-exclamation-triangle',
            warning: 'bi-exclamation-circle',
            info: 'bi-info-circle'
        };
        
        const alerta = document.createElement('div');
        alerta.className = `alerta-flotante position-fixed top-0 start-50 translate-middle-x mt-4 px-4 py-3 rounded-3 shadow-lg ${colores[tipo] || colores.success}`;
        alerta.style.zIndex = '9999';
        alerta.style.minWidth = '300px';
        alerta.style.maxWidth = '90%';
        alerta.style.transition = 'all 0.3s ease';
        alerta.innerHTML = `
            <div class="d-flex align-items-center gap-2">
                <i class="bi ${iconos[tipo] || iconos.success} fs-5"></i>
                <span class="fw-semibold">${mensaje}</span>
                <button type="button" class="btn-close btn-close-white ms-2" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(alerta);
        
        setTimeout(() => {
            alerta.style.opacity = '0';
            alerta.style.transform = 'translateY(-20px)';
            setTimeout(() => alerta.remove(), 300);
        }, 4000);
    }

    // ============================================================
    // 12. FECHA ACTUAL
    // ============================================================
    const fechaElement = document.getElementById('fechaActual');
    if (fechaElement) {
        const hoy = new Date();
        const opciones = { year: 'numeric', month: 'long', day: 'numeric' };
        fechaElement.textContent = hoy.toLocaleDateString('es-ES', opciones);
    }

    console.log('✅ SICAMED - Sistema listo.');
});

// ============================================================
// FUNCIÓN GLOBAL
// ============================================================
window.mostrarAlerta = function(mensaje, tipo) {
    const alerta = document.createElement('div');
    alerta.className = `position-fixed top-0 start-50 translate-middle-x mt-4 px-4 py-3 rounded-3 shadow-lg bg-${tipo || 'success'} text-white`;
    alerta.style.zIndex = '9999';
    alerta.style.minWidth = '300px';
    alerta.style.maxWidth = '90%';
    alerta.innerHTML = `
        <div class="d-flex align-items-center gap-2">
            <i class="bi bi-check-circle fs-5"></i>
            <span class="fw-semibold">${mensaje}</span>
            <button type="button" class="btn-close btn-close-white ms-2" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    document.body.appendChild(alerta);
    
    setTimeout(() => {
        alerta.style.opacity = '0';
        setTimeout(() => alerta.remove(), 300);
    }, 4000);
};