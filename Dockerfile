# Dockerfile - Construcción multi-stage para aplicación Flask
# Proyecto Primer Parcial - Gestión de la Configuración del Software
# Universidad de Guayaquil - Grupo D

# Etapa 1: Base con Python
FROM python:3.11-slim as base

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Crear directorio de trabajo
WORKDIR /app

# Etapa 2: Dependencias
FROM base as dependencies

# Copiar archivo de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 3: Aplicación
FROM dependencies as application

# Copiar código de la aplicación
COPY app/ ./app
COPY tests/ ./tests

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Cambiar al usuario no-root
USER appuser

# Exponer puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app.main:app"]
