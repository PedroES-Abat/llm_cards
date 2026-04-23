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
    company_address: str
    person_number: str
    person_email: str
    company_web: str
    person_name: str
    company_name: str


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

    prompt = "Please extract the relevant data from the image."
    print(f"Media type:  image/{img_ext}")

    prompt_output = agent.run_sync(
        [
            prompt,
            BinaryContent(data=image_bytes, media_type=f"image/{img_ext}"),
        ]
    )

    return prompt_output


def process_card_img(image_bytes: bytes, img_ext: str) -> dict:
    """Runs the AI agent on a card image and saves the result to Excel."""

    agent = create_ai_agent_cards()
    prompt_output = query_agent_img(agent, image_bytes, img_ext)

    return prompt_output.data.model_dump()


def insert_card_in_excel(card_info: dict) -> None:
    """Inserts the bussines card information in a Excel"""

    CARDS_EXCEL_PATH = Path(load_env_var("CARDS_EXCEL_PATH"))

    if not CARDS_EXCEL_PATH.exists():
        raise FileNotFoundError(f"Excel file not found: {CARDS_EXCEL_PATH}")

    df = pd.read_excel(CARDS_EXCEL_PATH, engine="openpyxl")
    new_row = pd.DataFrame([card_info])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(CARDS_EXCEL_PATH, index=False, engine="openpyxl")
