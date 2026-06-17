#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Pedro Escobedo Straffon.
Creation Date: 2026-04-22.
Description: Extracts contact information from business card images using a Gemini AI agent
    and stores the results in an Excel file.
"""

import pandas as pd
import numpy as np
from pydantic_ai import Agent, BinaryContent
from pydantic import BaseModel
from time import sleep
from pathlib import Path
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert

from load_env import load_environment_variables, load_env_var
from db_config import create_db_engine

load_environment_variables()
AI_MODEL = load_env_var("GEMINI_AI_MODEL")


class CardOutput(BaseModel):
    CompanyAddress: str
    PersonMobileNumber: str
    PersonOfficeNumber: str
    PersonRole: str
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
            "You are an AI agent specialized in extracting contact information from business cards. "
            "Given an image of a business card, extract the following information: "
            "1. Company address: the full address of the company as shown on the card. "
            "2. Person mobile number: the personal cell phone number of the individual. "
            "Look for icons like 📱 or labels like 'Cel', 'Móvil', 'Mobile', 'Cell', 'M:'. "
            "If no label is present, a number without extension is likely a mobile. "
            "3. Person office number: the company landline or direct office line. "
            "Look for icons like 📞 or labels like 'Tel', 'Office', 'Oficina', 'Direct', 'Ph', 'T:', 'PBX'. "
            "Office numbers often include an extension (e.g., 'Ext. 123'). "
            "If multiple numbers exist and one has an extension, that one is the office number. "
            "4. Person role: the job title or position of the person on the card. "
            "5. Person email: the email address of the person on the card. "
            "6. Company website: the website URL of the company as shown on the card. "
            "7. Person name: the full name of the person on the card. "
            "8. Company name: the name of the company as shown on the card. "
            "Be precise and extract only information that is clearly visible on the card. "
            "If a field is not present on the card, return an empty string for that field."
        ),
    )

    return agent


def query_agent_img(agent: Agent, image_bytes: bytes, img_ext: str) -> any:
    """Sends the image to the AI agent and returns response."""

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
            sleep(2)


def process_card_img(image_bytes: bytes, img_ext: str) -> dict:
    """Runs the AI agent on a card image and saves the result to Excel."""

    agent = create_ai_agent_cards()
    prompt_output = query_agent_img(agent, image_bytes, img_ext)

    return prompt_output.data.model_dump()


def insert_card_in_db(card_info: dict) -> None:
    # TODO Copiar create engine de SAF. Crear archivo de seguridad buscarlo en SAF (para el encriptado)
    """Inserts business card information into PostgreSQL."""

    engine = create_db_engine()
    pd.DataFrame([card_info]).to_sql(
        "CardsInfo", engine, if_exists="append", index=False
    )

    engine.dispose()


def update_cards_in_db(df: pd.DataFrame) -> None:
    """Upserts the edited dataframe into CardsInfo: updates existing rows by Id."""

    engine = create_db_engine()
    table = Table("CardsInfo", MetaData(), autoload_with=engine)

    rows = df.replace({np.nan: None}).to_dict(orient="records")
    if not rows:
        return

    stmt = pg_insert(table).values(rows)
    update_dict = {
        col.name: stmt.excluded[col.name] for col in table.columns if col.name != "Id"
    }
    stmt = stmt.on_conflict_do_update(index_elements=["Id"], set_=update_dict)

    with engine.begin() as conn:
        conn.execute(stmt)

    engine.dispose()


# TODO hacer README
