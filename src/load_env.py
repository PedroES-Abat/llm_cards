#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Load environment variables from env/.env file.
"""

from pathlib import Path
from os import environ

from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent.parent / "env" / ".env"


def load_environment_variables():
    if not ENV_PATH.exists():
        raise FileNotFoundError(f"Environment file not found at: {ENV_PATH}")

    if not load_dotenv(ENV_PATH, override=True):
        raise RuntimeError(f"Failed to load environment file at: {ENV_PATH}")


def load_env_var(env_var_name: str, target_type=None):
    try:
        value = environ[env_var_name]
        if target_type is bool:
            return value.strip().lower() == "true"
        if target_type:
            return target_type(value)
        return value
    except KeyError:
        raise KeyError(f"Environment variable '{env_var_name}' not found.")
