import pytest
import pytest_asyncio
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.responses import ( ClinicaResponse, PacienteResponse,ProfesionalResponse,EspecialidadResponse,TurnoResponse, LogIAResponse)
from app.config.database import AsyncSessionLocal, engine, Base
from app.repositories.repositories import (
    clinica_repo, paciente_repo, profesional_repo,
    especialidad_repo, turno_repo, log_ia_repo,
    ClinicaCreate, ClinicaUpdate,
    PacienteCreate, PacienteUpdate,
    ProfesionalCreate, ProfesionalUpdate, 
    EspecialidadCreate, EspecialidadUpdate, 
    TurnoCreate, TurnoUpdate, LogIAUpdate,
    LogIACreate
)

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def setup_database():
    """Setup test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session(setup_database):
    """Provide a database session for tests"""
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def clinica(db_session: AsyncSession):
    """Fixture para crear una clínica reutilizable"""
    clinica_data = ClinicaCreate(
        nombre="Clínica Test",
        did_whatsapp="123456789",
        activa=True,
        configuraciones={"horario": "8-18"}
    )
    async with db_session.begin():
        clinica = await clinica_repo.create(db_session, obj_in=clinica_data)
    return clinica

@pytest_asyncio.fixture
async def paciente(db_session: AsyncSession):
    """Fixture para crear un paciente reutilizable"""
    paciente_data = PacienteCreate(
        dni="12345678",
        telefono="1234567890",
        nombre="Juan Test",
        email="juan@test.com"
    )
    async with db_session.begin():
        paciente = await paciente_repo.create(db_session, obj_in=paciente_data)
    return paciente

@pytest_asyncio.fixture
async def profesional(db_session: AsyncSession):
    """Fixture para crear un profesional reutilizable"""
    profesional_data = ProfesionalCreate(
        nombre="Dr. Test",
        activo=True,
        especialidades=["Cardiología"]
    )
    async with db_session.begin():
        profesional = await profesional_repo.create(db_session, obj_in=profesional_data)
    return profesional

@pytest_asyncio.fixture
async def especialidad(db_session: AsyncSession):
    """Fixture para crear una especialidad reutilizable"""
    especialidad_data = EspecialidadCreate(
        nombre="Cardiología",
        descripcion="Especialidad de corazón"
    )
    async with db_session.begin():
        especialidad = await especialidad_repo.create(db_session, obj_in=especialidad_data)
    return especialidad

class TestClinicaRepository:
    """Tests para el repositorio de Clínica"""
    
    async def test_create_clinica(self, db_session: AsyncSession):
        """Test crear clínica"""
        clinica_data = ClinicaCreate(
            nombre="Clínica Test",
            configuraciones={"horario": "8-18"},
            did_whatsapp="123456789",
            activa=True
        )
        async with db_session.begin():
            clinica = await clinica_repo.create(db_session, obj_in=clinica_data)
        
        assert clinica.id is not None
        assert clinica.nombre == "Clínica Test"
        assert clinica.did_whatsapp == "123456789"
        assert clinica.activa is True
        assert clinica.configuraciones == {"horario": "8-18"}
    
    async def test_get_clinica(self, db_session: AsyncSession, clinica: ClinicaResponse):
        """Test obtener clínica por ID"""
        async with db_session.begin():
            retrieved_clinica = await clinica_repo.get(db_session, clinica.id)
        
        assert retrieved_clinica is not None
        assert retrieved_clinica.id == clinica.id
        assert retrieved_clinica.nombre == clinica.nombre
    
    async def test_get_by_whatsapp_did(self, db_session: AsyncSession, clinica: ClinicaResponse):
        """Test obtener clínica por DID de WhatsApp"""
        async with db_session.begin():
            retrieved_clinica = await clinica_repo.get_by_whatsapp_did(db_session, did_whatsapp=clinica.did_whatsapp)
        
        assert retrieved_clinica is not None
        assert retrieved_clinica.id == clinica.id
        assert retrieved_clinica.did_whatsapp == clinica.did_whatsapp
    
    async def test_get_active_clinics(self, db_session: AsyncSession):
        """Test obtener solo clínicas activas"""
        async with db_session.begin():
            await clinica_repo.create(
                db_session, 
                obj_in=ClinicaCreate(nombre="Inactiva", did_whatsapp="222", activa=False)
            )
            active_clinics = await clinica_repo.get_active_clinics(db_session)
        
        assert len(active_clinics) >= 1
        assert all(clinica.activa for clinica in active_clinics)

class TestPacienteRepository:
    """Tests para el repositorio de Paciente"""
    
    async def test_create_paciente(self, db_session: AsyncSession):
        """Test crear paciente"""
        paciente_data = PacienteCreate(
            dni="87654321",
            telefono="9876543210",
            nombre="María Test",
            email="maria@test.com"
        )
        async with db_session.begin():
            paciente = await paciente_repo.create(db_session, obj_in=paciente_data)
        
        assert paciente.id is not None
        assert paciente.dni == "87654321"
        assert paciente.nombre == "María Test"
        assert paciente.email == "maria@test.com"
    
    async def test_get_by_dni(self, db_session: AsyncSession, paciente: PacienteResponse, clinica: ClinicaResponse):
        """Test obtener paciente por DNI, con y sin clínica"""
        async with db_session.begin():
            profesional = await profesional_repo.create(
                db_session, 
                obj_in=ProfesionalCreate(nombre="Dr. Turno", activo=True)
            )
            turno_data = TurnoCreate(
                id_paciente=paciente.id,
                id_profesional=profesional.id,
                id_clinica=clinica.id,
                fecha_hora=datetime.now() + timedelta(days=1),
                estado="programado"
            )
            await turno_repo.create(db_session, obj_in=turno_data)
            
            # Buscar sin clínica
            found_paciente = await paciente_repo.get_by_dni(db_session, dni=paciente.dni)
            assert found_paciente is not None
            assert found_paciente.id == paciente.id
            assert found_paciente.dni == paciente.dni
            
            # Buscar con clínica
            found_paciente = await paciente_repo.get_by_dni(db_session, dni=paciente.dni, id_clinica=clinica.id)
            assert found_paciente is not None
            assert found_paciente.id == paciente.id

class TestProfesionalRepository:
    """Tests para el repositorio de Profesional"""
    
    async def test_create_profesional(self, db_session: AsyncSession, especialidad: EspecialidadResponse):
        """Test crear profesional con especialidad válida"""
        profesional_data = ProfesionalCreate(
            nombre="Dr. Especialista",
            especialidades=[especialidad.nombre],
            activo=True
        )
        async with db_session.begin():
            profesional = await profesional_repo.create(db_session, obj_in=profesional_data)
        
        assert profesional.id is not None
        assert profesional.nombre == "Dr. Especialista"
        assert profesional.especialidades == [especialidad.nombre]
    
    async def test_create_profesional_invalid_especialidad(self, db_session: AsyncSession):
        """Test crear profesional con especialidad inválida"""
        profesional_data = ProfesionalCreate(
            nombre="Dr. Inválido",
            especialidades=["No Existe"],
            activo=True
        )
        with pytest.raises(ValueError, match="Especialidad No Existe no existe"):
            async with db_session.begin():
                await profesional_repo.create(db_session, obj_in=profesional_data)

class TestEspecialidadRepository:
    """Tests para el repositorio de Especialidad"""
    
    async def test_create_especialidad(self, db_session: AsyncSession):
        """Test crear especialidad"""
        especialidad_data = EspecialidadCreate(
            nombre="Neurología",
            descripcion="Especialidad neurológica"
        )
        async with db_session.begin():
            especialidad = await especialidad_repo.create(db_session, obj_in=especialidad_data)
        
        assert especialidad.id is not None
        assert especialidad.nombre == "Neurología"
        assert especialidad.descripcion == "Especialidad neurológica"
    
    async def test_get_by_nombre(self, db_session: AsyncSession, especialidad: EspecialidadResponse):
        """Test obtener especialidad por nombre"""
        async with db_session.begin():
            found_especialidad = await especialidad_repo.get_by_nombre(db_session, nombre=especialidad.nombre)
        
        assert found_especialidad is not None
        assert found_especialidad.id == especialidad.id
        assert found_especialidad.nombre == especialidad.nombre

class TestTurnoRepository:
    """Tests para el repositorio de Turno"""
    
    async def test_create_turno(self, db_session: AsyncSession, clinica: ClinicaResponse, paciente: PacienteResponse, profesional: ProfesionalResponse):
        """Test crear turno"""
        turno_data = TurnoCreate(
            id_paciente=paciente.id,
            id_profesional=profesional.id,
            id_clinica=clinica.id,
            fecha_hora=datetime.now() + timedelta(days=1),
            estado="programado"
        )
        async with db_session.begin():
            turno = await turno_repo.create(db_session, obj_in=turno_data)
        
        assert turno.id is not None
        assert turno.id_paciente == paciente.id
        assert turno.id_profesional == profesional.id
        assert turno.id_clinica == clinica.id
        assert turno.estado == "programado"
    
    async def test_get_by_paciente(self, db_session: AsyncSession, clinica: ClinicaResponse, paciente: PacienteResponse, profesional: ProfesionalResponse):
        """Test obtener turnos por paciente"""
        turno_data = TurnoCreate(
            id_paciente=paciente.id,
            id_profesional=profesional.id,
            id_clinica=clinica.id,
            fecha_hora=datetime.now() + timedelta(days=1),
            estado="programado"
        )
        async with db_session.begin():
            await turno_repo.create(db_session, obj_in=turno_data)
            turnos = await turno_repo.get_by_paciente(db_session, id_paciente=paciente.id)
        
        assert len(turnos) >= 1
        assert all(turno.id_paciente == paciente.id for turno in turnos)

class TestLogIARepository:
    """Tests para el repositorio de LogIA"""
    
    async def test_create_log_ia(self, db_session: AsyncSession):
        """Test crear log IA"""
        log_data = LogIACreate(
            mensaje="Consulta test",
            respuesta_ia="Respuesta IA test",
            confianza="alta",
            metadatos={"origen": "test"}
        )
        async with db_session.begin():
            log = await log_ia_repo.create(db_session, obj_in=log_data)
        
        assert log.id is not None
        assert log.mensaje == "Consulta test"
        assert log.respuesta_ia == "Respuesta IA test"
        assert log.confianza == "alta"
        assert log.metadatos == {"origen": "test"}

class TestCRUDOperations:
    """Tests para operaciones CRUD generales"""
    
    async def test_update_clinica(self, db_session: AsyncSession, clinica: ClinicaResponse):
        """Test actualizar clínica"""
        update_data = ClinicaUpdate(nombre="Actualizada", activa=False)
        async with db_session.begin():
            updated_clinica = await clinica_repo.update(db_session, db_obj=clinica, obj_in=update_data)
        
        assert updated_clinica.nombre == "Actualizada"
        assert updated_clinica.activa is False
        assert updated_clinica.did_whatsapp == clinica.did_whatsapp
    
    async def test_delete_clinica(self, db_session: AsyncSession, clinica: ClinicaResponse):
        """Test eliminar clínica"""
        clinica_id = clinica.id
        async with db_session.begin():
            deleted_clinica = await clinica_repo.delete(db_session, id=clinica_id)
        
        assert deleted_clinica is not None
        assert deleted_clinica.id == clinica_id
        
        async with db_session.begin():
            not_found = await clinica_repo.get(db_session, clinica_id)
        assert not_found is None
    
    async def test_get_multi_with_filters(self, db_session: AsyncSession):
        """Test obtener múltiples registros con filtros"""
        async with db_session.begin():
            await clinica_repo.create(
                db_session, 
                obj_in=ClinicaCreate(nombre="Inactiva 1", did_whatsapp="999", activa=False, configuraciones={})
            )
            active_clinics = await clinica_repo.get_multi(db_session, filters={"activa": True})
        
        assert len(active_clinics) >= 1
        assert all(clinica.activa for clinica in active_clinics)
        
        async with db_session.begin():
            total_count = await clinica_repo.get_count(db_session)
        assert total_count >= 2

if __name__ == "__main__":
    pytest.main([__file__])