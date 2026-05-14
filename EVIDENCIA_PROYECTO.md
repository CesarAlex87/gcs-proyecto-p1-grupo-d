# Evidencia del Proyecto - Pipeline CI/CD con Jenkins

## Grupo D - Gestión de la Configuración del Software
**Universidad de Guayaquil** | **Prof. Ph.D. Franklin Parrales-Bravo** | **Mayo 2026**

### Integrantes
- Aguilar Villafuerte Daniel Mateo
- Arroba Carrillo Omar Andres
- Ayovi Villafuerte Camillie Thais
- Cordova Viteri Erick Alejandro
- Tipán Antón Cesar Alexander

---

## Entregables Completados

### 1. Repositorio GitHub
- **URL**: https://github.com/CesarAlex87/gcs-proyecto-p1-grupo-d
- **Visibilidad**: Público
- **Rama principal**: master
- **Contenido**:
  - Código fuente Flask (aplicación calculadora)
  - Jenkinsfile (pipeline CI/CD declarativo)
  - Dockerfile (imagen Docker multietapa)
  - docker-compose.yml (orquestación local)
  - tests/ (56 tests unitarios)
  - requirements.txt (dependencias Python)
  - docs/ (documentación técnica)

### 2. Pipeline CI/CD Funcional - Build #4

**Status**: SUCCESS
**Duración**: 43.835 segundos
**Fecha**: 2026-05-14 03:45:34 UTC

#### Etapas Ejecutadas

| Etapa | Estado | Duración | Detalles |
|-------|--------|----------|---------|
| Declarative: Checkout SCM | SUCCESS | 245ms | Inicialización del checkout |
| Checkout | SUCCESS | 1.452s | Descarga del código desde repositorio Git |
| Setup Environment | SUCCESS | 16.142s | Python 3.10.12, virtualenv, instalación de dependencias |
| Lint | SUCCESS | 4.578s | flake8 (0 errores) + pylint (9.05/10) |
| Build | SUCCESS | 11.158s | Tarball + Docker image (gcs-proyecto-p1:4 y :latest) |
| Test | SUCCESS | 1.872s | 56 tests passed, 84% code coverage |
| Deploy | SUCCESS | 6.185s | Docker container, health check HTTP 200 |
| Declarative: Post Actions | SUCCESS | 400ms | Archivado de artefactos |

### 3. Resultados de Tests

- **Total de tests**: 56 passed
- **Fallidos**: 0
- **Cobertura de código**: 84%
- **Detalles por módulo**:
  - app/__init__.py: 100% (0 lines missed)
  - app/calculator.py: 100% (0 lines missed)
  - app/main.py: 81% (13 lines missed)

**Tests incluidos**:
- TestSuma: 6 casos (positivos, negativos, mixtos, cero, decimales)
- TestResta: 6 casos (positivos, negativos, con cero, decimales)
- TestMultiplicacion: 7 casos (positivos, negativos, por cero, fracciones)
- TestDivision: 10 casos (división válida, por cero, decimales, extremos)
- TestCasosExtremos: 3 casos (números grandes, pequeños, precisión flotante)
- TestEndpointRaiz: 2 casos (GET, validación de estructura)
- TestHealthCheck: 2 casos (GET, validación de versión)
- TestCalculadoraSuma: 5 casos (endpoint Flask)
- TestCalculadoraResta: 2 casos (endpoint Flask)
- TestCalculadoraMultiplicacion: 2 casos (endpoint Flask)
- TestCalculadoraDivision: 4 casos (endpoint Flask)
- TestEstudiantes: 3 casos (GET, cantidad, estructura)
- TestErrorHandling: 2 casos (endpoint no existe, parámetros inválidos)
- TestMetodosHTTP: 2 casos (POST, PUT)

### 4. Análisis de Calidad de Código

**flake8**: 0 errores/warnings (max-line-length=120)

**pylint**: 9.05/10
- Warnings aceptados:
  - W0107: Unnecessary pass statement (1 instancia en calculator.py)
  - W0718: Catching broad exceptions (4 instancias en main.py)
  - W0613: Unused arguments (2 instancias en error handlers)

### 5. Docker Build & Deployment

**Imagen construida**: gcs-proyecto-p1:4 (también tagged como :latest)
- **Tamaño**: 203MB
- **Base**: python:3.11-slim
- **Arquitectura**: Multietapa (dependencies → application → final)
- **Usuario no-root**: appuser (UID 1000)
- **Healthcheck**: HTTP GET /health → 200 OK

