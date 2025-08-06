# MultiClinicaBot

## Configuración del entorno

1. Crear archivo `.env` con:
```
DATABASE_PG_URL=postgresql+asyncpg://usuario:contraseña@localhost:5432/nombre_db
```

2. Ejecutar migraciones:
```bash
alembic upgrade head
```

3. Crear datos de prueba:
```bash
python seed.py
```