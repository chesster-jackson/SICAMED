"""
Interfaz de Usuario con Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re


class VentanaPrincipal:
    """Ventana principal del sistema"""
    
    def __init__(self, controlador):
        self.controlador = controlador
        
        self.root = tk.Tk()
        self.root.title("SICAMED - Gestion del Adulto Mayor")
        self.root.geometry("900x750")
        self.root.configure(bg='#f0f4f8')
        
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
        
        titulo = tk.Label(self.frame_principal, 
                         text="SISTEMA DE GESTION DEL ADULTO MAYOR - MINSA",
                         font=('Arial', 18, 'bold'), bg='#f0f4f8', fg='#1a3b2e')
        titulo.pack(pady=15)
        
        subtitulo = tk.Label(self.frame_principal, 
                            text="Centro de Salud · Atencion Integral al Adulto Mayor",
                            font=('Arial', 11), bg='#f0f4f8', fg='#6c757d')
        subtitulo.pack(pady=5)
        
        tk.Frame(self.frame_principal, height=2, bg='#e9ecef').pack(fill=tk.X, pady=10)
        
        stats_frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        stats_frame.pack(pady=15)
        
        pacientes = self.controlador.contar_pacientes()
        doctores = self.controlador.contar_doctores()
        citas = self.controlador.contar_citas()
        
        stats = [
            (f"Pacientes: {pacientes}", "#e8f5ee"),
            (f"Doctores: {doctores}", "#e3f0ff"),
            (f"Citas: {citas}", "#fff3cd")
        ]
        
        for i, (texto, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, padx=25, pady=12, relief=tk.FLAT, bd=2)
            card.grid(row=0, column=i, padx=15)
            tk.Label(card, text=texto, font=('Arial', 14, 'bold'), bg=color).pack()
        
        tk.Label(self.frame_principal, text="--- ACCESO RAPIDO ---",
                font=('Arial', 12, 'bold'), bg='#f0f4f8', fg='#6c757d').pack(pady=15)
        
        botones_frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        botones_frame.pack(pady=10)
        
        botones = [
            ("Registrar Paciente", self.mostrar_registrar_paciente, "#4CAF50"),
            ("Registrar Doctor", self.mostrar_registrar_doctor, "#2196F3"),
            ("Buscar Paciente", self.mostrar_buscar_paciente, "#FF9800"),
            ("Buscar Doctor", self.mostrar_buscar_doctor, "#FF5722"),        # NUEVO
            ("Actualizar Paciente", self.mostrar_actualizar_paciente, "#795548"),
            ("Actualizar Doctor", self.mostrar_actualizar_doctor, "#607D8B"), # NUEVO
            ("Eliminar Paciente", self.mostrar_eliminar_paciente, "#f44336"),
            ("Eliminar Doctor", self.mostrar_eliminar_doctor, "#D32F2F"),     # NUEVO
            ("Agendar Cita", self.mostrar_agendar_cita, "#9C27B0"),
            ("Listar Pacientes", self.mostrar_listar_pacientes, "#00BCD4"),
            ("Listar Doctores", self.mostrar_listar_doctores, "#009688"),
            ("Ver Citas", self.mostrar_listar_citas, "#FF5722")
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(botones_frame, text=texto, command=comando,
                           bg=color, fg='white', font=('Arial', 9, 'bold'),
                           padx=12, pady=8, width=18, cursor='hand2',
                           relief=tk.FLAT)
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=6, pady=6)
    
    # ============================================================
    # REGISTRAR PACIENTE
    # ============================================================
    
    def mostrar_registrar_paciente(self):
        """Formulario para registrar paciente"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="REGISTRAR PACIENTE",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        aviso = tk.Label(self.frame_principal, 
                        text="ATENCION: Edad >= 60 años | Cedula: 123-123456-1234A | Nombres: solo letras",
                        font=('Arial', 10, 'bold'), fg='#d32f2f', bg='#f0f4f8')
        aviso.pack(pady=5)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        campos = [
            ("Nombres * (solo letras):", "entry_nombres"),
            ("Apellidos * (solo letras):", "entry_apellidos"),
            ("Edad * (60+):", "entry_edad"),
            ("Cedula * (123-123456-1234A):", "entry_cedula"),
            ("Telefono:", "entry_telefono"),
            ("Direccion:", "entry_direccion"),
            ("Email:", "entry_email")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, font=('Arial', 10), bg='#f0f4f8').grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(frame, width=38, font=('Arial', 10))
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
                
                # Validar campos obligatorios
                if not nombres or not apellidos or not edad or not cedula:
                    messagebox.showerror("Error", "Nombres, apellidos, edad y cedula son obligatorios")
                    return
                
                # Validar nombres (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in nombres):
                    messagebox.showerror("Error", "Los nombres solo pueden contener letras y espacios")
                    return
                
                # Validar apellidos (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in apellidos):
                    messagebox.showerror("Error", "Los apellidos solo pueden contener letras y espacios")
                    return
                
                # Validar formato de cedula
                patron = r'^\d{3}-\d{6}-\d{4}[A-Za-z]$'
                if not re.match(patron, cedula):
                    messagebox.showerror("Error", "Formato de cedula invalido. Debe ser: 123-123456-1234A")
                    return
                
                # Validar edad
                try:
                    edad_int = int(edad)
                    if edad_int < 60:
                        messagebox.showerror("Error", "El paciente debe ser mayor de 60 años (Adulto Mayor)")
                        return
                    if edad_int > 120:
                        messagebox.showerror("Error", "La edad no puede ser mayor a 120 años")
                        return
                except ValueError:
                    messagebox.showerror("Error", "La edad debe ser un numero valido")
                    return
                
                self.controlador.registrar_paciente(nombres, apellidos, edad_int, cedula, telefono, direccion, email)
                messagebox.showinfo("Exito", "Paciente registrado correctamente")
                
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_guardar = tk.Button(frame, text="Guardar Paciente", command=guardar,
                               bg="#4CAF50", fg='white', font=('Arial', 11, 'bold'),
                               padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(frame, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
    
    # ============================================================
    # REGISTRAR DOCTOR
    # ============================================================
    
    def mostrar_registrar_doctor(self):
        """Formulario para registrar doctor"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="REGISTRAR DOCTOR",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        aviso = tk.Label(self.frame_principal, 
                        text="ATENCION: Nombres solo letras | Cedula: 123-123456-1234A",
                        font=('Arial', 10, 'bold'), fg='#d32f2f', bg='#f0f4f8')
        aviso.pack(pady=5)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        campos = [
            ("Nombres * (solo letras):", "entry_nombres"),
            ("Apellidos * (solo letras):", "entry_apellidos"),
            ("Edad *:", "entry_edad"),
            ("Cedula * (123-123456-1234A):", "entry_cedula"),
            ("ID Doctor *:", "entry_id"),
            ("Especialidad *:", "entry_especialidad"),
            ("Telefono:", "entry_telefono")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, font=('Arial', 10), bg='#f0f4f8').grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(frame, width=38, font=('Arial', 10))
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
                
                # Validar nombres (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in nombres):
                    messagebox.showerror("Error", "Los nombres solo pueden contener letras y espacios")
                    return
                
                # Validar apellidos (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in apellidos):
                    messagebox.showerror("Error", "Los apellidos solo pueden contener letras y espacios")
                    return
                
                # Validar formato de cedula
                patron = r'^\d{3}-\d{6}-\d{4}[A-Za-z]$'
                if not re.match(patron, cedula):
                    messagebox.showerror("Error", "Formato de cedula invalido. Debe ser: 123-123456-1234A")
                    return
                
                self.controlador.registrar_doctor(nombres, apellidos, int(edad), cedula, id_doctor, especialidad, telefono)
                messagebox.showinfo("Exito", "Doctor registrado correctamente")
                
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_guardar = tk.Button(frame, text="Guardar Doctor", command=guardar,
                               bg="#2196F3", fg='white', font=('Arial', 11, 'bold'),
                               padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(frame, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
    
    # ============================================================
    # BUSCAR PACIENTE
    # ============================================================
    
    def mostrar_buscar_paciente(self):
        """Buscar paciente por cedula"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="BUSCAR PACIENTE",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        tk.Label(frame, text="Cedula (123-123456-1234A):", font=('Arial', 11), bg='#f0f4f8').grid(row=0, column=0, padx=5, pady=5)
        entry_cedula = tk.Entry(frame, width=25, font=('Arial', 11))
        entry_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        frame_resultados = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame_resultados.pack(pady=15, fill=tk.BOTH, expand=True)
        
        def buscar():
            for widget in frame_resultados.winfo_children():
                widget.destroy()
            
            cedula = entry_cedula.get().strip()
            if not cedula:
                messagebox.showwarning("Advertencia", "Ingrese una cedula")
                return
            
            try:
                paciente = self.controlador.buscar_paciente(cedula)
                if paciente:
                    info = f"""
DATOS DEL PACIENTE
----------------------------------------
Nombres:     {paciente.nombres}
Apellidos:   {paciente.apellidos}
Edad:        {paciente.edad} anos
Cedula:      {paciente.cedula}
Telefono:    {paciente.telefono or 'No registrado'}
Direccion:   {paciente.direccion or 'No registrada'}
Email:       {paciente.email or 'No registrado'}
----------------------------------------
"""
                    text_area = scrolledtext.ScrolledText(frame_resultados, width=65, height=12, font=('Courier', 10))
                    text_area.pack(pady=10)
                    text_area.insert('1.0', info)
                    text_area.config(state='disabled')
                else:
                    tk.Label(frame_resultados, text="Paciente no encontrado", 
                            font=('Arial', 14, 'bold'), fg='red', bg='#f0f4f8').pack()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_buscar = tk.Button(frame, text="Buscar", command=buscar,
                              bg="#FF9800", fg='white', font=('Arial', 11, 'bold'),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_buscar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)
    
    # ============================================================
    # ACTUALIZAR PACIENTE
    # ============================================================
    
    def mostrar_actualizar_paciente(self):
        """Actualizar paciente"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="ACTUALIZAR PACIENTE",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        tk.Label(frame, text="Cedula (123-123456-1234A):", font=('Arial', 10), bg='#f0f4f8').grid(row=0, column=0, padx=5, pady=5)
        entry_cedula = tk.Entry(frame, width=25, font=('Arial', 10))
        entry_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        btn_cargar = tk.Button(frame, text="Cargar Datos", command=lambda: cargar(),
                              bg="#795548", fg='white', font=('Arial', 10, 'bold'),
                              padx=15, pady=5, cursor='hand2', relief=tk.FLAT)
        btn_cargar.grid(row=0, column=2, padx=10, pady=5)
        
        frame_datos = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame_datos.pack(pady=15)
        
        entries = {}
        campos = ["Nombres", "Apellidos", "Edad", "Telefono", "Direccion", "Email"]
        
        for i, campo in enumerate(campos):
            tk.Label(frame_datos, text=f"{campo}:", font=('Arial', 10), bg='#f0f4f8').grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(frame_datos, width=38, font=('Arial', 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[campo.lower()] = entry
        
        def cargar():
            cedula = entry_cedula.get().strip()
            if not cedula:
                messagebox.showwarning("Advertencia", "Ingrese una cedula")
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
                    entries['telefono'].delete(0, tk.END)
                    entries['telefono'].insert(0, paciente.telefono)
                    entries['direccion'].delete(0, tk.END)
                    entries['direccion'].insert(0, paciente.direccion)
                    entries['email'].delete(0, tk.END)
                    entries['email'].insert(0, paciente.email)
                    messagebox.showinfo("Exito", "Paciente cargado para actualizar")
                else:
                    messagebox.showerror("Error", "Paciente no encontrado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def actualizar():
            try:
                cedula = entry_cedula.get().strip()
                nombres = entries['nombres'].get().strip()
                apellidos = entries['apellidos'].get().strip()
                edad = entries['edad'].get().strip()
                telefono = entries['telefono'].get().strip()
                direccion = entries['direccion'].get().strip()
                email = entries['email'].get().strip()
                
                if not nombres or not apellidos or not edad:
                    messagebox.showerror("Error", "Nombres, apellidos y edad son obligatorios")
                    return
                
                # Validar nombres (solo letras y espacios)
                if not all(c.isalpha() or c.isspace() for c in nombres):
                    messagebox.showerror("Error", "Los nombres solo pueden contener letras y espacios")
                    return
                
                if not all(c.isalpha() or c.isspace() for c in apellidos):
                    messagebox.showerror("Error", "Los apellidos solo pueden contener letras y espacios")
                    return
                
                self.controlador.actualizar_paciente(cedula, nombres, apellidos, int(edad), telefono, direccion, email)
                messagebox.showinfo("Exito", "Paciente actualizado correctamente")
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_actualizar = tk.Button(self.frame_principal, text="Actualizar Paciente", command=actualizar,
                                  bg="#795548", fg='white', font=('Arial', 11, 'bold'),
                                  padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_actualizar.pack(pady=10)
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=5)
    
    # ============================================================
    # ELIMINAR PACIENTE
    # ============================================================
    
    def mostrar_eliminar_paciente(self):
        """Eliminar paciente"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="ELIMINAR PACIENTE",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=30)
        
        tk.Label(frame, text="Cedula (123-123456-1234A):", font=('Arial', 11), bg='#f0f4f8').grid(row=0, column=0, padx=5, pady=5)
        entry_cedula = tk.Entry(frame, width=25, font=('Arial', 11))
        entry_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        def eliminar():
            cedula = entry_cedula.get().strip()
            if not cedula:
                messagebox.showwarning("Advertencia", "Ingrese una cedula")
                return
            
            # Confirmar eliminacion
            if not messagebox.askyesno("Confirmar", f"¿Esta seguro de eliminar al paciente con cedula {cedula}?"):
                return
            
            try:
                self.controlador.eliminar_paciente(cedula)
                messagebox.showinfo("Exito", "Paciente eliminado correctamente")
                self.mostrar_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_eliminar = tk.Button(frame, text="Eliminar Paciente", command=eliminar,
                                bg="#f44336", fg='white', font=('Arial', 11, 'bold'),
                                padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=20)
    
    # ============================================================
    # LISTAR PACIENTES
    # ============================================================
    
    def mostrar_listar_pacientes(self):
        """Listar todos los pacientes"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="LISTA DE PACIENTES",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columnas = ('Cedula', 'Nombres', 'Apellidos', 'Edad', 'Telefono')
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
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)
    
    # ============================================================
    # LISTAR DOCTORES
    # ============================================================
    
    def mostrar_listar_doctores(self):
        """Listar todos los doctores"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="LISTA DE DOCTORES",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columnas = ('ID', 'Nombres', 'Apellidos', 'Especialidad', 'Telefono')
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
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)
    
    # ============================================================
    # AGENDAR CITA
    # ============================================================
    
    def mostrar_agendar_cita(self):
        """Agendar cita"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="AGENDAR CITA",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        pacientes = self.controlador.obtener_pacientes()
        doctores = self.controlador.obtener_doctores()
        
        lista_pacientes = [f"{p.cedula} - {p.nombre_completo} ({p.edad} anos)" for p in pacientes]
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
                entry = ttk.Combobox(frame, values=values, width=38, font=('Arial', 10))
                entry.grid(row=i, column=1, padx=5, pady=5)
            else:
                entry = tk.Entry(frame, width=40, font=('Arial', 10))
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
                messagebox.showinfo("Exito", "Cita agendada correctamente")
                
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
        
        btn_guardar = tk.Button(frame, text="Agendar Cita", command=guardar,
                               bg="#9C27B0", fg='white', font=('Arial', 11, 'bold'),
                               padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        btn_volver = tk.Button(frame, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
    
    # ============================================================
    # VER CITAS
    # ============================================================
    
    def mostrar_listar_citas(self):
        """Listar todas las citas"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="LISTA DE CITAS",
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
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                              bg="#757575", fg='white', font=('Arial', 10),
                              padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)


    def mostrar_buscar_doctor(self):
        """Buscar doctor por ID"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="BUSCAR DOCTOR",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        tk.Label(frame, text="ID del Doctor:", font=('Arial', 11), bg='#f0f4f8').grid(row=0, column=0, padx=5, pady=5)
        entry_id = tk.Entry(frame, width=25, font=('Arial', 11))
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        frame_resultados = tk.Frame(self.frame_principal, bg='#f0f4f8')
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
                    info = f"""
    DATOS DEL DOCTOR
    ----------------------------------------
    Nombres:     {doctor.nombres}
    Apellidos:   {doctor.apellidos}
    Edad:        {doctor.edad} anos
    Cedula:      {doctor.cedula}
    ID Doctor:   {doctor.id_doctor}
    Especialidad:{doctor.especialidad}
    Telefono:    {doctor.telefono or 'No registrado'}
    ----------------------------------------
    """
                    text_area = scrolledtext.ScrolledText(frame_resultados, width=65, height=12, font=('Courier', 10))
                    text_area.pack(pady=10)
                    text_area.insert('1.0', info)
                    text_area.config(state='disabled')
                else:
                    tk.Label(frame_resultados, text="Doctor no encontrado", 
                            font=('Arial', 14, 'bold'), fg='red', bg='#f0f4f8').pack()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_buscar = tk.Button(frame, text="Buscar", command=buscar,
                            bg="#FF5722", fg='white', font=('Arial', 11, 'bold'),
                            padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_buscar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                            bg="#757575", fg='white', font=('Arial', 10),
                            padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=10)
    

    def mostrar_actualizar_doctor(self):
        """Actualizar doctor"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="ACTUALIZAR DOCTOR",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=15)
        
        tk.Label(frame, text="ID del Doctor:", font=('Arial', 10), bg='#f0f4f8').grid(row=0, column=0, padx=5, pady=5)
        entry_id = tk.Entry(frame, width=25, font=('Arial', 10))
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        btn_cargar = tk.Button(frame, text="Cargar Datos", command=lambda: cargar(),
                            bg="#607D8B", fg='white', font=('Arial', 10, 'bold'),
                            padx=15, pady=5, cursor='hand2', relief=tk.FLAT)
        btn_cargar.grid(row=0, column=2, padx=10, pady=5)
        
        frame_datos = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame_datos.pack(pady=15)
        
        entries = {}
        campos = ["Nombres", "Apellidos", "Edad", "Cedula", "Especialidad", "Telefono"]
        
        for i, campo in enumerate(campos):
            tk.Label(frame_datos, text=f"{campo}:", font=('Arial', 10), bg='#f0f4f8').grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(frame_datos, width=38, font=('Arial', 10))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[campo.lower()] = entry
        
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
                    entries['cedula'].delete(0, tk.END)
                    entries['cedula'].insert(0, doctor.cedula)
                    entries['especialidad'].delete(0, tk.END)
                    entries['especialidad'].insert(0, doctor.especialidad)
                    entries['telefono'].delete(0, tk.END)
                    entries['telefono'].insert(0, doctor.telefono)
                    messagebox.showinfo("Exito", "Doctor cargado para actualizar")
                else:
                    messagebox.showerror("Error", "Doctor no encontrado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def actualizar():
            try:
                id_doctor = entry_id.get().strip()
                nombres = entries['nombres'].get().strip()
                apellidos = entries['apellidos'].get().strip()
                edad = entries['edad'].get().strip()
                cedula = entries['cedula'].get().strip()
                especialidad = entries['especialidad'].get().strip()
                telefono = entries['telefono'].get().strip()
                
                if not nombres or not apellidos or not edad or not cedula or not especialidad:
                    messagebox.showerror("Error", "Nombres, apellidos, edad, cedula y especialidad son obligatorios")
                    return
                
                # Validar nombres
                if not all(c.isalpha() or c.isspace() for c in nombres):
                    messagebox.showerror("Error", "Los nombres solo pueden contener letras y espacios")
                    return
                
                if not all(c.isalpha() or c.isspace() for c in apellidos):
                    messagebox.showerror("Error", "Los apellidos solo pueden contener letras y espacios")
                    return
                
                self.controlador.actualizar_doctor(id_doctor, nombres, apellidos, int(edad), cedula, especialidad, telefono)
                messagebox.showinfo("Exito", "Doctor actualizado correctamente")
                self.mostrar_dashboard()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_actualizar = tk.Button(self.frame_principal, text="Actualizar Doctor", command=actualizar,
                                bg="#607D8B", fg='white', font=('Arial', 11, 'bold'),
                                padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_actualizar.pack(pady=10)
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                            bg="#757575", fg='white', font=('Arial', 10),
                            padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=5)


    def mostrar_eliminar_doctor(self):
        """Eliminar doctor"""
        self.limpiar_frame()
        
        tk.Label(self.frame_principal, text="ELIMINAR DOCTOR",
                font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#1a3b2e').pack(pady=10)
        
        frame = tk.Frame(self.frame_principal, bg='#f0f4f8')
        frame.pack(pady=30)
        
        tk.Label(frame, text="ID del Doctor:", font=('Arial', 11), bg='#f0f4f8').grid(row=0, column=0, padx=5, pady=5)
        entry_id = tk.Entry(frame, width=25, font=('Arial', 11))
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        def eliminar():
            id_doctor = entry_id.get().strip()
            if not id_doctor:
                messagebox.showwarning("Advertencia", "Ingrese un ID de doctor")
                return
            
            if not messagebox.askyesno("Confirmar", f"¿Esta seguro de eliminar al doctor con ID {id_doctor}?"):
                return
            
            try:
                self.controlador.eliminar_doctor(id_doctor)
                messagebox.showinfo("Exito", "Doctor eliminado correctamente")
                self.mostrar_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        btn_eliminar = tk.Button(frame, text="Eliminar Doctor", command=eliminar,
                                bg="#D32F2F", fg='white', font=('Arial', 11, 'bold'),
                                padx=30, pady=10, cursor='hand2', relief=tk.FLAT)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=5)
        
        btn_volver = tk.Button(self.frame_principal, text="Volver al Inicio", command=self.mostrar_dashboard,
                            bg="#757575", fg='white', font=('Arial', 10),
                            padx=20, pady=8, cursor='hand2', relief=tk.FLAT)
        btn_volver.pack(pady=20)

    def ejecutar(self):
        """Iniciar la aplicacion"""
        self.root.mainloop()