**Deploy verificado**:
- Container: gcs-proyecto-p1-deploy
- Puerto: 5000
- Health check: HTTP 200
- Respuesta health endpoint: `{"service":"Flask API Calculator","status":"healthy","version":"1.0.0"}`

### 6. Herramientas y Versiones

| Herramienta | Versión |
|-------------|---------|
| Jenkins | Latest LTS (WAR 2.479.3) |
| Java | OpenJDK 21.0.10 |
| Python | 3.10.12 |
| Flask | 3.0.0 |
| Flask-CORS | 4.0.0 |
| pytest | 7.4.3 |
| pytest-cov | 4.1.0 |
| flake8 | 7.3.0 |
| pylint | 4.0.5 |
| gunicorn | 21.2.0 |
| Docker | 29.4.3 |
| Git | 2.34.1 |
| GitHub CLI | 2.92.0 |

### 7. Capturas de Pantalla Disponibles

Las capturas fueron generadas con Playwright y validadas:

1. **01_jenkins_login.png** - Pantalla de login de Jenkins
2. **03_jenkins_manage.png** - Panel Manage Jenkins (configuración del sistema)
3. **04_jenkins_plugins.png** - Lista de plugins instalados
4. **05_pipeline_job.png** - Visualización del job gcs-proyecto-p1
5. **06_pipeline_config.png** - Configuración del pipeline (Jenkinsfile)
6. **07_pipeline_build.png** - Vista del build #4 en progreso/completado
7. **08_console_output.png** - Output de consola del pipeline
8. **09_pipeline_stages.png** - Visualización de etapas con tiempos
9. **11_flask_app_home.png** - Endpoint raíz (/) de la aplicación
10. **12_flask_health.png** - Endpoint health check (/health)
11. **13_flask_students.png** - Endpoint de estudiantes (/students)
12. **14_flask_calculator.png** - Endpoint calculadora (/calculator/suma)

**Ubicación**: `/mnt/d/University/GCS-Proyecto-P1/screenshots/captures/`

### 8. Documentación Generada

#### INFORME_TECNICO.pdf
- **Tamaño**: 77 KB
- **Contenido**:
  - Arquitectura del pipeline CI/CD
  - Flujo de trabajo del Jenkinsfile
  - Herramientas utilizadas
  - Problemas encontrados y soluciones aplicadas
  - Conclusiones y lecciones aprendidas

#### MANUAL_OPERACIONES.pdf
- **Tamaño**: 103 KB
- **Contenido**:
  - Instalación de Jenkins
  - Configuración del pipeline
  - Ejecución manual de builds
  - Interpretación de resultados
  - Screenshots de cada etapa
  - Troubleshooting

### 9. Artefactos Generados por el Pipeline

Todos guardados en `/mnt/d/University/GCS-Proyecto-P1/`:

