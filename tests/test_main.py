"""
Pruebas de Integración de la Aplicación Flask.
Proyecto Primer Parcial - Gestión de la Configuración del Software
Universidad de Guayaquil - Grupo D

Contiene pruebas para todos los endpoints de la API REST,
verificando comportamiento correcto y manejo de errores.
"""

import pytest
from app.main import app, ESTUDIANTES_GRUPO_D


@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba de Flask."""
    app.config["TESTING"] = True
    with app.test_client() as cliente:
        yield cliente


class TestEndpointRaiz:
    """Pruebas para el endpoint raíz."""

    def test_get_raiz(self, client) -> None:
        """Prueba GET / - Debe retornar información del proyecto."""
        respuesta = client.get("/")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert "mensaje" in datos
        assert "proyecto" in datos
        assert "grupo" in datos
        assert datos["grupo"] == "D"

    def test_raiz_contiene_endpoints(self, client) -> None:
        """Prueba que el endpoint raíz lista los demás endpoints."""
        respuesta = client.get("/")
        datos = respuesta.get_json()
        assert "endpoints" in datos
        assert "health" in datos["endpoints"]
        assert "calcular/sumar" in datos["endpoints"]


class TestHealthCheck:
    """Pruebas para el endpoint de verificación de salud."""

    def test_get_health(self, client) -> None:
        """Prueba GET /health - Debe retornar estado healthy."""
        respuesta = client.get("/health")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["status"] == "healthy"

    def test_health_contiene_version(self, client) -> None:
        """Prueba que health check incluya información de versión."""
        respuesta = client.get("/health")
        datos = respuesta.get_json()
        assert "version" in datos
        assert "service" in datos


class TestCalculadoraSuma:
    """Pruebas para el endpoint de suma."""

    def test_suma_valida(self, client) -> None:
        """Prueba suma con parámetros válidos."""
        respuesta = client.get("/api/calculator/add?a=5&b=3")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["a"] == 5
        assert datos["b"] == 3
        assert datos["resultado"] == 8
        assert datos["operacion"] == "suma"

    def test_suma_decimales(self, client) -> None:
        """Prueba suma con números decimales."""
        respuesta = client.get("/api/calculator/add?a=2.5&b=1.5")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["resultado"] == 4.0

    def test_suma_negativos(self, client) -> None:
        """Prueba suma con números negativos."""
        respuesta = client.get("/api/calculator/add?a=-5&b=3")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["resultado"] == -2

    def test_suma_sin_parametros(self, client) -> None:
        """Prueba suma sin parámetros - Debe retornar error 400."""
        respuesta = client.get("/api/calculator/add")
        assert respuesta.status_code == 400
        datos = respuesta.get_json()
        assert "error" in datos

    def test_suma_parametro_faltante(self, client) -> None:
        """Prueba suma faltando un parámetro."""
        respuesta = client.get("/api/calculator/add?a=5")
        assert respuesta.status_code == 400


class TestCalculadoraResta:
    """Pruebas para el endpoint de resta."""

    def test_resta_valida(self, client) -> None:
        """Prueba resta con parámetros válidos."""
        respuesta = client.get("/api/calculator/subtract?a=10&b=3")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["a"] == 10
        assert datos["b"] == 3
        assert datos["resultado"] == 7
        assert datos["operacion"] == "resta"

    def test_resta_resultado_negativo(self, client) -> None:
        """Prueba resta que produce resultado negativo."""
        respuesta = client.get("/api/calculator/subtract?a=3&b=10")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["resultado"] == -7


class TestCalculadoraMultiplicacion:
    """Pruebas para el endpoint de multiplicación."""

    def test_multiplicacion_valida(self, client) -> None:
        """Prueba multiplicación con parámetros válidos."""
        respuesta = client.get("/api/calculator/multiply?a=4&b=5")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["a"] == 4
        assert datos["b"] == 5
        assert datos["resultado"] == 20
        assert datos["operacion"] == "multiplicacion"

    def test_multiplicacion_por_cero(self, client) -> None:
        """Prueba multiplicación por cero."""
        respuesta = client.get("/api/calculator/multiply?a=5&b=0")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["resultado"] == 0


class TestCalculadoraDivision:
    """Pruebas para el endpoint de división."""

    def test_division_valida(self, client) -> None:
        """Prueba división con parámetros válidos."""
        respuesta = client.get("/api/calculator/divide?a=10&b=2")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["a"] == 10
        assert datos["b"] == 2
        assert datos["resultado"] == 5.0
        assert datos["operacion"] == "division"

    def test_division_por_cero(self, client) -> None:
        """Prueba división por cero - Debe retornar error 400."""
        respuesta = client.get("/api/calculator/divide?a=10&b=0")
        assert respuesta.status_code == 400
        datos = respuesta.get_json()
        assert "error" in datos
        assert "cero" in datos["error"].lower()

    def test_division_resultado_decimal(self, client) -> None:
        """Prueba división con resultado decimal."""
        respuesta = client.get("/api/calculator/divide?a=7&b=2")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["resultado"] == 3.5

    def test_division_cero_dividendo(self, client) -> None:
        """Prueba división cuando el dividendo es cero."""
        respuesta = client.get("/api/calculator/divide?a=0&b=5")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["resultado"] == 0.0


class TestEstudiantes:
    """Pruebas para el endpoint de estudiantes."""

    def test_get_estudiantes(self, client) -> None:
        """Prueba GET /api/students - Debe retornar lista de estudiantes."""
        respuesta = client.get("/api/students")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert "grupo" in datos
        assert datos["grupo"] == "D"
        assert "estudiantes" in datos
        assert isinstance(datos["estudiantes"], list)

    def test_cantidad_estudiantes(self, client) -> None:
        """Prueba que retorna la cantidad correcta de estudiantes."""
        respuesta = client.get("/api/students")
        datos = respuesta.get_json()
        assert datos["cantidad"] == len(ESTUDIANTES_GRUPO_D)
        assert datos["cantidad"] == 5

    def test_estructura_estudiante(self, client) -> None:
        """Prueba que cada estudiante tiene la estructura correcta."""
        respuesta = client.get("/api/students")
        datos = respuesta.get_json()
        for estudiante in datos["estudiantes"]:
            assert "id" in estudiante
            assert "nombre" in estudiante
            assert "carrera" in estudiante


class TestErrorHandling:
    """Pruebas para manejo de errores."""

    def test_endpoint_no_existe(self, client) -> None:
        """Prueba acceso a endpoint inexistente - Debe retornar 404."""
        respuesta = client.get("/api/endpoint-que-no-existe")
        assert respuesta.status_code == 404
        datos = respuesta.get_json()
        assert "error" in datos
        assert "no encontrado" in datos["error"].lower()

    def test_suma_parametros_invalidos(self, client) -> None:
        """Prueba suma con parámetros que no son números."""
        respuesta = client.get("/api/calculator/add?a=abc&b=def")
        assert respuesta.status_code == 400


class TestMetodosHTTP:
    """Pruebas para métodos HTTP no soportados."""

    def test_post_health(self, client) -> None:
        """Prueba POST /health - Debe retornar 405 Method Not Allowed."""
        respuesta = client.post("/health")
        assert respuesta.status_code == 405

    def test_put_suma(self, client) -> None:
        """Prueba PUT en endpoint de suma."""
        respuesta = client.put("/api/calculator/add?a=5&b=3")
        assert respuesta.status_code == 405
