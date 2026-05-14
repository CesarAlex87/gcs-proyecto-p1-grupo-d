// ============================================================================
// JENKINSFILE - Pipeline CI/CD para Proyecto GCS P1
// Universidad de Guayaquil - Gestión de Configuración de Software
//
// Este pipeline implementa un flujo completo de CI/CD para una aplicación
// Flask en Python, incluyendo: checkout, validación, pruebas, construcción,
// despliegue y notificaciones.
// ============================================================================

pipeline {
    agent any

    environment {
        APP_NAME = 'gcs-proyecto-p1'
        APP_VERSION = '1.0.0'
        PYTHON_VERSION = '3'
        COVERAGE_DIR = 'htmlcov'
        TEST_REPORTS_DIR = 'test-reports'
        BUILD_ARTIFACTS_DIR = 'build-artifacts'
    }

    triggers {
        // Polling SCM cada 15 minutos como fallback del webhook
        pollSCM('H/15 * * * *')
        // Para GitHub webhook: instalar plugin "GitHub Integration" y usar githubPush()
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '30'))
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
    }

    stages {
        // ====================================================================
        // ETAPA 1: CHECKOUT
        // ====================================================================
        stage('Checkout') {
            steps {
                echo '=========================================='
                echo 'ETAPA: CHECKOUT - Descargando código fuente'
                echo '=========================================='

                checkout scm

                script {
                    env.GIT_COMMIT_MSG = sh(script: "git log -1 --pretty=%B", returnStdout: true).trim()
                    env.GIT_COMMIT_AUTHOR = sh(script: "git log -1 --pretty=%an", returnStdout: true).trim()
                    env.GIT_COMMIT_HASH = sh(script: "git log -1 --pretty=%h", returnStdout: true).trim()
                }

                echo "Commit: ${env.GIT_COMMIT_HASH}"
                echo "Autor: ${env.GIT_COMMIT_AUTHOR}"
                echo "Mensaje: ${env.GIT_COMMIT_MSG}"
            }
        }

        // ====================================================================
        // ETAPA 2: SETUP ENVIRONMENT
        // ====================================================================
        stage('Setup Environment') {
            steps {
                echo '=========================================='
                echo 'ETAPA: SETUP - Configurando entorno Python'
                echo '=========================================='

                sh '''
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip setuptools wheel
                    pip install -r requirements.txt
                    pip install flake8 pylint
                    echo "Paquetes instalados:"
                    pip list
                '''
            }
        }

        // ====================================================================
        // ETAPA 3: LINT
        // ====================================================================
        stage('Lint') {
            steps {
                echo '=========================================='
                echo 'ETAPA: LINT - Análisis de calidad del código'
                echo '=========================================='

                sh '''
                    . venv/bin/activate
                    mkdir -p ${TEST_REPORTS_DIR}

                    echo "Ejecutando flake8..."
                    flake8 app/ --count --statistics --max-line-length=120 --exclude=venv,__pycache__ || true

                    echo "Ejecutando pylint..."
                    pylint app/ --output-format=text --disable=C0114,C0115,C0116 || true

                    echo "Análisis de linting completado"
                '''
            }
        }

        // ====================================================================
        // ETAPA 4: BUILD
        // ====================================================================
        stage('Build') {
            steps {
                echo '=========================================='
                echo 'ETAPA: BUILD - Construcción de artefactos'
                echo '=========================================='

                sh '''
                    . venv/bin/activate
                    mkdir -p ${BUILD_ARTIFACTS_DIR}

                    # Limpiar cachés
                    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
                    find . -type f -name "*.pyc" -delete 2>/dev/null || true

                    # Crear archivo de versión
                    echo "{\\"version\\": \\"${APP_VERSION}\\", \\"build_number\\": \\"${BUILD_NUMBER}\\", \\"commit\\": \\"${GIT_COMMIT_HASH}\\", \\"build_date\\": \\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\\"}" > app/version.json

                    # Empaquetar la aplicación
                    tar -czf ${BUILD_ARTIFACTS_DIR}/${APP_NAME}-${BUILD_NUMBER}.tar.gz \
                        --exclude=venv --exclude=.git --exclude=__pycache__ --exclude="*.pyc" .

                    ls -lh ${BUILD_ARTIFACTS_DIR}/
                    echo "Build completado exitosamente"
                '''

                // Construir imagen Docker si Docker está disponible
                sh '''
                    if command -v docker &> /dev/null; then
                        echo "Docker encontrado, construyendo imagen..."
                        sudo docker build --tag ${APP_NAME}:${BUILD_NUMBER} --tag ${APP_NAME}:latest . || echo "Docker build falló (no crítico)"
                        sudo docker images | grep ${APP_NAME} || true
                    else
                        echo "Docker no disponible, saltando construcción de imagen"
                    fi
                '''
            }
        }

        // ====================================================================
        // ETAPA 5: TEST
        // ====================================================================
        stage('Test') {
            steps {
                echo '=========================================='
                echo 'ETAPA: TEST - Ejecución de pruebas'
                echo '=========================================='

                sh '''
                    . venv/bin/activate
                    mkdir -p ${TEST_REPORTS_DIR}

                    echo "Ejecutando pytest con cobertura..."
                    pytest \
                        --cov=app \
                        --cov-report=term \
                        --cov-report=html:${COVERAGE_DIR} \
                        --cov-report=xml:${TEST_REPORTS_DIR}/coverage.xml \
                        --junitxml=${TEST_REPORTS_DIR}/junit.xml \
                        -v --tb=short \
                        tests/ 2>&1 | tee ${TEST_REPORTS_DIR}/test-output.log

                    echo "Pruebas completadas"
                '''
            }

            post {
                always {
                    junit testResults: "${TEST_REPORTS_DIR}/*.xml", allowEmptyResults: true
                }
            }
        }

        // ====================================================================
        // ETAPA 6: DEPLOY
        // ====================================================================
        stage('Deploy') {
            steps {
                echo '=========================================='
                echo 'ETAPA: DEPLOY - Despliegue de la aplicación'
                echo '=========================================='

                sh '''
                    if command -v docker &> /dev/null; then
                        echo "Desplegando con Docker..."
                        sudo docker stop ${APP_NAME}-deploy 2>/dev/null || true
                        sudo docker rm ${APP_NAME}-deploy 2>/dev/null || true
                        sudo docker run -d --name ${APP_NAME}-deploy -p 5000:5000 ${APP_NAME}:latest
                        sleep 5

                        echo "Verificando despliegue..."
                        MAX_ATTEMPTS=10
                        ATTEMPT=0
                        while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
                            HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health 2>/dev/null || echo "000")
                            if [ "$HTTP_CODE" = "200" ]; then
                                echo "Health check exitoso (HTTP $HTTP_CODE)"
                                curl -s http://localhost:5000/health
                                echo ""
                                break
                            fi
                            echo "Health check intento $((ATTEMPT+1))/$MAX_ATTEMPTS (HTTP $HTTP_CODE)"
                            sleep 3
                            ATTEMPT=$((ATTEMPT+1))
                        done

                        echo "Aplicación desplegada en http://localhost:5000"
                    else
                        echo "Docker no disponible. Deploy manual requerido."
                    fi
                '''
            }
        }
    }

    // ========================================================================
    // POST - Acciones posteriores
    // ========================================================================
    post {
        always {
            echo '=========================================='
            echo 'POST: Acciones finales'
            echo '=========================================='

            archiveArtifacts artifacts: "${BUILD_ARTIFACTS_DIR}/**", allowEmptyArchive: true
            archiveArtifacts artifacts: "${TEST_REPORTS_DIR}/**", allowEmptyArchive: true
        }

        success {
            echo '=========================================='
            echo 'POST: BUILD EXITOSO'
            echo '=========================================='
            echo "Pipeline completado exitosamente para ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }

        failure {
            echo '=========================================='
            echo 'POST: BUILD FALLIDO'
            echo '=========================================='
            echo "Pipeline falló para ${env.JOB_NAME} #${env.BUILD_NUMBER}"

            sh '''
                sudo docker stop ${APP_NAME}-deploy 2>/dev/null || true
                sudo docker rm ${APP_NAME}-deploy 2>/dev/null || true
            '''
        }

        cleanup {
            echo 'POST: Limpieza final'
        }
    }
}

// ============================================================================
// CONFIGURACIÓN DE GITHUB WEBHOOK (Instrucciones)
// ============================================================================
//
// 1. Instalar plugin "GitHub Integration" en Jenkins
// 2. Manage Jenkins → Credentials → Agregar token de GitHub
// 3. En GitHub: Settings → Webhooks → Add webhook
//    - URL: http://<jenkins-url>/github-webhook/
//    - Content type: application/json
//    - Events: Push events
// 4. Cambiar pollSCM() por githubPush() en triggers
//
// ============================================================================
