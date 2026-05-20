#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Load environment variables from env/.env file or Streamlit secrets.
"""

from os import environ
from pathlib import Path

import streamlit as st

from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent.parent / "env" / ".env"


def load_environment_variables():
    if ENV_PATH.exists():
        if not load_dotenv(ENV_PATH, override=True):
            raise RuntimeError(f"Failed to load environment file at: {ENV_PATH}")
        return

    try:

        for key, value in st.secrets.items():
            environ[key] = str(value)
    except Exception:
        raise FileNotFoundError(
            f"Environment file not found at: {ENV_PATH} and no Streamlit secrets available."
        )


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
