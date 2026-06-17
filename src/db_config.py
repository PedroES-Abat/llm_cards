#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Pedro Escobedo Straffon.
Creation Date: 2026-06-15.
Description: Database engine configuration for PostgreSQL with SSL.
"""

from pathlib import Path

from sqlalchemy import URL, create_engine
from sqlalchemy.pool import QueuePool

from load_env import load_env_var

_BUNDLE_PEM_PATH = Path(__file__).parent.parent / "env" / "bundle.pem"


def create_db_engine():
    url = URL.create(
        drivername="postgresql+psycopg",
        username=load_env_var("Usuario"),
        password=load_env_var("Contrasena"),
        host=load_env_var("HOST"),
        port=load_env_var("Puerto"),
        database=load_env_var("NombreDB"),
    )
    return create_engine(
        url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": 10,
            "sslmode": "verify-full",
            "sslrootcert": str(_BUNDLE_PEM_PATH),
        },
    )
