"""
Punto de entrada de la aplicación
SICAMED - Sistema de Gestión del Adulto Mayor
"""

from controllers.sistema_controlador import SistemaControlador
from view.interfaz_usuario import VentanaPrincipal

if __name__ == "__main__":
    print("=" * 50)
    print(" SICAMED - Sistema de Gestión del Adulto Mayor")
    print(" MINSA - Centro de Salud")
    print("=" * 50)
    print(" Iniciando aplicación...")
    
    # Crear controlador
    controlador = SistemaControlador()
    
    # Crear ventana principal
    app = VentanaPrincipal(controlador)
    app.ejecutar()
    
    print(" SICAMED cerrado")