**Directorio: docs/**
- jenkins_console_build4.txt (699 líneas - salida completa de consola)
- pipeline_stages.json (información de etapas en JSON)
- test_results.txt (resultados detallados de tests)
- INFORME_TECNICO.md (fuente del informe técnico)
- INFORME_TECNICO.pdf (PDF compilado)
- MANUAL_OPERACIONES.md (fuente del manual)
- MANUAL_OPERACIONES.pdf (PDF compilado)

**Directorio: build-artifacts/**
- gcs-proyecto-p1-4.tar.gz (26KB - código compilado)

**Directorio: test-reports/**
- junit.xml (resultados en formato JUnit)
- coverage.xml (cobertura en formato XML)
- test-output.log (salida de tests)
- htmlcov/ (reporte HTML interactivo)

**Directorio: screenshots/captures/**
- 12 capturas PNG de Jenkins y aplicación (resolución 1280x720)

### 10. Estructura del Proyecto

```
/mnt/d/University/GCS-Proyecto-P1/
├── Dockerfile                          # Imagen Docker multietapa
├── Jenkinsfile                         # Pipeline CI/CD declarativo
├── README.md                           # Documentación del proyecto
├── docker-compose.yml                  # Orquestación local
├── requirements.txt                    # Dependencias Python
│
├── app/                                # Código fuente Flask
│   ├── __init__.py
│   ├── main.py                         # Endpoints principales (8 rutas)
│   └── calculator.py                   # Módulo de cálculos (4 operaciones)
│
├── tests/                              # Suite de tests (56 tests)
│   ├── __init__.py
│   ├── test_main.py                    # Tests de endpoints (30 tests)
│   └── test_calculator.py              # Tests de lógica (26 tests)
│
├── docs/                               # Documentación
│   ├── INFORME_TECNICO.md
│   ├── INFORME_TECNICO.pdf
│   ├── MANUAL_OPERACIONES.md
│   ├── MANUAL_OPERACIONES.pdf
│   ├── jenkins_console_build4.txt
│   ├── pipeline_stages.json
│   └── test_results.txt
│
├── build-artifacts/                    # Artefactos compilados
│   └── gcs-proyecto-p1-4.tar.gz
│
├── test-reports/                       # Reportes de tests
│   ├── junit.xml
│   ├── coverage.xml
│   ├── test-output.log
│   └── htmlcov/
│
├── screenshots/                        # Capturas de pantalla
│   ├── README.md
│   ├── capture-jenkins.js
│   ├── capture-pipeline.js
│   ├── capture-webhook.js
│   ├── package.json
│   └── captures/                       # 12 PNG (1280x720)
│
├── venv/                               # Virtual environment
└── EVIDENCIA_PROYECTO.md               # Este archivo
```

### 11. Endpoints API Implementados

**Aplicación Flask (http://localhost:5000)**

| Ruta | Método | Descripción | Parámetros |
|------|--------|-------------|-----------|
| / | GET | Raíz - lista endpoints disponibles | - |
| /health | GET, POST | Health check | - |
| /calculator/suma | GET | Suma de dos números | a, b |
| /calculator/resta | GET | Resta de dos números | a, b |
| /calculator/multiplicacion | GET | Multiplicación | a, b |
| /calculator/division | GET | División (con error handling) | a, b |
| /students | GET | Lista de estudiantes | - |
| /error | GET, PUT | Endpoint para testing de errores HTTP | - |

### 12. Logs y Evidencia Digital

**Jenkins Console Output**:
- Archivo: `/mnt/d/University/GCS-Proyecto-P1/docs/jenkins_console_build4.txt`
- Líneas: 699
- Contiene: Todos los pasos del pipeline con timestamps

**Pipeline Stages (JSON)**:
- Archivo: `/mnt/d/University/GCS-Proyecto-P1/docs/pipeline_stages.json`
- Información: ID de cada etapa, status, duración, timestamps precisos

**Test Coverage Report**:
- HTML interactivo disponible en `/mnt/d/University/GCS-Proyecto-P1/test-reports/htmlcov/`
- XML para CI/CD: `/mnt/d/University/GCS-Proyecto-P1/test-reports/coverage.xml`
- Formato JUnit: `/mnt/d/University/GCS-Proyecto-P1/test-reports/junit.xml`

---

## Resumen de Logros

### Infraestructura CI/CD
- Jenkins local totalmente configurado
- Jenkinsfile limpio y compatible con plugins base
- 8 etapas de pipeline automatizadas
- Ejecución exitosa del build #4

### Calidad de Código
- 0 errores de linting (flake8)
- 9.05/10 en análisis estático (pylint)
- 84% cobertura de código
- 56 tests unitarios pasados

### Containerización
- Docker image construida y testeada
- Dockerfile multietapa optimizado (203MB final)
- Container running con health check exitoso
- Puerto 5000 accesible

### Documentación
- Informe técnico completo (77 KB)
- Manual de operaciones detallado (103 KB)
- 12 capturas de pantalla de evidencia
- Logs completos del pipeline

### Integración
- Código integrado en GitHub (repositorio público)
- Pipeline ejecutado exitosamente
- Docker deploy funcional
- API endpoints operacionales

---

## Pendiente para Completar Entrega Final

- [ ] Grabar video demostrativo (5-10 minutos) mostrando:
  - Interfaz de Jenkins
  - Ejecución del pipeline
  - Output de tests
  - Acceso a endpoints desde navegador
  - Docker container en ejecución
  
- [ ] Subir video a YouTube (con enlace en descripción)

- [ ] Actualizar INFORME_TECNICO.pdf con enlace a video (en sección Demostración)

- [ ] Reemplazar placeholders en MANUAL_OPERACIONES.pdf con las screenshots reales (ya están disponibles en captures/)

---

**Generado**: 2026-05-14
**Versión del Proyecto**: 1.0.0
**Build**: #4 - SUCCESS
