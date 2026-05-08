#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Pedro Escobedo Straffon.
Creation Date: 2026-04-22.
Description: Extracts contact information from business card images using a Gemini AI agent
    and stores the results in an Excel file.
"""

import pandas as pd

from pathlib import Path
from pydantic_ai import Agent, BinaryContent
from pydantic import BaseModel
from load_env import load_environment_variables, load_env_var

load_environment_variables()
AI_MODEL = load_env_var("GEMINI_AI_MODEL")


class CardOutput(BaseModel):
    Companyaddress: str
    PersonNumber: str
    PersonEmail: str
    CompanyWeb: str
    PersonName: str
    CompanyName: str


def create_ai_agent_cards() -> Agent:
    """Extracts the information of a business card"""

    agent = Agent(
        AI_MODEL,
        result_type=CardOutput,
        system_prompt=(
            "You are an AI agent specialized in extracting contact information from business cards."
            "Given an image of a business card, extract the following information:"
            "1. Company address: Extract the full address of the company as shown on the card."
            "2. Person phone number: Extract the phone number of the person on the card."
            "3. Person email: Extract the email address of the person on the card."
            "4. Company website: Extract the website URL of the company as shown on the card."
            "5. Person name: Extract the full name of the person on the card."
            "6. Company name: Extract the name of the company as shown on the card."
            "Be precise and extract only information that is clearly visible on the card."
            "If a field is not present, return an empty string for that field."
        ),
    )

    return agent


def query_agent_img(agent: Agent, image_bytes: bytes, img_ext: str):
    """Sends the image to the AI agent and returns response."""
    import time

    prompt = "Please extract the relevant data from the image."

    for attempt in range(3):
        try:
            return agent.run_sync(
                [
                    prompt,
                    BinaryContent(data=image_bytes, media_type=f"image/{img_ext}"),
                ]
            )
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)


def process_card_img(image_bytes: bytes, img_ext: str) -> dict:
    """Runs the AI agent on a card image and saves the result to Excel."""

    agent = create_ai_agent_cards()
    prompt_output = query_agent_img(agent, image_bytes, img_ext)

    return prompt_output.data.model_dump()


def insert_card_in_db(card_info: dict) -> None:
    """Inserts business card information into PostgreSQL."""
    from sqlalchemy import create_engine

    engine = create_engine(load_env_var("DATABASE_URL"))
    pd.DataFrame([card_info]).to_sql(
        "CardsInfo", engine, if_exists="append", index=False
    )

    engine.dispose()
