import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class VentanaPrincipal:
    
    def __init__(self, controlador):
        self.controlador = controlador
        
        # Ventana principal
        self.root = tk.Tk()
        self.root.title("SICAMED - Gestión del Adulto Mayor")
        self.root.geometry("850x700")
        self.root.configure(bg='#f0f4f8')
        
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg='#f0f4f8')
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.mostrar_dashboard()
    
    def limpiar_frame(self):
        """Limpiar el frame principal"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        """Mostrar dashboard principal"""
        self.limpiar_frame()
        
        # Título
        titulo = tk.Label(self.frame_principal, 
                         text=" SISTEMA DE GESTIÓN DEL ADULTO MAYOR - MINSA",
                         font=('Arial', 18, 'bold'), bg='#f0f4f8', fg='#1a3b2e')
        titulo.pack(pady=15)
        
        # Subtítulo
        subtitulo = tk.Label(self.frame_principal, 
                            text="Centro de Salud · Atención Integral al Adulto Mayor",
                            font=('Arial', 11), bg='#f0f4f8', fg='#6c757d')
        subtitulo.pack(pady=5)
        
        # Línea separadora
        tk.Frame(self.frame_principal, height=2, bg='#e9ecef').pack(fill=tk.X, pady=10)
        
        # Estadísticas
        stats_frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        stats_frame.pack(pady=15)
        
        try:
            pacientes = len(self.controlador.obtener_pacientes())
            doctores = len(self.controlador.obtener_doctores())
            citas = len(self.controlador.obtener_citas())
        except:
            pacientes = doctores = citas = 0
        
        # Tarjetas de estadísticas
        stats = [
            (f" {pacientes}", "Pacientes", "#e8f5ee"),
            (f" {doctores}", "Doctores", "#e3f0ff"),
            (f" {citas}", "Citas", "#fff3cd")
        ]
        
        for i, (numero, label, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, padx=20, pady=10, relief=tk.FLAT)
            card.grid(row=0, column=i, padx=15)
            
            tk.Label(card, text=numero, font=('Arial', 18, 'bold'), bg=color).pack()
            tk.Label(card, text=label, font=('Arial', 10), bg=color).pack()
        
        # Botones de acceso rápido
        tk.Label(self.frame_principal, text="--- ACCESO RÁPIDO ---",
                font=('Arial', 12, 'bold'), bg='#f0f4f8', fg='#6c757d').pack(pady=15)
        
        botones_frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        botones_frame.pack(pady=10)
        
        botones = [
            (" Registrar Paciente", self.mostrar_registrar_paciente, "#4CAF50"),
            (" Registrar Doctor", self.mostrar_registrar_doctor, "#2196F3"),
            (" Buscar Paciente", self.mostrar_buscar_paciente, "#FF9800"),
            (" Agendar Cita", self.mostrar_agendar_cita, "#f44336"),
            (" Listar Pacientes", self.mostrar_listar_pacientes, "#9C27B0"),
            (" Listar Doctores", self.mostrar_listar_doctores, "#00BCD4"),
            (" Ver Citas", self.mostrar_listar_citas, "#795548")
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(botones_frame, text=texto, command=comando,
                           bg=color, fg='white', font=('Arial', 10, 'bold'),
                           padx=15, pady=10, width=20, cursor='hand2',
                           relief=tk.FLAT)
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=8, pady=8)
    
    # ===== REGISTRAR PACIENTE =====
    
    def mostrar_registrar_paciente(self):
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text=" REGISTRAR PACIENTE",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        # Mensaje de advertencia sobre la edad
        aviso = tk.Label(self.frame_principal, 
                        text="⚠️ La edad debe ser mayor o igual a 60 años (Adulto Mayor)",
                        font=('Arial', 10, 'bold'), fg='#d32f2f', bg='#f0f4f8')
        aviso.pack(pady=5)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        campos = [
            ("Nombres *:", "entry_nombres"),
            ("Apellidos *:", "entry_apellidos"),
            ("Edad * (60+):", "entry_edad"),
            ("Cédula * (8 dígitos):", "entry_cedula"),
            ("Teléfono:", "entry_telefono"),
            ("Dirección:", "entry_direccion"),
            ("Email:", "entry_email")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, font=('Arial', 10), bg='#f0f4f8').grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(frame, width=35, font=('Arial', 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry
        
        def guardar():
            try:
                nombres = entries['entry_nombres'].get().strip()
                apellidos = entries['entry_apellidos'].get().strip()
                edad = entries['entry_edad'].get().strip()
                cedula = entries['entry_cedula'].get().strip()
                telefono = entries['entry_telefono'].get().strip()
                direccion = entries['entry_direccion'].get().strip()
                email = entries['entry_email'].get().strip()
                
                if not nombres or not apellidos or not edad or not cedula:
                    messagebox.showerror("Error", "Nombres, apellidos, edad y cédula son obligatorios")
                    return
                
                # Validar edad
                try:
                    edad_int = int(edad)
                    if edad_int < 60:
                        messagebox.showerror("Error", " La edad debe ser mayor o igual a 60 años (Adulto Mayor)")
                        return
                    if edad_int > 120:
                        messagebox.showerror("Error", " La edad no puede ser mayor a 120 años")
                        return
                except ValueError:
                    messagebox.showerror("Error", " La edad debe ser un número válido")
                    return
                
                self.controlador.registrar_paciente(nombres, apellidos, edad_int, cedula, telefono, direccion, email)
                messagebox.showinfo("Éxito", " Paciente registrado correctamente")
                
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_guardar = tk.Button(frame, text=" Guardar Paciente", command=guardar,
                               bg="#4CAF50", fg='white', font=('Arial', 11, 'bold'),
                               padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(frame, text="⬅ Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
    
    # ===== REGISTRAR DOCTOR =====
    
    def mostrar_registrar_doctor(self):
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text=" REGISTRAR DOCTOR",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        campos = [
            ("Nombres *:", "entry_nombres"),
            ("Apellidos *:", "entry_apellidos"),
            ("Edad *:", "entry_edad"),
            ("Cédula *:", "entry_cedula"),
            ("ID Doctor *:", "entry_id"),
            ("Especialidad *:", "entry_especialidad"),
            ("Teléfono:", "entry_telefono")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, font=('Arial', 10), bg='#f0f4f8').grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(frame, width=35, font=('Arial', 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry
        
        def guardar():
            try:
                nombres = entries['entry_nombres'].get().strip()
                apellidos = entries['entry_apellidos'].get().strip()
                edad = entries['entry_edad'].get().strip()
                cedula = entries['entry_cedula'].get().strip()
                id_doctor = entries['entry_id'].get().strip()
                especialidad = entries['entry_especialidad'].get().strip()
                telefono = entries['entry_telefono'].get().strip()
                
                if not nombres or not apellidos or not edad or not cedula or not id_doctor or not especialidad:
                    messagebox.showerror("Error", "Todos los campos con * son obligatorios")
                    return
                
                self.controlador.registrar_doctor(nombres, apellidos, int(edad), cedula, id_doctor, especialidad, telefono)
                messagebox.showinfo("Éxito", " Doctor registrado correctamente")
                
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_guardar = tk.Button(frame, text=" Guardar Doctor", command=guardar,
                               bg="#2196F3", fg='white', font=('Arial', 11, 'bold'),
                               padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(frame, text="⬅ Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
    
    # ===== BUSCAR PACIENTE =====
    
    def mostrar_buscar_paciente(self):
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text=" BUSCAR PACIENTE",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        tk.Label(frame, text="Cédula:", font=('Arial', 11), bg='#f0f4f8').grid(row=0, column=0, padx=5, pady=5)
        entry_cedula = tk.Entry(frame, width=25, font=('Arial', 11))
        entry_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        frame_resultados = tk.Frame(self.frame_principal, bg='#f0f4f8')
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
                    info = f"""
