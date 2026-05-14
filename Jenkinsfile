// ============================================================================
// JENKINSFILE - Pipeline CI/CD para Proyecto GCS P1
// Universidad de Guayaquil - Gestión de Configuración de Software
//
// Este pipeline implementa un flujo completo de CI/CD para una aplicación
// Flask en Python, incluyendo: checkout, validación, pruebas, construcción,
// despliegue y notificaciones.
// ============================================================================

pipeline {
    // El agente puede ejecutarse en cualquier nodo disponible del cluster Jenkins
    agent any

    // ========================================================================
    // VARIABLES DE ENTORNO
    // Definición de variables globales accesibles en todas las etapas
    // ========================================================================
    environment {
        // Información del aplicativo
        APP_NAME = 'gcs-proyecto-p1'
        APP_VERSION = '1.0.0'

        // Configuración de Docker
        DOCKER_REGISTRY = 'localhost:5000'
        DOCKER_IMAGE = "${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}"
        DOCKER_IMAGE_LATEST = "${DOCKER_REGISTRY}/${APP_NAME}:latest"

        // Versión de Python requerida
        PYTHON_VERSION = '3.11'

        // Rutas de artefactos y reportes
        COVERAGE_DIR = 'htmlcov'
        TEST_REPORTS_DIR = 'test-reports'
        BUILD_ARTIFACTS_DIR = 'build-artifacts'

        // Configuración de notificaciones
        NOTIFICATION_EMAIL = 'proyecto-gcs@example.com'
        JENKINS_URL = "${env.JENKINS_URL}"
        BUILD_URL = "${env.BUILD_URL}"
    }

    // ========================================================================
    // TRIGGERS - Configuración de activadores del pipeline
    // ========================================================================
    triggers {
        // GitHub Webhook - Se ejecuta automáticamente en cada push a la rama main
        // Configuración en GitHub:
        // 1. Ir a Settings → Webhooks → Add webhook
        // 2. URL: http://<jenkins-server>/github-webhook/
        // 3. Content type: application/json
        // 4. Eventos: Push events (seleccionar ramas: main, develop)
        // 5. Activo: Si
        githubPush()

        // Polling SCM - Fallback si el webhook no funciona
        // Ejecuta cada 15 minutos (H = hash para distribuir carga)
        // pollSCM('H/15 * * * *')
    }

    // ========================================================================
    // OPCIONES - Configuración global del pipeline
    // ========================================================================
    options {
        // Mantener los últimos 30 builds
        buildDiscarder(logRotator(numToKeepStr: '30'))

        // Timeout global de 1 hora
        timeout(time: 1, unit: 'HOURS')

        // Mostrar timestamps en los logs
        timestamps()

        // No ejecutar builds concurrentes del mismo proyecto
        disableConcurrentBuilds()
    }

    // ========================================================================
    // ETAPAS DEL PIPELINE
    // Flujo secuencial de tareas desde checkout hasta despliegue
    // ========================================================================
    stages {
        // ====================================================================
        // ETAPA 1: CHECKOUT
        // Descarga el código fuente del repositorio Git
        // ====================================================================
        stage('Checkout') {
            steps {
                echo '=========================================='
                echo 'ETAPA: CHECKOUT - Descargando código fuente'
                echo '=========================================='

                // Checkout del repositorio con credenciales de GitHub
                checkout(
                    scm: [
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'https://github.com/usuario/gcs-proyecto-p1.git',
                            credentialsId: 'github-credentials'
                        ]]
                    ]
                )

                // Información del commit
                script {
                    env.GIT_COMMIT_MSG = sh(
                        script: "git log -1 --pretty=%B",
                        returnStdout: true
                    ).trim()
                    env.GIT_COMMIT_AUTHOR = sh(
                        script: "git log -1 --pretty=%an",
                        returnStdout: true
                    ).trim()
                    env.GIT_COMMIT_HASH = sh(
                        script: "git log -1 --pretty=%h",
                        returnStdout: true
                    ).trim()
                }

                echo "Commit: ${env.GIT_COMMIT_HASH}"
                echo "Autor: ${env.GIT_COMMIT_AUTHOR}"
                echo "Mensaje: ${env.GIT_COMMIT_MSG}"
            }
        }

        // ====================================================================
        // ETAPA 2: SETUP ENVIRONMENT
        // Configura el entorno: virtualenv, dependencias, etc.
        // ====================================================================
        stage('Setup Environment') {
            steps {
                echo '=========================================='
                echo 'ETAPA: SETUP - Configurando entorno Python'
                echo '=========================================='

                script {
                    try {
                        // Verificar versión de Python
                        sh '''
                            echo "Versión de Python requerida: ${PYTHON_VERSION}"
                            python3 --version
                        '''

                        // Crear y activar ambiente virtual
                        sh '''
                            echo "Creando ambiente virtual..."
                            python3 -m venv venv

                            # Activar virtualenv
                            . venv/bin/activate

                            # Actualizar pip, setuptools y wheel
                            pip install --upgrade pip setuptools wheel

                            # Instalar dependencias del proyecto
                            if [ -f requirements.txt ]; then
                                echo "Instalando dependencias desde requirements.txt..."
                                pip install -r requirements.txt
                            else
                                echo "ADVERTENCIA: requirements.txt no encontrado"
                                exit 1
                            fi

                            # Instalar dependencias de desarrollo para testing
                            pip install pytest pytest-cov flake8 pylint

                            # Mostrar paquetes instalados
                            echo "Paquetes instalados:"
                            pip list
                        '''
                    } catch (Exception e) {
                        echo "ERROR en Setup Environment: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }

        // ====================================================================
        // ETAPA 3: LINT
        // Validación de calidad del código usando flake8 y pylint
        // ====================================================================
        stage('Lint') {
            steps {
                echo '=========================================='
                echo 'ETAPA: LINT - Análisis de calidad del código'
                echo '=========================================='

                script {
                    try {
                        sh '''
                            . venv/bin/activate

                            # Crear directorio para reportes
                            mkdir -p ${TEST_REPORTS_DIR}

                            echo "Ejecutando flake8..."
                            # flake8: Validación de estilo PEP8
                            # --count: Mostrar número de errores
                            # --statistics: Mostrar estadísticas
                            # --max-line-length: Longitud máxima de línea
                            flake8 app/ \
                                --count \
                                --statistics \
                                --max-line-length=120 \
                                --exclude=venv,__pycache__ \
                                --format=json > ${TEST_REPORTS_DIR}/flake8-report.json || true

                            echo "Ejecutando pylint..."
                            # pylint: Análisis estático más profundo
                            # --rcfile: Archivo de configuración
                            # --output-format: Formato de salida
                            pylint app/ \
                                --output-format=json \
                                > ${TEST_REPORTS_DIR}/pylint-report.json || true

                            echo "Análisis de linting completado"
                            echo "Ver reportes en: ${TEST_REPORTS_DIR}/"
                        '''
                    } catch (Exception e) {
                        echo "ADVERTENCIA: Linting encontró problemas: ${e.message}"
                        // No frenamos el pipeline en lint, pero registramos el problema
                    }
                }
            }
        }

        // ====================================================================
        // ETAPA 4: BUILD
        // Construcción de artefactos y imagen Docker
        // ====================================================================
        stage('Build') {
            steps {
                echo '=========================================='
                echo 'ETAPA: BUILD - Construcción de artefactos'
                echo '=========================================='

                script {
                    try {
                        sh '''
                            . venv/bin/activate

                            # Crear directorio de artefactos
                            mkdir -p ${BUILD_ARTIFACTS_DIR}

                            echo "Preparando aplicación para build..."

                            # Limpiar cachés y archivos compilados
                            find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
                            find . -type f -name "*.pyc" -delete
                            find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

                            # Crear archivo de versión
                            echo "{
                              \"version\": \"${APP_VERSION}\",
                              \"build_number\": \"${BUILD_NUMBER}\",
                              \"commit\": \"${GIT_COMMIT_HASH}\",
                              \"build_date\": \"$(date -u '+%Y-%m-%dT%H:%M:%SZ')\"
                            }" > app/version.json

                            echo "Archivo de versión creado: app/version.json"

                            # Empaquetar la aplicación
                            echo "Creando paquete tarball..."
                            tar -czf ${BUILD_ARTIFACTS_DIR}/${APP_NAME}-${BUILD_NUMBER}.tar.gz \
                                --exclude=venv \
                                --exclude=.git \
                                --exclude=__pycache__ \
                                --exclude="*.pyc" \
                                .

                            ls -lh ${BUILD_ARTIFACTS_DIR}/
                            echo "Build completado exitosamente"
                        '''

                        // Construir imagen Docker
                        echo "Construyendo imagen Docker: ${DOCKER_IMAGE}"
                        sh '''
                            . venv/bin/activate

                            # Verificar que existe Dockerfile
                            if [ ! -f Dockerfile ]; then
                                echo "ERROR: Dockerfile no encontrado en la raíz del proyecto"
                                exit 1
                            fi

                            echo "Docker build iniciado..."
                            docker build \
                                --tag ${DOCKER_IMAGE} \
                                --tag ${DOCKER_IMAGE_LATEST} \
                                --build-arg BUILD_NUMBER=${BUILD_NUMBER} \
                                --build-arg GIT_COMMIT=${GIT_COMMIT_HASH} \
                                --build-arg BUILD_DATE="$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
                                .

                            echo "Imagen Docker construida: ${DOCKER_IMAGE}"
                            docker images | grep ${APP_NAME}
                        '''

                    } catch (Exception e) {
                        echo "ERROR en Build: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }

        // ====================================================================
        // ETAPA 5: TEST
        // Ejecución de pruebas unitarias, integración y cobertura
        // ====================================================================
        stage('Test') {
            steps {
                echo '=========================================='
                echo 'ETAPA: TEST - Ejecución de pruebas'
                echo '=========================================='

                script {
                    try {
                        sh '''
                            . venv/bin/activate

                            # Crear directorio para reportes de test
                            mkdir -p ${TEST_REPORTS_DIR}

                            echo "Ejecutando pytest con cobertura..."
                            # pytest: Framework de testing
                            # --cov: Generar reporte de cobertura
                            # --cov-report: Formatos de reporte
                            # --junitxml: Formato JUnit XML para Jenkins
                            # -v: Modo verbose
                            pytest \
                                --cov=app \
                                --cov-report=term \
                                --cov-report=html:${COVERAGE_DIR} \
                                --cov-report=xml:${TEST_REPORTS_DIR}/coverage.xml \
                                --junitxml=${TEST_REPORTS_DIR}/junit.xml \
                                -v \
                                --tb=short \
                                tests/ 2>&1 | tee ${TEST_REPORTS_DIR}/test-output.log

                            # Verificar cobertura mínima (70%)
                            echo "Verificando cobertura de código..."
                            coverage report --fail-under=70 || {
                                echo "ADVERTENCIA: Cobertura por debajo del 70%"
                            }

                            echo "Pruebas completadas"
                        '''
                    } catch (Exception e) {
                        echo "ERROR en Test: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }

            post {
                always {
                    // Publicar reportes de pruebas JUnit
                    junit testResults: "${TEST_REPORTS_DIR}/*.xml",
                          allowEmptyResults: true

                    // Publicar reporte de cobertura
                    publishHTML(
                        reportDir: "${COVERAGE_DIR}",
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    )

                    // Publicar reporte de linting si existe
                    script {
                        if (fileExists("${TEST_REPORTS_DIR}/flake8-report.json")) {
                            archiveArtifacts artifacts: "${TEST_REPORTS_DIR}/*.json",
                                           allowEmptyArchive: true
                        }
                    }
                }
            }
        }

        // ====================================================================
        // ETAPA 6: DEPLOY
        // Despliegue de la aplicación usando Docker Compose
        // ====================================================================
        stage('Deploy') {
            // Solo desplegar en rama main y build exitosos
            when {
                branch 'main'
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }

            steps {
                echo '=========================================='
                echo 'ETAPA: DEPLOY - Despliegue de la aplicación'
                echo '=========================================='

                script {
                    try {
                        sh '''
                            echo "Preparando despliegue con Docker Compose..."

                            # Verificar que existe docker-compose.yml
                            if [ ! -f docker-compose.yml ]; then
                                echo "ERROR: docker-compose.yml no encontrado"
                                exit 1
                            fi

                            # Detener contenedores antiguos
                            echo "Deteniendo contenedores previos..."
                            docker-compose down || true

                            # Actualizar variables de entorno
                            echo "Configurando variables de entorno..."
                            cat > .env << EOF
                            APP_NAME=${APP_NAME}
                            DOCKER_IMAGE=${DOCKER_IMAGE}
                            ENVIRONMENT=production
                            LOG_LEVEL=INFO
EOF

                            # Iniciar nuevos contenedores
                            echo "Iniciando contenedores con Docker Compose..."
                            docker-compose up -d

                            # Esperar a que la aplicación inicie
                            echo "Esperando que la aplicación inicie..."
                            sleep 5

                            # Mostrar estado de contenedores
                            echo "Estado de contenedores:"
                            docker-compose ps

                            # Verificar logs
                            echo "Últimos logs:"
                            docker-compose logs --tail=20
                        '''

                        // Health check
                        echo "Ejecutando health check..."
                        sh '''
                            MAX_ATTEMPTS=10
                            ATTEMPT=0
                            HEALTH_CHECK_URL="http://localhost:5000/health"

                            while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
                                echo "Health check intento $((ATTEMPT+1))/$MAX_ATTEMPTS"

                                HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_CHECK_URL || echo "000")

                                if [ "$HTTP_CODE" = "200" ]; then
                                    echo "✓ Health check exitoso (HTTP $HTTP_CODE)"
                                    exit 0
                                else
                                    echo "✗ Health check falló (HTTP $HTTP_CODE), reintentando..."
                                    sleep 3
                                    ATTEMPT=$((ATTEMPT+1))
                                fi
                            done

                            echo "ERROR: Health check falló después de $MAX_ATTEMPTS intentos"
                            exit 1
                        '''

                    } catch (Exception e) {
                        echo "ERROR en Deploy: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }
    }

    // ========================================================================
    // POST - Acciones posteriores a la ejecución del pipeline
    // ========================================================================
    post {
        always {
            echo '=========================================='
            echo 'POST: Acciones finales (siempre se ejecutan)'
            echo '=========================================='

            // Limpiar workspace opcional (comentado por defecto)
            // cleanWs()

            // Archivar artefactos importantes
            script {
                sh '''
                    echo "Archivando artefactos..."

                    # Archivar reportes de pruebas
                    if [ -d ${TEST_REPORTS_DIR} ]; then
                        echo "Archivando reportes de test..."
                    fi

                    # Archivar logs
                    if [ -f ${TEST_REPORTS_DIR}/test-output.log ]; then
                        echo "Logs de pruebas archivados"
                    fi
                '''
            }

            // Archivar artifacts
            archiveArtifacts artifacts: "${BUILD_ARTIFACTS_DIR}/**",
                            allowEmptyArchive: true

            // Archivar logs del test
            archiveArtifacts artifacts: "${TEST_REPORTS_DIR}/**",
                            allowEmptyArchive: true
        }

        success {
            echo '=========================================='
            echo 'POST: BUILD EXITOSO'
            echo '=========================================='

            // Notificación de éxito por email
            emailext(
                subject: "✓ Build Exitoso: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: '''
                    <h2>Build Exitoso</h2>
                    <p><strong>Proyecto:</strong> ${JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
                    <p><strong>Rama:</strong> main</p>
                    <p><strong>Commit:</strong> ${GIT_COMMIT_HASH}</p>
                    <p><strong>Autor:</strong> ${GIT_COMMIT_AUTHOR}</p>
                    <p><strong>Duración:</strong> ${BUILD_DURATION}</p>

                    <h3>Reportes</h3>
                    <ul>
                        <li><a href="${BUILD_URL}Coverage_Report">Coverage Report</a></li>
                        <li><a href="${BUILD_URL}testReport">Test Report</a></li>
                    </ul>

                    <p><a href="${BUILD_URL}">Ver en Jenkins</a></p>
                ''',
                to: "${NOTIFICATION_EMAIL}",
                mimeType: 'text/html'
            )

            script {
                currentBuild.result = 'SUCCESS'
            }
        }

        failure {
            echo '=========================================='
            echo 'POST: BUILD FALLIDO'
            echo '=========================================='

            // Notificación de fallo por email
            emailext(
                subject: "✗ Build Fallido: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: '''
                    <h2>Build Fallido</h2>
                    <p><strong>Proyecto:</strong> ${JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
                    <p><strong>Rama:</strong> main</p>
                    <p><strong>Commit:</strong> ${GIT_COMMIT_HASH}</p>
                    <p><strong>Autor:</strong> ${GIT_COMMIT_AUTHOR}</p>
                    <p><strong>Mensaje:</strong> ${GIT_COMMIT_MSG}</p>

                    <h3>Información del Error</h3>
                    <p>Por favor, revise los logs para más detalles.</p>

                    <h3>Reportes</h3>
                    <ul>
                        <li><a href="${BUILD_URL}testReport">Test Report</a></li>
                        <li><a href="${BUILD_URL}console">Build Log</a></li>
                    </ul>

                    <p><a href="${BUILD_URL}">Ver en Jenkins</a></p>
                ''',
                to: "${NOTIFICATION_EMAIL}",
                mimeType: 'text/html'
            )

            // Detener y limpiar contenedores en caso de fallo
            sh '''
                echo "Limpiando contenedores por fallo en deploy..."
                docker-compose down || true
            '''

            script {
                currentBuild.result = 'FAILURE'
            }
        }

        unstable {
            echo '=========================================='
            echo 'POST: BUILD INESTABLE (Problemas en tests)'
            echo '=========================================='

            emailext(
                subject: "⚠ Build Inestable: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "El build se completó pero hay problemas en los tests.\n\nVer detalles en: ${BUILD_URL}",
                to: "${NOTIFICATION_EMAIL}"
            )
        }

        cleanup {
            echo 'POST: Limpieza final'
            // Limpiar archivos temporales si es necesario
        }
    }
}

// ============================================================================
// CONFIGURACIÓN DE GITHUB WEBHOOK
// Instrucciones para configurar el webhook en GitHub:
// ============================================================================
//
// 1. HABILITAR PLUGIN DE GITHUB EN JENKINS:
//    - Manage Jenkins → Plugins → Buscar "GitHub Integration"
//    - Instalar "GitHub Integration" y "GitHub Plugin"
//    - Restart Jenkins si es necesario
//
// 2. CONFIGURAR CREDENCIALES DE GITHUB EN JENKINS:
//    - Ir a: Manage Jenkins → Credentials → Global Credentials
//    - New Credentials:
//      * Kind: Username with password
//      * Username: <github-user>
//      * Password: <github-personal-access-token>
//      * ID: github-credentials
//    - O usar SSH keys (recomendado para producción)
//
// 3. CREAR O CONFIGURAR EL JOB EN JENKINS:
//    - New Item → Pipeline
//    - Definition: Pipeline script from SCM
//    - SCM: Git
//    - Repository URL: https://github.com/usuario/gcs-proyecto-p1.git
//    - Credentials: github-credentials
//    - Script Path: Jenkinsfile
//
// 4. CONFIGURAR EL WEBHOOK EN GITHUB:
//    - Ir al repositorio: https://github.com/usuario/gcs-proyecto-p1
//    - Settings → Webhooks → Add webhook
//    - Payload URL: http://<jenkins-server>/github-webhook/
//      Ejemplo: http://jenkins.ejemplo.com/github-webhook/
//    - Content type: application/json
//    - Which events would you like to trigger this webhook?
//      ✓ Push events
//      ✓ Pull request events (opcional)
//    - Active: ✓ (marcado)
//    - Add webhook
//
// 5. VERIFICAR LA CONFIGURACIÓN:
//    - En GitHub, ir a Settings → Webhooks
//    - Ver las entregas recientes (Recent Deliveries)
//    - Status verde (200) indica éxito
//    - Status rojo indica error (revisar logs en Jenkins)
//
// 6. ALTERNATIVA: USAR GITHUB PERSONAL ACCESS TOKEN:
//    - En Jenkins, instalar "GitHub Branch Source Plugin"
//    - Manage Jenkins → Credentials → Add Credentials
//    - Kind: GitHub App or Personal Access Token
//    - Scope: Usar token con permisos: repo, admin:repo_hook, admin:org_hook
//
// 7. PARA TESTING DEL WEBHOOK SIN COMMITS:
//    - En GitHub Webhooks, buscar la entrega más reciente
//    - Hacer clic en "Redeliver" para reenviar el evento
//    - Verificar que Jenkins dispara el build
//
// ============================================================================
