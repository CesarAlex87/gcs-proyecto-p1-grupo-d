# Proyecto Primer Parcial - Gestión de la Configuración del Software

## Información del Curso

**Cátedra:** Gestión de la Configuración del Software  
**Profesor:** Ph.D. Franklin Parrales-Bravo  
**Universidad:** Universidad de Guayaquil  
**Grupo:** D  
**Periodo:** Primer Parcial

## Integrantes del Grupo D

1. **Aguilar Villafuerte Daniel Mateo**
2. **Arroba Carrillo Omar Andres**
3. **Ayovi Villafuerte Camillie Thais**
4. **Cordova Viteri Erick Alejandro**
5. **Tipán Antón Cesar Alexander**

## Descripción del Proyecto

Este proyecto es una aplicación Flask que implementa una **API REST de Calculadora** con **integración CI/CD mediante Jenkins**. El objetivo es demostrar las mejores prácticas de gestión de configuración del software, incluyendo:

- **Versionamiento de código** con Git
- **Desarrollo con ramificaciones** (Git Flow)
- **Testing automático** (Unitarias e Integración)
- **Construcción automática** con Docker
- **Pipeline CI/CD** con Jenkins
- **Integración continua** y **Entrega continua**

## Características

### API REST

La aplicación expone los siguientes endpoints:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información del proyecto |
| `GET` | `/health` | Verificación de salud del servicio |
| `GET` | `/api/calculator/add?a=X&b=Y` | Suma de dos números |
| `GET` | `/api/calculator/subtract?a=X&b=Y` | Resta de dos números |
| `GET` | `/api/calculator/multiply?a=X&b=Y` | Multiplicación de dos números |
| `GET` | `/api/calculator/divide?a=X&b=Y` | División de dos números |
| `GET` | `/api/students` | Lista de estudiantes del Grupo D |

### Pruebas

El proyecto incluye:

- **10+ pruebas unitarias** en `tests/test_calculator.py` para el módulo calculadora
- **8+ pruebas de integración** en `tests/test_main.py` para los endpoints Flask
- **Cobertura de código** con pytest-cov
- **Manejo de casos extremos** (división por cero, valores negros, decimales, etc.)

### Docker

- **Dockerfile multi-stage** para optimización de imágenes
- **docker-compose.yml** para orquestación de contenedores
- **Health check** automático

## Tecnologías Utilizadas

- **Python 3.11**
- **Flask 3.0.0** - Framework web
- **Flask-CORS 4.0.0** - Control de CORS
- **pytest 7.4.3** - Framework de pruebas
- **pytest-cov 4.1.0** - Cobertura de pruebas
- **gunicorn 21.2.0** - Servidor WSGI de producción
- **Docker** - Containerización
- **Docker Compose** - Orquestación

## Estructura del Proyecto

```
GCS-Proyecto-P1/
├── app/
│   ├── __init__.py          # Inicializador del paquete
│   ├── main.py              # Aplicación Flask y endpoints
│   └── calculator.py        # Módulo de operaciones matemáticas
├── tests/
│   ├── __init__.py          # Inicializador del paquete
│   ├── test_calculator.py   # Pruebas unitarias
│   └── test_main.py         # Pruebas de integración
├── requirements.txt         # Dependencias de Python
├── Dockerfile               # Configuración Docker
├── docker-compose.yml       # Configuración Docker Compose
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## Instalación

### Requisitos Previos

- Python 3.11+
- pip (gestor de paquetes de Python)
- Docker y Docker Compose (opcional)

### Setup Local

1. **Clonar el repositorio:**
```bash
git clone <url-del-repositorio>
cd GCS-Proyecto-P1
```

2. **Crear un entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## Ejecución

### Ejecutar la Aplicación

**Modo desarrollo:**
```bash
python -m flask --app app.main run --host 0.0.0.0 --port 5000
```

**Modo producción con gunicorn:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app.main:app
```

La aplicación estará disponible en `http://localhost:5000`

### Con Docker

**Construir la imagen:**
```bash
docker build -t gcs-proyecto-p1:latest .
```

**Ejecutar el contenedor:**
```bash
docker run -p 5000:5000 gcs-proyecto-p1:latest
```