╔══════════════════════════════════════════════════════╗
║              DATOS DEL PACIENTE                     ║
╠══════════════════════════════════════════════════════╣
║  Nombres:     {paciente.nombres:<30} ║
║  Apellidos:   {paciente.apellidos:<30} ║
║  Edad:        {paciente.edad:<30} años ║
║  Cédula:      {paciente.cedula:<30} ║
║  Teléfono:    {paciente.telefono or 'No registrado':<30} ║
║  Dirección:   {paciente.direccion or 'No registrada':<30} ║
║  Email:       {paciente.email or 'No registrado':<30} ║
╚══════════════════════════════════════════════════════╝
"""
                    text_area = scrolledtext.ScrolledText(frame_resultados, width=60, height=12, font=('Courier', 10))
                    text_area.pack(pady=10)
                    text_area.insert('1.0', info)
                    text_area.config(state='disabled')
                else:
                    tk.Label(frame_resultados, text=" Paciente no encontrado", 
                            font=('Arial', 14, 'bold'), fg='red', bg='#f0f4f8').pack()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_buscar = tk.Button(frame, text="🔍 Buscar", command=buscar,
                              bg="#FF9800", fg='white', font=('Arial', 11, 'bold'),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_buscar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(self.frame_principal, text="⬅ Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)
    
    # ===== LISTAR PACIENTES =====
    
    def mostrar_listar_pacientes(self):
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text=" LISTA DE PACIENTES",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columnas = ('Cédula', 'Nombres', 'Apellidos', 'Edad', 'Teléfono')
        tree = ttk.Treeview(frame, columns=columnas, show='headings', height=15)
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        pacientes = self.controlador.obtener_pacientes()
        for p in pacientes:
            tree.insert('', tk.END, values=(p.cedula, p.nombres, p.apellidos, p.edad, p.telefono))
        
        if not pacientes:
            tk.Label(frame, text="No hay pacientes registrados", 
                    font=('Arial', 12), bg='#f0f4f8').pack(pady=20)
        
        btn_volver = tk.Button(self.frame_principal, text="⬅ Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)
    
    # ===== LISTAR DOCTORES =====
    
    def mostrar_listar_doctores(self):
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text=" LISTA DE DOCTORES",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columnas = ('ID', 'Nombres', 'Apellidos', 'Especialidad', 'Teléfono')
        tree = ttk.Treeview(frame, columns=columnas, show='headings', height=15)
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        doctores = self.controlador.obtener_doctores()
        for d in doctores:
            tree.insert('', tk.END, values=(d.id_doctor, d.nombres, d.apellidos, d.especialidad, d.telefono))
        
        if not doctores:
            tk.Label(frame, text="No hay doctores registrados", 
                    font=('Arial', 12), bg='#f0f4f8').pack(pady=20)
        
        btn_volver = tk.Button(self.frame_principal, text="⬅ Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)
    
    # ===== AGENDAR CITA =====
    
    def mostrar_agendar_cita(self):
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text=" AGENDAR CITA",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        pacientes = self.controlador.obtener_pacientes()
        doctores = self.controlador.obtener_doctores()
        
        lista_pacientes = [f"{p.cedula} - {p.nombre_completo} ({p.edad} años)" for p in pacientes]
        lista_doctores = [f"{d.id_doctor} - {d.nombre_completo} ({d.especialidad})" for d in doctores]
        
        if not pacientes:
            messagebox.showwarning("Advertencia", "Primero registre un paciente (Adulto Mayor 60+)")
            self.mostrar_dashboard()
            return
        
        if not doctores:
            messagebox.showwarning("Advertencia", "Primero registre un doctor")
            self.mostrar_dashboard()
            return
        
        campos = [
            ("Paciente *:", "combo_paciente", lista_pacientes),
            ("Doctor *:", "combo_doctor", lista_doctores),
            ("Fecha (YYYY-MM-DD) *:", "entry_fecha", None),
            ("Hora (HH:MM) *:", "entry_hora", None),
            ("Observaciones:", "entry_obs", None)
        ]
        
        entries = {}
        for i, (label, key, values) in enumerate(campos):
            tk.Label(frame, text=label, font=('Arial', 10), bg='#f0f4f8').grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if values:
                entry = ttk.Combobox(frame, values=values, width=35, font=('Arial', 10))
                entry.grid(row=i, column=1, padx=5, pady=5)
            else:
                entry = tk.Entry(frame, width=37, font=('Arial', 10))
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
                messagebox.showinfo("Éxito", " Cita agendada correctamente")
                
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
        
        btn_guardar = tk.Button(frame, text=" Agendar Cita", command=guardar,
                               bg="#f44336", fg='white', font=('Arial', 11, 'bold'),
                               padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(frame, text="⬅ Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
    
    # ===== LISTAR CITAS =====
    
    def mostrar_listar_citas(self):
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text=" LISTA DE CITAS",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columnas = ('ID', 'Paciente', 'Doctor', 'Fecha', 'Hora', 'Estado')
        tree = ttk.Treeview(frame, columns=columnas, show='headings', height=15)
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        citas = self.controlador.obtener_citas()
        pacientes = self.controlador.obtener_pacientes()
        doctores = self.controlador.obtener_doctores()
        
        for c in citas:
            paciente = next((p for p in pacientes if p.cedula == c.cedula_paciente), None)
            doctor = next((d for d in doctores if d.id_doctor == c.id_doctor), None)
            
            nombre_paciente = paciente.nombre_completo if paciente else c.cedula_paciente
            nombre_doctor = doctor.nombre_completo if doctor else c.id_doctor
            
            tree.insert('', tk.END, values=(c.id, nombre_paciente, nombre_doctor, c.fecha, c.hora, c.estado))
        
        if not citas:
            tk.Label(frame, text="No hay citas registradas", 
                    font=('Arial', 12), bg='#f0f4f8').pack(pady=20)
        
        btn_volver = tk.Button(self.frame_principal, text="⬅ Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)
    
    def ejecutar(self):
        """Iniciar la aplicación"""
        self.root.mainloop()