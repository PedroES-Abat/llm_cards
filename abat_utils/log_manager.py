#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Pedro Escobedo Straffon.
Creation Date: 2026-04-22 11:54:15.
Description: .
"""
import logging

from common.constants import logger_constants


logger = logging.getLogger(__name__)
logging.basicConfig(
    format=logger_constants.LOG_FORMAT,
    level=logger_constants.LOG_LEVEL,
    datefmt=logger_constants.LOG_DATE_FORMAT,
)

# Write to console.
console_handler = logging.StreamHandler()
console_handler.setLevel(logger_constants.LOG_LEVEL)
console_handler.setFormatter(
    logging.Formatter(
        logger_constants.LOG_FORMAT,
        datefmt=logger_constants.LOG_DATE_FORMAT,
    )
)

logger.addHandler(console_handler)
