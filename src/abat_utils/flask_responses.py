#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Jorge Germán García Velázquez.
Creation Date: 2025-03-19.
Description: Flask responses.
"""
from flask import jsonify


def bad_request() -> tuple:
    """
    Returns a 400 Bad Request response, with a JSON message indicating that the request body is empty or not a JSON.
    """
    return (
        jsonify(
            {
                "status": "ERROR",
                "message": "Bad Request: the request body is empty or not a JSON",
            }
        ),
        400,
    )


def internal_server_error(e: Exception) -> tuple:
    """
    Returns a 500 Internal Server Error response, with a JSON message indicating that an unexpected error occurred and the error detail.

    Parameters:
        e: The exception raised.
    """
    return (
        jsonify(
            {
                "status": "ERROR",
                "message": "Internal Server Error",
                "error_detail": str(e),
            }
        ),
        500,
    )


def success(result: str) -> tuple:
    """
    Returns a 200 OK response, with a JSON message indicating that the request was successful.

    Parameters:
        result: The result to return.
    """
    return (
        jsonify(
            {"status": "OK", "message": "The request was successful.", "result": result}
        ),
        200,
    )
