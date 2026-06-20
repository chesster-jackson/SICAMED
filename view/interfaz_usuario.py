"""
Interfaz de Usuario con Tkinter - Mejorada con Teoría del Color
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re


class VentanaPrincipal:
    """Ventana principal del sistema"""
    
    def __init__(self, controlador):
        self.controlador = controlador
        
        # Configuración de colores basada en teoría del color
        self.colores = {
            'fondo_principal': '#F0F7F4',
            'fondo_secundario': '#E8F1ED',
            'fondo_card': '#FFFFFF',
            'fondo_header': '#1A3B2E',
            'texto_principal': '#1A3B2E',
            'texto_secundario': '#5A6F66',
            'texto_blanco': '#FFFFFF',
            'boton_primary': '#2E7D32',
            'boton_primary_hover': '#1B5E20',
            'boton_secondary': '#1565C0',
            'boton_secondary_hover': '#0D47A1',
            'boton_warning': '#E65100',
            'boton_warning_hover': '#BF360C',
            'boton_danger': '#C62828',
            'boton_danger_hover': '#B71C1C',
            'boton_info': '#00838F',
            'boton_info_hover': '#006064',
            'boton_purple': '#6A1B9A',
            'boton_purple_hover': '#4A148C',
            'boton_gray': '#546E7A',
            'boton_gray_hover': '#37474F',
            'tabla_header': '#1A3B2E',
            'tabla_header_texto': '#FFFFFF',
            'tabla_fila_par': '#FFFFFF',
            'tabla_fila_impar': '#F5F8F6',
            'tabla_seleccion': '#4CAF50',
            'tabla_borde': '#C8D6D0',
            'stats_pacientes': '#E8F5E9',
            'stats_doctores': '#E3F2FD',
            'stats_citas': '#FFF8E1',
            'error': '#C62828',
            'exito': '#2E7D32',
            'aviso': '#E65100'
        }
        
        self.root = tk.Tk()
        self.root.title("SICAMED - Gestión del Adulto Mayor")
        self.root.geometry("1000x900")
        self.root.configure(bg=self.colores['fondo_principal'])
        
        self.frame_principal = tk.Frame(self.root, bg=self.colores['fondo_principal'])
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.mostrar_dashboard()
    
    def limpiar_frame(self):
        """Limpiar el frame principal"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
    
    def _filtrar_none(self, lista):
        """Filtra elementos None de una lista"""
        return [item for item in lista if item is not None]
    
    def _validar_email(self, email):
        """
        Valida el formato del correo electrónico
        Retorna True si es válido, False si no
        """
        if not email:  # Campo opcional, vacío es válido
            return True
        
        # Patrón completo para email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(patron, email):
            return True
        return False
    
    def _validar_telefono(self, telefono):
        """
        Valida que el teléfono solo tenga números
        Retorna True si es válido, False si no
        """
        if not telefono:  # Campo opcional
            return True
        
        if not telefono.isdigit():
            return False
        return True
    
    def mostrar_dashboard(self):
        """Mostrar dashboard principal"""
        self.limpiar_frame()
        
        # Título principal
        titulo = tk.Label(
            self.frame_principal, 
            text="SISTEMA DE GESTIÓN DEL ADULTO MAYOR - MINSA",
            font=('Segoe UI', 20, 'bold'), 
            bg=self.colores['fondo_principal'], 
            fg=self.colores['texto_principal']
        )
        titulo.pack(pady=15)
        
        # Subtítulo
        subtitulo = tk.Label(
            self.frame_principal, 
            text="Centro de Salud · Atención Integral al Adulto Mayor",
            font=('Segoe UI', 12), 
            bg=self.colores['fondo_principal'], 
            fg=self.colores['texto_secundario']
        )
        subtitulo.pack(pady=5)
        
        # Línea separadora
        tk.Frame(self.frame_principal, height=2, bg=self.colores['tabla_borde']).pack(fill=tk.X, pady=10)
        
        # Tarjetas de estadísticas
        stats_frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        stats_frame.pack(pady=15)
        
        pacientes = self.controlador.contar_pacientes()
        doctores = self.controlador.contar_doctores()
        citas = self.controlador.contar_citas()
        
        stats = [
            (f" Pacientes: {pacientes}", self.colores['stats_pacientes']),
            (f" Doctores: {doctores}", self.colores['stats_doctores']),
            (f"Citas: {citas}", self.colores['stats_citas'])
        ]
        
        for i, (texto, color) in enumerate(stats):
            card = tk.Frame(
                stats_frame, 
                bg=color, 
                padx=30, 
                pady=15, 
                relief=tk.RAISED, 
                bd=1
            )
            card.grid(row=0, column=i, padx=15)
            
            tk.Label(
                card, 
                text=texto, 
                font=('Segoe UI', 14, 'bold'), 
                bg=color,
                fg=self.colores['texto_principal']
            ).pack()
        
        # Título de acceso rápido
        tk.Label(
            self.frame_principal, 
            text="--- ACCESO RÁPIDO ---",
            font=('Segoe UI', 13, 'bold'), 
            bg=self.colores['fondo_principal'], 
            fg=self.colores['texto_secundario']
        ).pack(pady=15)
        
        # Botones
        botones_frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        botones_frame.pack(pady=10)
        
        botones = [
            ("Registrar Paciente", self.mostrar_registrar_paciente, self.colores['boton_primary']),
            ("Registrar Doctor", self.mostrar_registrar_doctor, self.colores['boton_secondary']),
            ("Buscar Paciente", self.mostrar_buscar_paciente, self.colores['boton_warning']),
            ("Buscar Doctor", self.mostrar_buscar_doctor, self.colores['boton_warning']),
            ("Actualizar Paciente", self.mostrar_actualizar_paciente, self.colores['boton_gray']),
            ("Actualizar Doctor", self.mostrar_actualizar_doctor, self.colores['boton_gray']),
            ("Eliminar Paciente", self.mostrar_eliminar_paciente, self.colores['boton_danger']),
            ("Eliminar Doctor", self.mostrar_eliminar_doctor, self.colores['boton_danger']),
            ("Agendar Cita", self.mostrar_agendar_cita, self.colores['boton_purple']),
            ("Listar Pacientes", self.mostrar_listar_pacientes, self.colores['boton_info']),
            ("Listar Doctores", self.mostrar_listar_doctores, self.colores['boton_secondary']),
            ("Ver Citas", self.mostrar_listar_citas, self.colores['boton_info'])
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(
                botones_frame, 
                text=texto, 
                command=comando,
                bg=color, 
                fg=self.colores['texto_blanco'], 
                font=('Segoe UI', 10, 'bold'),
                padx=12, 
                pady=10, 
                width=20, 
                cursor='hand2',
                relief=tk.FLAT,
                bd=0
            )
            
            # Efecto hover
            hover_color = self._obtener_hover_color(color)
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
            
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=6, pady=6, sticky='ew')
        
        # Configurar columnas
        for j in range(3):
            botones_frame.grid_columnconfigure(j, weight=1)
    
    def _obtener_hover_color(self, color):
        """Obtener versión más oscura del color para hover"""
        colores_hover = {
            self.colores['boton_primary']: self.colores['boton_primary_hover'],
            self.colores['boton_secondary']: self.colores['boton_secondary_hover'],
            self.colores['boton_warning']: self.colores['boton_warning_hover'],
            self.colores['boton_danger']: self.colores['boton_danger_hover'],
            self.colores['boton_info']: self.colores['boton_info_hover'],
            self.colores['boton_purple']: self.colores['boton_purple_hover'],
            self.colores['boton_gray']: self.colores['boton_gray_hover']
        }
        return colores_hover.get(color, color)
    
    # ============ LISTAR PACIENTES ============
    
    def mostrar_listar_pacientes(self):
        """Listar todos los pacientes con formato tipo Excel y teoría del color"""
        self.limpiar_frame()
        
        # Título
        tk.Label(
            self.frame_principal,
            text="LISTA DE PACIENTES",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        # Obtener pacientes y filtrar None
        pacientes = self._filtrar_none(self.controlador.obtener_pacientes())
        total = len(pacientes)
        
        # Contador
        tk.Label(
            self.frame_principal,
            text=f"Total: {total} pacientes registrados",
            font=('Segoe UI', 11),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_secundario']
        ).pack(pady=5)
        
        # Frame para la tabla
        frame_tabla = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Configurar estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview.Heading",
            background=self.colores['tabla_header'],
            foreground=self.colores['tabla_header_texto'],
            font=('Segoe UI', 11, 'bold'),
            padding=8
        )
        style.configure(
            "Custom.Treeview",
            background=self.colores['tabla_fila_par'],
            foreground=self.colores['texto_principal'],
            rowheight=30,
            font=('Segoe UI', 10),
            fieldbackground=self.colores['tabla_fila_par']
        )
        style.map(
            "Custom.Treeview",
            background=[('selected', self.colores['tabla_seleccion'])],
            foreground=[('selected', 'white')]
        )
        
        # Crear tabla
        columnas = ('Cédula', 'Nombres', 'Apellidos', 'Edad', 'Teléfono')
        tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show='headings',
            height=15,
            style="Custom.Treeview"
        )
        
        # Configurar columnas
        tree.heading('Cédula', text='CÉDULA')
        tree.column('Cédula', width=150, anchor='center')
        tree.heading('Nombres', text='NOMBRES')
        tree.column('Nombres', width=180, anchor='w')
        tree.heading('Apellidos', text='APELLIDOS')
        tree.column('Apellidos', width=180, anchor='w')
        tree.heading('Edad', text='EDAD')
        tree.column('Edad', width=80, anchor='center')
        tree.heading('Teléfono', text='TELÉFONO')
        tree.column('Teléfono', width=150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insertar datos
        if not pacientes:
            tree.insert('', tk.END, values=("", "No hay pacientes registrados", "", "", ""))
            tree.tag_configure('empty', background='#FFF9C4', font=('Segoe UI', 11, 'bold'))
            tree.item(tree.get_children()[0], tags=('empty',))
        else:
            for idx, paciente in enumerate(pacientes):
                tag = 'even' if idx % 2 == 0 else 'odd'
                tree.insert(
                    '',
                    tk.END,
                    values=(
                        paciente.cedula,
                        paciente.nombres,
                        paciente.apellidos,
                        paciente.edad,
                        paciente.telefono or '-'
                    ),
                    tags=(tag,)
                )
            tree.tag_configure('even', background=self.colores['tabla_fila_par'])
            tree.tag_configure('odd', background=self.colores['tabla_fila_impar'])
        
        # Botón Volver al Inicio (siempre visible)
        frame_botones = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_botones.pack(pady=15, fill=tk.X)
        btn_volver = tk.Button(
            frame_botones,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=25,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT,
            width=20
        )
        btn_volver.pack(pady=5)
        btn_volver.bind("<Enter>", lambda e: btn_volver.config(bg=self.colores['boton_gray_hover']))
        btn_volver.bind("<Leave>", lambda e: btn_volver.config(bg=self.colores['boton_gray']))
    
    # ============ LISTAR DOCTORES ============
    
    def mostrar_listar_doctores(self):
        """Listar todos los doctores"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text=" LISTA DE DOCTORES",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        doctores = self._filtrar_none(self.controlador.obtener_doctores())
        total = len(doctores)
        
        tk.Label(
            self.frame_principal,
            text=f"Total: {total} doctores registrados",
            font=('Segoe UI', 11),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_secundario']
        ).pack(pady=5)
        
        frame_tabla = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Doctor.Treeview.Heading",
            background=self.colores['tabla_header'],
            foreground=self.colores['tabla_header_texto'],
            font=('Segoe UI', 11, 'bold'),
            padding=8
        )
        style.configure(
            "Doctor.Treeview",
            background=self.colores['tabla_fila_par'],
            foreground=self.colores['texto_principal'],
            rowheight=30,
            font=('Segoe UI', 10)
        )
        
        columnas = ('ID', 'Nombres', 'Apellidos', 'Especialidad', 'Teléfono')
        tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show='headings',
            height=15,
            style="Doctor.Treeview"
        )
        tree.heading('ID', text='ID')
        tree.column('ID', width=100, anchor='center')
        tree.heading('Nombres', text='NOMBRES')
        tree.column('Nombres', width=180, anchor='w')
        tree.heading('Apellidos', text='APELLIDOS')
        tree.column('Apellidos', width=180, anchor='w')
        tree.heading('Especialidad', text='ESPECIALIDAD')
        tree.column('Especialidad', width=150, anchor='w')
        tree.heading('Teléfono', text='TELÉFONO')
        tree.column('Teléfono', width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if not doctores:
            tree.insert('', tk.END, values=("", " No hay doctores registrados", "", "", ""))
            tree.tag_configure('empty', background='#FFF9C4', font=('Segoe UI', 11, 'bold'))
            tree.item(tree.get_children()[0], tags=('empty',))
        else:
            for idx, d in enumerate(doctores):
                tag = 'even' if idx % 2 == 0 else 'odd'
                tree.insert(
                    '',
                    tk.END,
                    values=(d.id_doctor, d.nombres, d.apellidos, d.especialidad, d.telefono or '-'),
                    tags=(tag,)
                )
            tree.tag_configure('even', background=self.colores['tabla_fila_par'])
            tree.tag_configure('odd', background=self.colores['tabla_fila_impar'])
        
        # Botón Volver
        frame_botones = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_botones.pack(pady=15, fill=tk.X)
        btn_volver = tk.Button(
            frame_botones,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=25,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT,
            width=20
        )
        btn_volver.pack(pady=5)
        btn_volver.bind("<Enter>", lambda e: btn_volver.config(bg=self.colores['boton_gray_hover']))
        btn_volver.bind("<Leave>", lambda e: btn_volver.config(bg=self.colores['boton_gray']))
    
    # ============ LISTAR CITAS ============
    
    def mostrar_listar_citas(self):
        """Listar todas las citas"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text="LISTA DE CITAS",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        citas = self._filtrar_none(self.controlador.obtener_citas())
        pacientes = self._filtrar_none(self.controlador.obtener_pacientes())
        doctores = self._filtrar_none(self.controlador.obtener_doctores())
        total = len(citas)
        
        tk.Label(
            self.frame_principal,
            text=f"Total: {total} citas registradas",
            font=('Segoe UI', 11),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_secundario']
        ).pack(pady=5)
        
        frame_tabla = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Cita.Treeview.Heading",
            background=self.colores['tabla_header'],
            foreground=self.colores['tabla_header_texto'],
            font=('Segoe UI', 11, 'bold'),
            padding=8
        )
        style.configure(
            "Cita.Treeview",
            background=self.colores['tabla_fila_par'],
            foreground=self.colores['texto_principal'],
            rowheight=30,
            font=('Segoe UI', 10)
        )
        
        columnas = ('ID', 'Paciente', 'Doctor', 'Fecha', 'Hora', 'Estado')
        tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show='headings',
            height=15,
            style="Cita.Treeview"
        )
        tree.heading('ID', text='ID')
        tree.column('ID', width=80, anchor='center')
        tree.heading('Paciente', text='PACIENTE')
        tree.column('Paciente', width=200, anchor='w')
        tree.heading('Doctor', text='DOCTOR')
        tree.column('Doctor', width=200, anchor='w')
        tree.heading('Fecha', text='FECHA')
        tree.column('Fecha', width=120, anchor='center')
        tree.heading('Hora', text='HORA')
        tree.column('Hora', width=100, anchor='center')
        tree.heading('Estado', text='ESTADO')
        tree.column('Estado', width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if not citas:
            tree.insert('', tk.END, values=("", "No hay citas registradas", "", "", "", ""))
            tree.tag_configure('empty', background='#FFF9C4', font=('Segoe UI', 11, 'bold'))
            tree.item(tree.get_children()[0], tags=('empty',))
        else:
            for idx, c in enumerate(citas):
                paciente = next((p for p in pacientes if p.cedula == c.cedula_paciente), None)
                doctor = next((d for d in doctores if d.id_doctor == c.id_doctor), None)
                nombre_paciente = f"{paciente.nombres} {paciente.apellidos}" if paciente else c.cedula_paciente
                nombre_doctor = f"{doctor.nombres} {doctor.apellidos}" if doctor else c.id_doctor
                tag = 'even' if idx % 2 == 0 else 'odd'
                tree.insert(
                    '',
                    tk.END,
                    values=(c.id, nombre_paciente, nombre_doctor, c.fecha, c.hora, c.estado),
                    tags=(tag,)
                )
            tree.tag_configure('even', background=self.colores['tabla_fila_par'])
            tree.tag_configure('odd', background=self.colores['tabla_fila_impar'])
        
        # Botón Volver
        frame_botones = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_botones.pack(pady=15, fill=tk.X)
        btn_volver = tk.Button(
            frame_botones,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=25,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT,
            width=20
        )
        btn_volver.pack(pady=5)
        btn_volver.bind("<Enter>", lambda e: btn_volver.config(bg=self.colores['boton_gray_hover']))
        btn_volver.bind("<Leave>", lambda e: btn_volver.config(bg=self.colores['boton_gray']))
    
    # ============ REGISTRAR PACIENTE (CON VALIDACIÓN DE EMAIL) ============
    
    def mostrar_registrar_paciente(self):
        """Formulario para registrar paciente"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text="REGISTRAR PACIENTE",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        aviso = tk.Label(
            self.frame_principal,
            text="ATENCIÓN: Edad ≥ 60 años | Cédula: 123-123456-1234A | Nombres: solo letras",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colores['error'],
            bg=self.colores['fondo_principal']
        )
        aviso.pack(pady=5)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=15)
        
        campos = [
            ("Nombres * (solo letras):", "nombres"),
            ("Apellidos * (solo letras):", "apellidos"),
            ("Edad * (60+):", "edad"),
            ("Cédula * (123-123456-1234A):", "cedula"),
            ("Teléfono:", "telefono"),
            ("Dirección:", "direccion"),
            ("Email:", "email")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(
                frame,
                text=label,
                font=('Segoe UI', 10),
                bg=self.colores['fondo_principal'],
                fg=self.colores['texto_principal']
            ).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry
        
        def guardar():
            try:
                nombres = entries['nombres'].get().strip()
                apellidos = entries['apellidos'].get().strip()
                edad = entries['edad'].get().strip()
                cedula = entries['cedula'].get().strip()
                telefono = entries['telefono'].get().strip()
                direccion = entries['direccion'].get().strip()
                email = entries['email'].get().strip()
                
                # Validar campos obligatorios
                if not nombres or not apellidos or not edad or not cedula:
                    messagebox.showerror("Error", "Nombres, apellidos, edad y cédula son obligatorios")
                    return
                
                # Validar nombres (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in nombres):
                    messagebox.showerror("Error", "Los nombres solo pueden contener letras y espacios")
                    return
                
                # Validar apellidos (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in apellidos):
                    messagebox.showerror("Error", "Los apellidos solo pueden contener letras y espacios")
                    return
                
                #  VALIDAR EMAIL (si se proporciona)
                if email and not self._validar_email(email):
                    messagebox.showerror("Error", 
                        " Email inválido\n\n"
                        "El correo debe tener:\n"
                        "• Un @ (arroba)\n"
                        "• Un punto (.) después del @\n"
                        "• Ejemplo: usuario@dominio.com"
                    )
                    return
                
                # VALIDAR TELÉFONO (solo números)
                if telefono and not self._validar_telefono(telefono):
                    messagebox.showerror("Error", "El teléfono solo debe contener números")
                    return
                
                # Intentar registrar (el controlador valida el resto)
                self.controlador.registrar_paciente(
                    nombres, apellidos, int(edad), 
                    cedula, telefono, direccion, email
                )
                messagebox.showinfo("Éxito", "Paciente registrado correctamente")
                
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_guardar = tk.Button(
            frame,
            text="Guardar Paciente",
            command=guardar,
            bg=self.colores['boton_primary'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.pack(pady=10)
    
    # ============ REGISTRAR DOCTOR (CON VALIDACIÓN DE TELÉFONO) ============
    
    def mostrar_registrar_doctor(self):
        """Formulario para registrar doctor"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text="REGISTRAR DOCTOR",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        aviso = tk.Label(
            self.frame_principal,
            text="ATENCIÓN: Nombres solo letras | Cédula: 123-123456-1234A",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colores['error'],
            bg=self.colores['fondo_principal']
        )
        aviso.pack(pady=5)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=15)
        
        campos = [
            ("Nombres * (solo letras):", "nombres"),
            ("Apellidos * (solo letras):", "apellidos"),
            ("Edad * (18-80):", "edad"),
            ("Cédula * (123-123456-1234A):", "cedula"),
            ("ID Doctor *:", "id_doctor"),
            ("Especialidad *:", "especialidad"),
            ("Teléfono:", "telefono")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(
                frame,
                text=label,
                font=('Segoe UI', 10),
                bg=self.colores['fondo_principal'],
                fg=self.colores['texto_principal']
            ).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry
        
        def guardar():
            try:
                nombres = entries['nombres'].get().strip()
                apellidos = entries['apellidos'].get().strip()
                edad = entries['edad'].get().strip()
                cedula = entries['cedula'].get().strip()
                id_doctor = entries['id_doctor'].get().strip()
                especialidad = entries['especialidad'].get().strip()
                telefono = entries['telefono'].get().strip()
                
                if not nombres or not apellidos or not edad or not cedula or not id_doctor or not especialidad:
                    messagebox.showerror("Error", " Todos los campos con * son obligatorios")
                    return
                
                # Validar nombres (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in nombres):
                    messagebox.showerror("Error", "Los nombres solo pueden contener letras y espacios")
                    return
                
                # Validar apellidos (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in apellidos):
                    messagebox.showerror("Error", " Los apellidos solo pueden contener letras y espacios")
                    return
                
                # VALIDAR TELÉFONO (solo números)
                if telefono and not self._validar_telefono(telefono):
                    messagebox.showerror("Error", " El teléfono solo debe contener números")
                    return
                
                # Intentar registrar (el controlador valida el resto)
                self.controlador.registrar_doctor(
                    nombres, apellidos, int(edad), 
                    cedula, id_doctor, especialidad, telefono
                )
                messagebox.showinfo("Éxito", "Doctor registrado correctamente")
                
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_guardar = tk.Button(
            frame,
            text="Guardar Doctor",
            command=guardar,
            bg=self.colores['boton_secondary'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.pack(pady=10)
    
    # ============ BUSCAR PACIENTE ============
    
    def mostrar_buscar_paciente(self):
        """Buscar paciente por cédula"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text="BUSCAR PACIENTE",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=15)
        
        tk.Label(
            frame,
            text="Cédula (123-123456-1234A):",
            font=('Segoe UI', 11),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).grid(row=0, column=0, padx=5, pady=5)
        
        entry_cedula = tk.Entry(frame, width=25, font=('Segoe UI', 11))
        entry_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        frame_resultados = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_resultados.pack(pady=15, fill=tk.BOTH, expand=True)
        
        def buscar():
            for widget in frame_resultados.winfo_children():
                widget.destroy()
            
            cedula = entry_cedula.get().strip()
            if not cedula:
                messagebox.showwarning("Advertencia", "Ingrese una cédula")
                return
            
            try:
                paciente = self.controlador.buscar_paciente(cedula)
                if paciente:
                    card = tk.Frame(
                        frame_resultados,
                        bg='white',
                        relief=tk.RAISED,
                        bd=2,
                        padx=20,
                        pady=20
                    )
                    card.pack(pady=10, padx=20, fill=tk.X)
                    
                    info = [
                        (" Nombres:", paciente.nombres),
                        (" Apellidos:", paciente.apellidos),
                        (" Edad:", f"{paciente.edad} años"),
                        (" Cédula:", paciente.cedula),
                        (" Teléfono:", paciente.telefono or 'No registrado'),
                        (" Dirección:", paciente.direccion or 'No registrada'),
                        ("Email:", paciente.email or 'No registrado')
                    ]
                    
                    for i, (label, value) in enumerate(info):
                        tk.Label(
                            card,
                            text=label,
                            font=('Segoe UI', 10, 'bold'),
                            bg='white',
                            fg=self.colores['texto_principal']
                        ).grid(row=i, column=0, sticky='w', pady=3)
                        
                        tk.Label(
                            card,
                            text=value,
                            font=('Segoe UI', 10),
                            bg='white',
                            fg=self.colores['texto_secundario']
                        ).grid(row=i, column=1, sticky='w', padx=10, pady=3)
                else:
                    tk.Label(
                        frame_resultados,
                        text="Paciente no encontrado",
                        font=('Segoe UI', 14, 'bold'),
                        fg=self.colores['error'],
                        bg=self.colores['fondo_principal']
                    ).pack(pady=20)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_buscar = tk.Button(
            frame,
            text="Buscar",
            command=buscar,
            bg=self.colores['boton_warning'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_buscar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.pack(pady=10)
    
    # ============ BUSCAR DOCTOR ============
    
    def mostrar_buscar_doctor(self):
        """Buscar doctor por ID"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text="BUSCAR DOCTOR",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=15)
        
        tk.Label(
            frame,
            text="ID del Doctor:",
            font=('Segoe UI', 11),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).grid(row=0, column=0, padx=5, pady=5)
        
        entry_id = tk.Entry(frame, width=25, font=('Segoe UI', 11))
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        frame_resultados = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_resultados.pack(pady=15, fill=tk.BOTH, expand=True)
        
        def buscar():
            for widget in frame_resultados.winfo_children():
                widget.destroy()
            
            id_doctor = entry_id.get().strip()
            if not id_doctor:
                messagebox.showwarning("Advertencia", "Ingrese un ID de doctor")
                return
            
            try:
                doctor = self.controlador.buscar_doctor(id_doctor)
                if doctor:
                    card = tk.Frame(
                        frame_resultados,
                        bg='white',
                        relief=tk.RAISED,
                        bd=2,
                        padx=20,
                        pady=20
                    )
                    card.pack(pady=10, padx=20, fill=tk.X)
                    
                    info = [
                        ("Nombres:", doctor.nombres),
                        ("Apellidos:", doctor.apellidos),
                        ("Edad:", f"{doctor.edad} años"),
                        ("Cédula:", doctor.cedula),
                        ("ID Doctor:", doctor.id_doctor),
                        ("Especialidad:", doctor.especialidad),
                        ("Teléfono:", doctor.telefono or 'No registrado')
                    ]
                    
                    for i, (label, value) in enumerate(info):
                        tk.Label(
                            card,
                            text=label,
                            font=('Segoe UI', 10, 'bold'),
                            bg='white',
                            fg=self.colores['texto_principal']
                        ).grid(row=i, column=0, sticky='w', pady=3)
                        
                        tk.Label(
                            card,
                            text=value,
                            font=('Segoe UI', 10),
                            bg='white',
                            fg=self.colores['texto_secundario']
                        ).grid(row=i, column=1, sticky='w', padx=10, pady=3)
                else:
                    tk.Label(
                        frame_resultados,
                        text="Doctor no encontrado",
                        font=('Segoe UI', 14, 'bold'),
                        fg=self.colores['error'],
                        bg=self.colores['fondo_principal']
                    ).pack(pady=20)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_buscar = tk.Button(
            frame,
            text="Buscar",
            command=buscar,
            bg=self.colores['boton_warning'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_buscar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.pack(pady=10)
    
    # ============ ACTUALIZAR PACIENTE ============
    
    def mostrar_actualizar_paciente(self):
        """Actualizar paciente"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text=" ACTUALIZAR PACIENTE",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=15)
        
        tk.Label(
            frame,
            text="Cédula (123-123456-1234A):",
            font=('Segoe UI', 10),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).grid(row=0, column=0, padx=5, pady=5)
        
        entry_cedula = tk.Entry(frame, width=25, font=('Segoe UI', 10))
        entry_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        def cargar():
            cedula = entry_cedula.get().strip()
            if not cedula:
                messagebox.showwarning("Advertencia", "Ingrese una cédula")
                return
            
            try:
                paciente = self.controlador.buscar_paciente(cedula)
                if paciente:
                    entries['nombres'].delete(0, tk.END)
                    entries['nombres'].insert(0, paciente.nombres)
                    entries['apellidos'].delete(0, tk.END)
                    entries['apellidos'].insert(0, paciente.apellidos)
                    entries['edad'].delete(0, tk.END)
                    entries['edad'].insert(0, str(paciente.edad))
                    entries['teléfono'].delete(0, tk.END)
                    entries['teléfono'].insert(0, paciente.telefono or '')
                    entries['dirección'].delete(0, tk.END)
                    entries['dirección'].insert(0, paciente.direccion or '')
                    entries['email'].delete(0, tk.END)
                    entries['email'].insert(0, paciente.email or '')
                    messagebox.showinfo("Éxito", "Paciente cargado para actualizar")
                else:
                    messagebox.showerror("Error", "Paciente no encontrado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_cargar = tk.Button(
            frame,
            text="Cargar Datos",
            command=cargar,
            bg=self.colores['boton_info'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_cargar.grid(row=0, column=2, padx=10, pady=5)
        
        frame_datos = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_datos.pack(pady=15)
        
        entries = {}
        campos = ["Nombres", "Apellidos", "Edad", "Teléfono", "Dirección", "Email"]
        
        for i, campo in enumerate(campos):
            tk.Label(
                frame_datos,
                text=f"{campo}:",
                font=('Segoe UI', 10),
                bg=self.colores['fondo_principal'],
                fg=self.colores['texto_principal']
            ).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            entry = tk.Entry(frame_datos, width=40, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[campo.lower()] = entry
        
        def actualizar():
            try:
                cedula = entry_cedula.get().strip()
                nombres = entries['nombres'].get().strip()
                apellidos = entries['apellidos'].get().strip()
                edad = entries['edad'].get().strip()
                telefono = entries['teléfono'].get().strip()
                direccion = entries['dirección'].get().strip()
                email = entries['email'].get().strip()
                
                if not nombres or not apellidos or not edad:
                    messagebox.showerror("Error", " Nombres, apellidos y edad son obligatorios")
                    return
                
                # Validar nombres (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in nombres):
                    messagebox.showerror("Error", "Los nombres solo pueden contener letras y espacios")
                    return
                
                # Validar apellidos (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in apellidos):
                    messagebox.showerror("Error", "Los apellidos solo pueden contener letras y espacios")
                    return
                
                # VALIDAR EMAIL (si se proporciona)
                if email and not self._validar_email(email):
                    messagebox.showerror("Error", 
                        "Email inválido\n\n"
                        "El correo debe tener:\n"
                        "• Un @ (arroba)\n"
                        "• Un punto (.) después del @\n"
                        "• Ejemplo: usuario@dominio.com"
                    )
                    return
                
                # VALIDAR TELÉFONO (solo números)
                if telefono and not self._validar_telefono(telefono):
                    messagebox.showerror("Error", "El teléfono solo debe contener números")
                    return
                
                self.controlador.actualizar_paciente(cedula, nombres, apellidos, int(edad), telefono, direccion, email)
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_actualizar = tk.Button(
            self.frame_principal,
            text="Actualizar Paciente",
            command=actualizar,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_actualizar.pack(pady=10)
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.pack(pady=5)
    
    # ============ ACTUALIZAR DOCTOR ============
    
    def mostrar_actualizar_doctor(self):
        """Actualizar doctor"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text=" ACTUALIZAR DOCTOR",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=15)
        
        tk.Label(
            frame,
            text="ID del Doctor:",
            font=('Segoe UI', 10),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).grid(row=0, column=0, padx=5, pady=5)
        
        entry_id = tk.Entry(frame, width=25, font=('Segoe UI', 10))
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        def cargar():
            id_doctor = entry_id.get().strip()
            if not id_doctor:
                messagebox.showwarning("Advertencia", "Ingrese un ID de doctor")
                return
            
            try:
                doctor = self.controlador.buscar_doctor(id_doctor)
                if doctor:
                    entries['nombres'].delete(0, tk.END)
                    entries['nombres'].insert(0, doctor.nombres)
                    entries['apellidos'].delete(0, tk.END)
                    entries['apellidos'].insert(0, doctor.apellidos)
                    entries['edad'].delete(0, tk.END)
                    entries['edad'].insert(0, str(doctor.edad))
                    entries['cédula'].delete(0, tk.END)
                    entries['cédula'].insert(0, doctor.cedula)
                    entries['especialidad'].delete(0, tk.END)
                    entries['especialidad'].insert(0, doctor.especialidad)
                    entries['teléfono'].delete(0, tk.END)
                    entries['teléfono'].insert(0, doctor.telefono or '')
                    messagebox.showinfo("Éxito", " Doctor cargado para actualizar")
                else:
                    messagebox.showerror("Error", "Doctor no encontrado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_cargar = tk.Button(
            frame,
            text="Cargar Datos",
            command=cargar,
            bg=self.colores['boton_info'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_cargar.grid(row=0, column=2, padx=10, pady=5)
        
        frame_datos = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame_datos.pack(pady=15)
        
        entries = {}
        campos = ["Nombres", "Apellidos", "Edad", "Cédula", "Especialidad", "Teléfono"]
        
        for i, campo in enumerate(campos):
            tk.Label(
                frame_datos,
                text=f"{campo}:",
                font=('Segoe UI', 10),
                bg=self.colores['fondo_principal'],
                fg=self.colores['texto_principal']
            ).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            entry = tk.Entry(frame_datos, width=40, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[campo.lower()] = entry
        
        def actualizar():
            try:
                id_doctor = entry_id.get().strip()
                nombres = entries['nombres'].get().strip()
                apellidos = entries['apellidos'].get().strip()
                edad = entries['edad'].get().strip()
                cedula = entries['cédula'].get().strip()
                especialidad = entries['especialidad'].get().strip()
                telefono = entries['teléfono'].get().strip()
                
                if not nombres or not apellidos or not edad or not cedula or not especialidad:
                    messagebox.showerror("Error", " Nombres, apellidos, edad, cédula y especialidad son obligatorios")
                    return
                
                # Validar nombres (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in nombres):
                    messagebox.showerror("Error", " Los nombres solo pueden contener letras y espacios")
                    return
                
                # Validar apellidos (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in apellidos):
                    messagebox.showerror("Error", "Los apellidos solo pueden contener letras y espacios")
                    return
                
                # VALIDAR TELÉFONO (solo números)
                if telefono and not self._validar_telefono(telefono):
                    messagebox.showerror("Error", " El teléfono solo debe contener números")
                    return
                
                self.controlador.actualizar_doctor(id_doctor, nombres, apellidos, int(edad), cedula, especialidad, telefono)
                messagebox.showinfo("Éxito", " Doctor actualizado correctamente")
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_actualizar = tk.Button(
            self.frame_principal,
            text="Actualizar Doctor",
            command=actualizar,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_actualizar.pack(pady=10)
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.pack(pady=5)
    
    # ============ ELIMINAR PACIENTE ============
    
    def mostrar_eliminar_paciente(self):
        """Eliminar paciente"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text=" ELIMINAR PACIENTE",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=30)
        
        tk.Label(
            frame,
            text="Cédula (123-123456-1234A):",
            font=('Segoe UI', 11),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).grid(row=0, column=0, padx=5, pady=5)
        
        entry_cedula = tk.Entry(frame, width=25, font=('Segoe UI', 11))
        entry_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        def eliminar():
            cedula = entry_cedula.get().strip()
            if not cedula:
                messagebox.showwarning("Advertencia", "Ingrese una cédula")
                return
            
            if not messagebox.askyesno("Confirmar", f" ¿Está seguro de eliminar al paciente con cédula {cedula}?"):
                return
            
            try:
                self.controlador.eliminar_paciente(cedula)
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
                self.mostrar_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_eliminar = tk.Button(
            frame,
            text="Eliminar Paciente",
            command=eliminar,
            bg=self.colores['boton_danger'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_eliminar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.pack(pady=20)
    
    # ============ ELIMINAR DOCTOR ============
    
    def mostrar_eliminar_doctor(self):
        """Eliminar doctor"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text=" ELIMINAR DOCTOR",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=30)
        
        tk.Label(
            frame,
            text="ID del Doctor:",
            font=('Segoe UI', 11),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).grid(row=0, column=0, padx=5, pady=5)
        
        entry_id = tk.Entry(frame, width=25, font=('Segoe UI', 11))
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        def eliminar():
            id_doctor = entry_id.get().strip()
            if not id_doctor:
                messagebox.showwarning("Advertencia", "Ingrese un ID de doctor")
                return
            
            if not messagebox.askyesno("Confirmar", f" ¿Está seguro de eliminar al doctor con ID {id_doctor}?"):
                return
            
            try:
                self.controlador.eliminar_doctor(id_doctor)
                messagebox.showinfo("Éxito", "Doctor eliminado correctamente")
                self.mostrar_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_eliminar = tk.Button(
            frame,
            text="Eliminar Doctor",
            command=eliminar,
            bg=self.colores['boton_danger'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_eliminar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.pack(pady=20)
    
    # ============ AGENDAR CITA ============
    
    def mostrar_agendar_cita(self):
        """Agendar cita"""
        self.limpiar_frame()
        
        tk.Label(
            self.frame_principal,
            text=" AGENDAR CITA",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colores['fondo_principal'],
            fg=self.colores['texto_principal']
        ).pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg=self.colores['fondo_principal'])
        frame.pack(pady=15)
        
        pacientes = self._filtrar_none(self.controlador.obtener_pacientes())
        doctores = self._filtrar_none(self.controlador.obtener_doctores())
        
        if not pacientes:
            messagebox.showwarning("Advertencia", "Primero registre un paciente (Adulto Mayor 60+)")
            self.mostrar_dashboard()
            return
        
        if not doctores:
            messagebox.showwarning("Advertencia", "Primero registre un doctor")
            self.mostrar_dashboard()
            return
        
        lista_pacientes = [f"{p.cedula} - {p.nombres} {p.apellidos} ({p.edad} años)" for p in pacientes]
        lista_doctores = [f"{d.id_doctor} - {d.nombres} {d.apellidos} ({d.especialidad})" for d in doctores]
        
        campos = [
            ("Paciente *:", "combo_paciente", lista_pacientes),
            ("Doctor *:", "combo_doctor", lista_doctores),
            ("Fecha (YYYY-MM-DD) *:", "entry_fecha", None),
            ("Hora (HH:MM) *:", "entry_hora", None),
            ("Observaciones:", "entry_obs", None)
        ]
        
        entries = {}
        for i, (label, key, values) in enumerate(campos):
            tk.Label(
                frame,
                text=label,
                font=('Segoe UI', 10),
                bg=self.colores['fondo_principal'],
                fg=self.colores['texto_principal']
            ).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if values:
                entry = ttk.Combobox(frame, values=values, width=38, font=('Segoe UI', 10))
                entry.grid(row=i, column=1, padx=5, pady=5)
            else:
                entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
                entry.grid(row=i, column=1, padx=5, pady=5)
            
            entries[key] = entry
        
        def guardar():
            try:
                paciente_seleccionado = entries['combo_paciente'].get().strip()
                doctor_seleccionado = entries['combo_doctor'].get().strip()
                fecha = entries['entry_fecha'].get().strip()
                hora = entries['entry_hora'].get().strip()
                observaciones = entries['entry_obs'].get().strip()
                
                if not paciente_seleccionado or not doctor_seleccionado or not fecha or not hora:
                    messagebox.showerror("Error", "Paciente, doctor, fecha y hora son obligatorios")
                    return
                
                cedula = paciente_seleccionado.split(' - ')[0]
                id_doctor = doctor_seleccionado.split(' - ')[0]
                
                self.controlador.agendar_cita(cedula, id_doctor, fecha, hora, observaciones)
                messagebox.showinfo("Éxito", "Cita agendada correctamente")
                
                for entry in entries.values():
                    if hasattr(entry, 'set'):
                        entry.set('')
                    else:
                        entry.delete(0, tk.END)
                
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_guardar = tk.Button(
            frame,
            text=" Agendar Cita",
            command=guardar,
            bg=self.colores['boton_purple'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(
            frame,
            text="← Volver al Inicio",
            command=self.mostrar_dashboard,
            bg=self.colores['boton_gray'],
            fg=self.colores['texto_blanco'],
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT
        )
        btn_volver.grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
    
    def ejecutar(self):
        """Iniciar la aplicación"""
        self.root.mainloop()