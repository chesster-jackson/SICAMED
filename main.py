from controllers.sistema_controlador import SistemaControlador
from view.interfaz_usuario import VentanaPrincipal

if __name__ == "__main__":
    print("=" * 50)
    print("SICAMED - Sistema de Gestion del Adulto Mayor")
    print("MINSA - Centro de Salud")
    print("=" * 50)
    print("Iniciando aplicacion...")
    
    controlador = SistemaControlador()
    app = VentanaPrincipal(controlador)
    app.ejecutar()
    
    print("SICAMED cerrado")