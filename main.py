from controllers.sistema_controlador import Sistema
from model.paciente import Paciente
from model.doctor import Doctor
from model.medicamento import Medicamento
from model.persona import Persona

sistema = Sistema()
m1 = Medicamento("paracetamlo",5)
p1 = Paciente("Chesster Ivan" ,"Zacarias Jackson", 25,"89858-8579S","fundeci leon",8985-8595,)
d1 = Doctor(" Juan carlos ", "soto garcias",33,"5896-85895W","neurologo","0023")

sistema.agregar_paciente(p1)
sistema.agregar_doctor(d1)

sistema.asignar_doctor("89858-8579S", "0023")
sistema.crear_cita("89858-8579S", "0023", "2026-06-12")

sistema.ver_citas()