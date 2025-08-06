from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base
from datetime import datetime
from typing import Optional


class Clinica(Base):
    __tablename__ = "clinicas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    configuraciones = Column(JSON, nullable=True)  # JSONB para configuraciones
    did_whatsapp = Column(String(50), unique=True, index=True)
    activa = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())        


class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String(20), nullable=False, index=True)
    telefono = Column(String(20), nullable=False, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True)    
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones    
    turnos = relationship("Turno", back_populates="paciente", cascade="all, delete-orphan")
    
    # Índices compuestos
    __table_args__ = (
        Index('idx_paciente_dni', 'dni'),
        Index('idx_paciente_telefono', 'telefono'),
    )


class Profesional(Base):
    __tablename__ = "profesionales"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    especialidades = Column(JSON, nullable=True)  # JSONB para especialidades
    horarios = Column(JSON, nullable=True)  # JSONB para horarios    
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
        
    turnos = relationship("Turno", back_populates="profesional", cascade="all, delete-orphan")


class Especialidad(Base):
    __tablename__ = "especialidades"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    preparacion_previa = Column(Text, nullable=True)    
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
        
    # Índice compuesto
    __table_args__ = (
        Index('idx_especialidad_nombre', 'nombre'),
    )


class Turno(Base):
    __tablename__ = "turnos"
    
    id = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    id_profesional = Column(Integer, ForeignKey("profesionales.id"), nullable=False)
    id_clinica = Column(Integer, ForeignKey("clinicas.id"), nullable=False)    
    fecha_hora = Column(DateTime(timezone=True), nullable=False, index=True)
    estado = Column(String(50), nullable=False, default="programado", index=True)  # programado, confirmado, cancelado, completado
    observaciones = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="turnos")
    profesional = relationship("Profesional", back_populates="turnos")
    clinica = relationship("Clinica")    

    # Índices compuestos
    __table_args__ = (
        Index('idx_turno_fecha_profesional', 'fecha_hora', 'id_profesional'),
        Index('idx_turno_paciente_fecha', 'id_paciente', 'fecha_hora'),
        Index('idx_turno_estado_fecha', 'estado', 'fecha_hora'),
        Index('idx_turno_clinica_fecha', 'id_clinica', 'fecha_hora'),        
    )


class LogIA(Base):
    __tablename__ = "logs_ia"
    
    id = Column(Integer, primary_key=True, index=True)
    mensaje = Column(Text, nullable=False)
    respuesta_ia = Column(Text, nullable=False)
    confianza = Column(String(20), nullable=True)  # baja, media, alta
    fecha = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    metadatos = Column(JSON, nullable=True)  # JSONB para metadata adicional
    
    # Índices
    __table_args__ = (
        Index('idx_log_fecha_confianza', 'fecha', 'confianza'),
    )