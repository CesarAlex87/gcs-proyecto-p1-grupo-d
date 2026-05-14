"""
Aplicación Flask - API REST de Calculadora.
Proyecto Primer Parcial - Gestión de la Configuración del Software
Universidad de Guayaquil - Grupo D

Esta aplicación demuestra un pipeline CI/CD con Jenkins,
incluyendo pruebas unitarias, integración, y despliegue en Docker.
"""

from typing import Dict, Any, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS

from app.calculator import sumar, restar, multiplicar, dividir, DivisionPorCeroError


# Crear instancia de la aplicación Flask
app = Flask(__name__)
CORS(app)


# Constantes
ESTUDIANTES_GRUPO_D = [
    {
        "id": 1,
        "nombre": "Aguilar Villafuerte Daniel Mateo",
        "carrera": "Ingeniería en Sistemas Computacionales"
    },
    {
        "id": 2,
        "nombre": "Arroba Carrillo Omar Andres",
        "carrera": "Ingeniería en Sistemas Computacionales"
    },
    {
        "id": 3,
        "nombre": "Ayovi Villafuerte Camillie Thais",
        "carrera": "Ingeniería en Sistemas Computacionales"
    },
    {
        "id": 4,
        "nombre": "Cordova Viteri Erick Alejandro",
        "carrera": "Ingeniería en Sistemas Computacionales"
    },
    {
        "id": 5,
        "nombre": "Tipán Antón Cesar Alexander",
        "carrera": "Ingeniería en Sistemas Computacionales"
    }
]


@app.route("/", methods=["GET"])
def bienvenida() -> Tuple[Dict[str, Any], int]:
    """
    Endpoint raíz - Retorna mensaje de bienvenida con información del proyecto.

    Returns:
        JSON con información del proyecto y estatus HTTP 200
    """
    return jsonify({
        "mensaje": "Bienvenido al Proyecto de Gestión de la Configuración del Software",
        "proyecto": "Primer Parcial - Pipeline CI/CD con Jenkins",
        "universidad": "Universidad de Guayaquil",
        "profesor": "Ph.D. Franklin Parrales-Bravo",
        "grupo": "D",
        "endpoints": {
            "health": "/health",
            "calcular/sumar": "/api/calculator/add?a=X&b=Y",
            "calcular/restar": "/api/calculator/subtract?a=X&b=Y",
            "calcular/multiplicar": "/api/calculator/multiply?a=X&b=Y",
            "calcular/dividir": "/api/calculator/divide?a=X&b=Y",
            "listar_estudiantes": "/api/students"
        }
    }), 200


@app.route("/health", methods=["GET"])
def health_check() -> Tuple[Dict[str, Any], int]:
    """
    Endpoint de verificación de salud - Confirma que el servicio está activo.

    Returns:
        JSON con estado del servicio y estatus HTTP 200
    """
    return jsonify({
        "status": "healthy",
        "service": "Flask API Calculator",
        "version": "1.0.0"
    }), 200


@app.route("/api/calculator/add", methods=["GET"])
def suma() -> Tuple[Dict[str, Any], int]:
    """
    Endpoint para suma - Calcula a + b.

    Query Parameters:
        a: Primer número (float)
        b: Segundo número (float)

    Returns:
        JSON con el resultado o mensaje de error
    """
    try:
        a = request.args.get("a", type=float)
        b = request.args.get("b", type=float)

        if a is None or b is None:
            return jsonify({
                "error": "Parámetros requeridos: a y b (números)"
            }), 400

        resultado = sumar(a, b)
        return jsonify({
            "operacion": "suma",
            "a": a,
            "b": b,
            "resultado": resultado
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Error al procesar la solicitud: {str(e)}"
        }), 500