**Usar docker-compose:**
```bash
docker-compose up -d
```

## Pruebas

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar pruebas con salida detallada

```bash
pytest -v
```

### Ejecutar pruebas con cobertura

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

Esto generará un reporte de cobertura en `htmlcov/index.html`

### Ejecutar solo pruebas unitarias

```bash
pytest tests/test_calculator.py -v
```

### Ejecutar solo pruebas de integración

```bash
pytest tests/test_main.py -v
```

## Ejemplos de Uso

### GET /health
```bash
curl http://localhost:5000/health
```

Respuesta:
```json
{
  "status": "healthy",
  "service": "Flask API Calculator",
  "version": "1.0.0"
}
```

### GET /api/calculator/add
```bash
curl "http://localhost:5000/api/calculator/add?a=5&b=3"
```

Respuesta:
```json
{
  "operacion": "suma",
  "a": 5,
  "b": 3,
  "resultado": 8
}
```

### GET /api/calculator/divide
```bash
curl "http://localhost:5000/api/calculator/divide?a=10&b=2"
```

Respuesta:
```json
{
  "operacion": "division",
  "a": 10,
  "b": 2,
  "resultado": 5.0
}
```

### GET /api/students
```bash
curl http://localhost:5000/api/students
```

Respuesta:
```json
{
  "grupo": "D",
  "cantidad": 5,
  "estudiantes": [
    {
      "id": 1,
      "nombre": "Aguilar Villafuerte Daniel Mateo",
      "carrera": "Ingeniería en Sistemas Computacionales"
    },
    ...
  ],
  "universidad": "Universidad de Guayaquil",
  "carrera": "Ingeniería en Sistemas Computacionales"
}
```

## Pipeline CI/CD con Jenkins

### Etapas del Pipeline

1. **Stage: Checkout** - Obtener código del repositorio Git
2. **Stage: Install Dependencies** - Instalar dependencias con pip
3. **Stage: Unit Tests** - Ejecutar pruebas unitarias
4. **Stage: Integration Tests** - Ejecutar pruebas de integración
5. **Stage: Code Coverage** - Calcular y reportar cobertura
6. **Stage: Build** - Construir imagen Docker
7. **Stage: Deploy** - Desplegar en ambiente (desarrollo/producción)

### Configuración del Jenkins

El archivo `Jenkinsfile` (si está presente) define el pipeline automático.

Requisitos en Jenkins:
- Plugin de Docker
- Plugin de Git
- Plugin de Pipeline
- Plugin de Cobertura

## Mejores Prácticas Implementadas

### Código
- ✅ Type hints en Python
- ✅ Documentación en docstrings (español)
- ✅ Manejo de excepciones personalizado
- ✅ Separación de responsabilidades

### Testing
- ✅ Pruebas unitarias exhaustivas
- ✅ Pruebas de integración
- ✅ Casos extremos (edge cases)
- ✅ Cobertura de código >= 80%

### DevOps
- ✅ Dockerfile multi-stage
- ✅ Docker Compose para desarrollo
- ✅ Health checks
- ✅ Archivo .gitignore completo

### Git
- ✅ Commits descriptivos
- ✅ Versionamiento semántico
- ✅ Ramificaciones organizadas

## Resolución de Problemas

### Error: ModuleNotFoundError: No module named 'flask'
**Solución:** Ejecutar `pip install -r requirements.txt`

### Error: Port 5000 already in use
**Solución:** Cambiar el puerto con `--port 8000` o detener el proceso usando el puerto

### Las pruebas fallan localmente
**Solución:** Verificar que Flask esté en testing mode y que todas las dependencias estén instaladas

## Contribución

Para contribuir al proyecto:

1. Crear una rama desde `develop`: `git checkout -b feature/nueva-funcionalidad`
2. Realizar cambios y commits descriptivos
3. Ejecutar pruebas: `pytest`
4. Crear un Pull Request

## Licencia

Este proyecto es parte del curso de Gestión de la Configuración del Software de la Universidad de Guayaquil.

## Contacto

Para preguntas o sugerencias, contactar a los integrantes del Grupo D.

---

**Actualizado:** 2026-05-13  
**Versión:** 1.0.0
