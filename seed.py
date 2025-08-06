import asyncio
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import AsyncSessionLocal
from app.schemas.responses import (
    ClinicaCreate, PacienteCreate, ProfesionalCreate, 
    EspecialidadCreate, TurnoCreate, LogIACreate
)
from app.repositories.repositories import (
    clinica_repo, paciente_repo, profesional_repo,
    especialidad_repo, turno_repo, log_ia_repo
)

# Cargar variables de entorno
load_dotenv()

async def create_seed_data():
    """Crear datos de prueba para el sistema"""
    async with AsyncSessionLocal() as db:
        try:
            print("🌱 Iniciando seed de datos...")
            
            # 1. Crear 2 clínicas
            print("📋 Creando clínicas...")
            clinicas_data = [
                {
                    "nombre": "Clínica San Rafael",
                    "configuraciones": {
                        "horario_atencion": {"inicio": "08:00", "fin": "18:00"},
                        "duracion_turno": 30,
                        "dias_laborables": ["lunes", "martes", "miercoles", "jueves", "viernes"]
                    },
                    "did_whatsapp": "549123456789",
                    "activa": True
                },
                {
                    "nombre": "Centro Médico Norte",
                    "configuraciones": {
                        "horario_atencion": {"inicio": "07:00", "fin": "20:00"},
                        "duracion_turno": 45,
                        "dias_laborables": ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"]
                    },
                    "did_whatsapp": "549987654321",
                    "activa": True
                }
            ]
            
            clinicas = []
            for clinica_data in clinicas_data:
                clinica = await clinica_repo.create(db, obj_in=ClinicaCreate(**clinica_data))
                clinicas.append(clinica)
                print(f"  ✅ Clínica creada: {clinica.nombre}")
            
            # 2. Crear especialidades
            print("🏥 Creando especialidades...")
            especialidades_data = [
                {
                    "nombre": "Cardiología",
                    "descripcion": "Especialidad médica que se ocupa del corazón y del sistema circulatorio",
                    "preparacion_previa": "Ayuno de 4 horas. Traer estudios previos."
                },
                {
                    "nombre": "Dermatología",
                    "descripcion": "Especialidad médica que se ocupa de la piel",
                    "preparacion_previa": "No usar cremas ni maquillaje el día de la consulta."
                },
                {
                    "nombre": "Traumatología",
                    "descripcion": "Especialidad que trata lesiones del sistema musculoesquelético",
                    "preparacion_previa": "Traer estudios radiológicos previos si los tiene."
                }
            ]
            
            especialidades = []
            for clinica in clinicas:
                for esp_data in especialidades_data:
                    esp_data_with_clinica = {**esp_data, "id_clinica": clinica.id}
                    especialidad = await especialidad_repo.create(
                        db, obj_in=EspecialidadCreate(**esp_data_with_clinica)
                    )
                    especialidades.append(especialidad)
                    print(f"  ✅ Especialidad creada: {especialidad.nombre} en {clinica.nombre}")
            
            # 3. Crear 5 profesionales
            print("👨‍⚕️ Creando profesionales...")
            profesionales_data = [
                {
                    "nombre": "Dr. Carlos Mendoza",
                    "especialidades": ["Cardiología"],
                    "horarios": {
                        "lunes": [{"inicio": "08:00", "fin": "12:00"}],
                        "miercoles": [{"inicio": "14:00", "fin": "18:00"}],
                        "viernes": [{"inicio": "08:00", "fin": "12:00"}]
                    },
                    "activo": True,
                    "id_clinica": clinicas[0].id
                },
                {
                    "nombre": "Dra. Ana García",
                    "especialidades": ["Dermatología"],
                    "horarios": {
                        "martes": [{"inicio": "09:00", "fin": "13:00"}],
                        "jueves": [{"inicio": "15:00", "fin": "19:00"}]
                    },
                    "activo": True,
                    "id_clinica": clinicas[0].id
                },
                {
                    "nombre": "Dr. Roberto Silva",
                    "especialidades": ["Traumatología"],
                    "horarios": {
                        "lunes": [{"inicio": "14:00", "fin": "18:00"}],
                        "miercoles": [{"inicio": "08:00", "fin": "12:00"}],
                        "viernes": [{"inicio": "14:00", "fin": "18:00"}]
                    },
                    "activo": True,
                    "id_clinica": clinicas[1].id
                },
                {
                    "nombre": "Dra. María López",
                    "especialidades": ["Cardiología", "Medicina General"],
                    "horarios": {
                        "martes": [{"inicio": "08:00", "fin": "16:00"}],
                        "jueves": [{"inicio": "08:00", "fin": "16:00"}]
                    },
                    "activo": True,
                    "id_clinica": clinicas[1].id
                },
                {
                    "nombre": "Dr. Luis Fernández",
                    "especialidades": ["Dermatología"],
                    "horarios": {
                        "lunes": [{"inicio": "08:00", "fin": "12:00"}],
                        "martes": [{"inicio": "14:00", "fin": "18:00"}],
                        "miercoles": [{"inicio": "08:00", "fin": "12:00"}]
                    },
                    "activo": True,
                    "id_clinica": clinicas[0].id
                }
            ]
            
            profesionales = []
            for prof_data in profesionales_data:
                profesional = await profesional_repo.create(db, obj_in=ProfesionalCreate(**prof_data))
                profesionales.append(profesional)
                print(f"  ✅ Profesional creado: {profesional.nombre}")
            
            # 4. Crear 10 pacientes
            print("👥 Creando pacientes...")
            pacientes_data = [
                {"dni": "12345678", "telefono": "1234567890", "nombre": "Juan Pérez", "email": "juan@email.com"},
                {"dni": "23456789", "telefono": "2345678901", "nombre": "María González", "email": "maria@email.com"},
                {"dni": "34567890", "telefono": "3456789012", "nombre": "Pedro Rodríguez", "email": "pedro@email.com"},
                {"dni": "45678901", "telefono": "4567890123", "nombre": "Ana Martínez", "email": "ana@email.com"},
                {"dni": "56789012", "telefono": "5678901234", "nombre": "Carlos López", "email": "carlos@email.com"},
                {"dni": "67890123", "telefono": "6789012345", "nombre": "Laura Sánchez", "email": "laura@email.com"},
                {"dni": "78901234", "telefono": "7890123456", "nombre": "Miguel Torres", "email": "miguel@email.com"},
                {"dni": "89012345", "telefono": "8901234567", "nombre": "Sofia Herrera", "email": "sofia@email.com"},
                {"dni": "90123456", "telefono": "9012345678", "nombre": "Diego Morales", "email": "diego@email.com"},
                {"dni": "01234567", "telefono": "0123456789", "nombre": "Carmen Ruiz", "email": "carmen@email.com"}
            ]
            
            pacientes = []
            for i, paciente_data in enumerate(pacientes_data):
                # Alternar entre las dos clínicas
                clinica_id = clinicas[i % 2].id
                paciente_data_with_clinica = {**paciente_data, "id_clinica": clinica_id}
                paciente = await paciente_repo.create(db, obj_in=PacienteCreate(**paciente_data_with_clinica))
                pacientes.append(paciente)
                print(f"  ✅ Paciente creado: {paciente.nombre}")
            
            # 5. Crear algunos turnos
            print("📅 Creando turnos...")
            base_date = datetime.now() + timedelta(days=1)
            turnos_data = [
                {
                    "id_paciente": pacientes[0].id,
                    "id_profesional": profesionales[0].id,
                    "id_clinica": clinicas[0].id,
                    "fecha_hora": base_date.replace(hour=9, minute=0),
                    "estado": "programado",
                    "observaciones": "Primera consulta"
                },
                {
                    "id_paciente": pacientes[1].id,
                    "id_profesional": profesionales[1].id,
                    "id_clinica": clinicas[0].id,
                    "fecha_hora": base_date.replace(hour=10, minute=0),
                    "estado": "confirmado",
                    "observaciones": "Control de rutina"
                },
                {
                    "id_paciente": pacientes[2].id,
                    "id_profesional": profesionales[2].id,
                    "id_clinica": clinicas[1].id,
                    "fecha_hora": base_date.replace(hour=15, minute=0),
                    "estado": "programado",
                    "observaciones": None
                }
            ]
            
            for turno_data in turnos_data:
                turno = await turno_repo.create(db, obj_in=TurnoCreate(**turno_data))
                print(f"  ✅ Turno creado: {turno.fecha_hora}")
            
            # 6. Crear logs de IA
            print("🤖 Creando logs de IA...")
            logs_data = [
                {
                    "mensaje": "Quiero solicitar un turno con cardiología",
                    "respuesta_ia": "Perfecto, puedo ayudarte a solicitar un turno con cardiología. ¿Podrías proporcionarme tu DNI?",
                    "confianza": "alta",
                    "metadatos": {"intent": "solicitar_turno", "especialidad": "cardiologia"}
                },
                {
                    "mensaje": "Mi DNI es 12345678",
                    "respuesta_ia": "Gracias. Encontré tu registro, Juan Pérez. Te muestro los turnos disponibles para cardiología.",
                    "confianza": "alta",
                    "metadatos": {"intent": "proporcionar_dni", "paciente_encontrado": True}
                },
                {
                    "mensaje": "¿Qué horarios tienen disponibles?",
                    "respuesta_ia": "Los horarios disponibles para cardiología son: Lunes 08:00-12:00, Miércoles 14:00-18:00, Viernes 08:00-12:00",
                    "confianza": "media",
                    "metadatos": {"intent": "consultar_horarios", "especialidad": "cardiologia"}
                }
            ]
            
            for log_data in logs_data:
                log = await log_ia_repo.create(db, obj_in=LogIACreate(**log_data))
                print(f"  ✅ Log IA creado")
            
            print("✨ ¡Seed completado exitosamente!")
            print(f"📊 Resumen:")
            print(f"   - {len(clinicas)} clínicas creadas")
            print(f"   - {len(especialidades)} especialidades creadas")
            print(f"   - {len(profesionales)} profesionales creados")
            print(f"   - {len(pacientes)} pacientes creados")
            print(f"   - {len(turnos_data)} turnos creados")
            print(f"   - {len(logs_data)} logs IA creados")
            
        except Exception as e:
            print(f"❌ Error durante el seed: {e}")
            await db.rollback()
            raise
        finally:
            await db.close()


async def main():
    """Función principal para ejecutar el seed"""
    print("🚀 Iniciando proceso de seed...")
    await create_seed_data()
    print("🎉 Proceso de seed finalizado!")


if __name__ == "__main__":
    asyncio.run(main())