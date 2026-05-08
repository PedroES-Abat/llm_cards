#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Pedro Escobedo Straffon.
Creation Date: 2026-04-22 09:54:40.
Description: UI to extract the relevant data of a business card.
"""

import streamlit as st
import pandas as pd

from pydantic_examples import process_card_img, insert_card_in_db
from pydantic_examples import process_card_img
from load_env import load_env_var
from pathlib import Path
from streamlit.runtime.uploaded_file_manager import UploadedFile


def convert_img_to_bytes(img: UploadedFile) -> dict:
    """Converts the image to bytes and sends it to process card"""
    from PIL import Image
    import io

    image = Image.open(img).convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()

    return process_card_img(image_bytes, "jpeg")


# UI of the program
uploaded_file = st.file_uploader("Sube la tarjeta", type=["jpg", "jpeg", "png"])
comments = st.text_area("Comentarios")
submit = st.button("Enviar")

if submit and uploaded_file:

    result = convert_img_to_bytes(uploaded_file)
    result["comments"] = comments
    insert_card_in_db(result)

from sqlalchemy import create_engine

engine = create_engine(load_env_var("DATABASE_URL"))
df = pd.read_sql("SELECT * FROM business_cards", engine)
engine.dispose()
st.dataframe(df)
