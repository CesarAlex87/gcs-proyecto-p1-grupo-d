"""
Módulo Calculadora - Operaciones matemáticas básicas.
Proyecto Primer Parcial - Gestión de la Configuración del Software
Universidad de Guayaquil - Grupo D
"""

from typing import Union


class DivisionPorCeroError(Exception):
    """Excepción levantada cuando se intenta dividir entre cero."""
    pass


def sumar(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Suma dos números.

    Args:
        a: Primer número
        b: Segundo número

    Returns:
        La suma de a y b
    """
    return a + b


def restar(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Resta dos números.

    Args:
        a: Minuendo
        b: Sustraendo

    Returns:
        La diferencia a - b
    """
    return a - b


def multiplicar(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Multiplica dos números.

    Args:
        a: Primer número
        b: Segundo número

    Returns:
        El producto de a y b
    """
    return a * b


def dividir(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Divide dos números.

    Args:
        a: Dividendo
        b: Divisor

    Returns:
        El cociente a / b

    Raises:
        DivisionPorCeroError: Si b es cero
    """
    if b == 0:
        raise DivisionPorCeroError("No se puede dividir entre cero")
    return a / b
