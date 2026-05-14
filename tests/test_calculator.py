"""
Pruebas Unitarias del Módulo Calculadora.
Proyecto Primer Parcial - Gestión de la Configuración del Software
Universidad de Guayaquil - Grupo D

Contiene pruebas exhaustivas para todas las operaciones matemáticas,
incluyendo casos normales, valores negativos, cero, y casos extremos.
"""

import pytest
from app.calculator import (
    sumar, restar, multiplicar, dividir, DivisionPorCeroError
)


class TestSuma:
    """Pruebas para la función sumar."""

    def test_sumar_positivos(self) -> None:
        """Prueba suma de dos números positivos."""
        assert sumar(2, 3) == 5

    def test_sumar_negativos(self) -> None:
        """Prueba suma de dos números negativos."""
        assert sumar(-5, -3) == -8

    def test_sumar_mixtos(self) -> None:
        """Prueba suma de números positivos y negativos."""
        assert sumar(10, -7) == 3

    def test_sumar_con_cero(self) -> None:
        """Prueba suma cuando uno de los operandos es cero."""
        assert sumar(5, 0) == 5
        assert sumar(0, 5) == 5

    def test_sumar_ambos_cero(self) -> None:
        """Prueba suma de cero con cero."""
        assert sumar(0, 0) == 0

    def test_sumar_decimales(self) -> None:
        """Prueba suma de números con punto decimal."""
        assert sumar(1.5, 2.5) == 4.0
        assert abs(sumar(0.1, 0.2) - 0.3) < 1e-9


class TestResta:
    """Pruebas para la función restar."""

    def test_restar_positivos(self) -> None:
        """Prueba resta de dos números positivos."""
        assert restar(10, 3) == 7

    def test_restar_resultado_negativo(self) -> None:
        """Prueba resta que produce resultado negativo."""
        assert restar(5, 10) == -5

    def test_restar_negativos(self) -> None:
        """Prueba resta de números negativos."""
        assert restar(-5, -3) == -2

    def test_restar_con_cero(self) -> None:
        """Prueba resta cuando uno de los operandos es cero."""
        assert restar(5, 0) == 5
        assert restar(0, 5) == -5

    def test_restar_mismo_numero(self) -> None:
        """Prueba resta de un número consigo mismo."""
        assert restar(7, 7) == 0

    def test_restar_decimales(self) -> None:
        """Prueba resta de números con punto decimal."""
        assert restar(5.5, 2.5) == 3.0


class TestMultiplicacion:
    """Pruebas para la función multiplicar."""

    def test_multiplicar_positivos(self) -> None:
        """Prueba multiplicación de dos números positivos."""
        assert multiplicar(3, 4) == 12

    def test_multiplicar_negativos(self) -> None:
        """Prueba multiplicación de dos números negativos."""
        assert multiplicar(-3, -4) == 12

    def test_multiplicar_mixtos(self) -> None:
        """Prueba multiplicación de número positivo por negativo."""
        assert multiplicar(5, -2) == -10
        assert multiplicar(-5, 2) == -10

    def test_multiplicar_por_cero(self) -> None:
        """Prueba multiplicación cuando uno de los operandos es cero."""
        assert multiplicar(5, 0) == 0
        assert multiplicar(0, 5) == 0

    def test_multiplicar_por_uno(self) -> None:
        """Prueba multiplicación por uno (elemento neutro)."""
        assert multiplicar(5, 1) == 5
        assert multiplicar(1, 5) == 5

    def test_multiplicar_decimales(self) -> None:
        """Prueba multiplicación de números con punto decimal."""
        assert multiplicar(2.5, 4) == 10.0
        assert abs(multiplicar(0.1, 0.2) - 0.02) < 1e-9

    def test_multiplicar_fracciones(self) -> None:
        """Prueba multiplicación de fracciones."""
        assert multiplicar(0.5, 0.5) == 0.25


class TestDivision:
    """Pruebas para la función dividir."""

    def test_dividir_positivos(self) -> None:
        """Prueba división de dos números positivos."""
        assert dividir(10, 2) == 5.0

    def test_dividir_resultado_decimal(self) -> None:
        """Prueba división que produce resultado decimal."""
        assert abs(dividir(10, 3) - 3.333333) < 0.001

    def test_dividir_negativos(self) -> None:
        """Prueba división de números negativos."""
        assert dividir(-10, -2) == 5.0

    def test_dividir_mixtos(self) -> None:
        """Prueba división de número positivo por negativo."""
        assert dividir(-10, 2) == -5.0
        assert dividir(10, -2) == -5.0

    def test_dividir_por_cero(self) -> None:
        """Prueba división por cero - Debe lanzar excepción."""
        with pytest.raises(DivisionPorCeroError):
            dividir(10, 0)

    def test_dividir_cero_por_numero(self) -> None:
        """Prueba división de cero entre un número."""
        assert dividir(0, 5) == 0.0

    def test_dividir_por_uno(self) -> None:
        """Prueba división por uno (elemento neutro)."""
        assert dividir(5, 1) == 5.0

    def test_dividir_entre_mismo_numero(self) -> None:
        """Prueba división de un número entre sí mismo."""
        assert dividir(7, 7) == 1.0

    def test_dividir_decimales(self) -> None:
        """Prueba división de números con punto decimal."""
        assert dividir(5.0, 2.0) == 2.5

    def test_mensaje_error_division_cero(self) -> None:
        """Prueba el mensaje de error en división por cero."""
        with pytest.raises(DivisionPorCeroError) as excinfo:
            dividir(5, 0)
        assert "cero" in str(excinfo.value).lower()


class TestCasosExtremos:
    """Pruebas de casos extremos y límites."""

    def test_numeros_muy_grandes(self) -> None:
        """Prueba con números muy grandes."""
        a = 1e15
        b = 1e15
        resultado = sumar(a, b)
        assert resultado == 2e15

    def test_numeros_muy_pequenos(self) -> None:
        """Prueba con números muy pequeños."""
        a = 1e-10
        b = 1e-10
        resultado = sumar(a, b)
        assert abs(resultado - 2e-10) < 1e-20

    def test_precision_flotante(self) -> None:
        """Prueba la precisión en operaciones con punto flotante."""
        # Suma de muchas fracciones pequeñas
        resultado = 0.1 + 0.1 + 0.1
        assert abs(resultado - 0.3) < 1e-9