@app.route("/api/calculator/subtract", methods=["GET"])
def resta() -> Tuple[Dict[str, Any], int]:
    """
    Endpoint para resta - Calcula a - b.

    Query Parameters:
        a: Minuendo (float)
        b: Sustraendo (float)

    Returns:
        JSON con el resultado o mensaje de error
    """
    try:
        a = request.args.get("a", type=float)
        b = request.args.get("b", type=float)

        if a is None or b is None:
            return jsonify({
                "error": "Parámetros requeridos: a y b (números)"
            }), 400

        resultado = restar(a, b)
        return jsonify({
            "operacion": "resta",
            "a": a,
            "b": b,
            "resultado": resultado
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Error al procesar la solicitud: {str(e)}"
        }), 500


@app.route("/api/calculator/multiply", methods=["GET"])
def multiplicacion() -> Tuple[Dict[str, Any], int]:
    """
    Endpoint para multiplicación - Calcula a * b.

    Query Parameters:
        a: Primer número (float)
        b: Segundo número (float)

    Returns:
        JSON con el resultado o mensaje de error
    """
    try:
        a = request.args.get("a", type=float)
        b = request.args.get("b", type=float)

        if a is None or b is None:
            return jsonify({
                "error": "Parámetros requeridos: a y b (números)"
            }), 400

        resultado = multiplicar(a, b)
        return jsonify({
            "operacion": "multiplicacion",
            "a": a,
            "b": b,
            "resultado": resultado
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Error al procesar la solicitud: {str(e)}"
        }), 500


@app.route("/api/calculator/divide", methods=["GET"])
def division() -> Tuple[Dict[str, Any], int]:
    """
    Endpoint para división - Calcula a / b.

    Query Parameters:
        a: Dividendo (float)
        b: Divisor (float)

    Returns:
        JSON con el resultado o mensaje de error

    Maneja:
        - División por cero (retorna 400)
        - Parámetros inválidos (retorna 400)
        - Otros errores (retorna 500)
    """
    try:
        a = request.args.get("a", type=float)
        b = request.args.get("b", type=float)

        if a is None or b is None:
            return jsonify({
                "error": "Parámetros requeridos: a y b (números)"
            }), 400

        resultado = dividir(a, b)
        return jsonify({
            "operacion": "division",
            "a": a,
            "b": b,
            "resultado": resultado
        }), 200
    except DivisionPorCeroError as e:
        return jsonify({
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "error": f"Error al procesar la solicitud: {str(e)}"
        }), 500


@app.route("/api/students", methods=["GET"])
def obtener_estudiantes() -> Tuple[Dict[str, Any], int]:
    """
    Endpoint para obtener lista de estudiantes del Grupo D.

    Returns:
        JSON con la lista de estudiantes y estatus HTTP 200
    """
    return jsonify({
        "grupo": "D",
        "cantidad": len(ESTUDIANTES_GRUPO_D),
        "estudiantes": ESTUDIANTES_GRUPO_D,
        "universidad": "Universidad de Guayaquil",
        "carrera": "Ingeniería en Sistemas Computacionales"
    }), 200


@app.errorhandler(404)
def no_encontrado(error: Exception) -> Tuple[Dict[str, str], int]:
    """
    Manejador de error 404 - Recurso no encontrado.

    Args:
        error: Excepción del error 404

    Returns:
        JSON con mensaje de error y estatus HTTP 404
    """
    return jsonify({
        "error": "Recurso no encontrado",
        "mensaje": "El endpoint solicitado no existe"
    }), 404


@app.errorhandler(500)
def error_interno(error: Exception) -> Tuple[Dict[str, str], int]:
    """
    Manejador de error 500 - Error interno del servidor.

    Args:
        error: Excepción del error 500

    Returns:
        JSON con mensaje de error y estatus HTTP 500
    """
    return jsonify({
        "error": "Error interno del servidor",
        "mensaje": "Ocurrió un error inesperado"
    }), 500


if __name__ == "__main__":
    # Nota: En producción, usar gunicorn en lugar de esta configuración
    app.run(host="0.0.0.0", port=5000, debug=False)
