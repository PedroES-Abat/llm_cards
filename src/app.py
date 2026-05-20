#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Pedro Escobedo Straffon.
Creation Date: 2026-04-22 09:54:40.
Description: UI to extract the relevant data of a business card.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit.runtime.uploaded_file_manager import UploadedFile
from sqlalchemy import create_engine

from ai_agent import process_card_img, insert_card_in_db
from load_env import load_env_var


def convert_img_to_bytes(img: UploadedFile) -> dict:
    """Converts the image to bytes and sends it to process card"""

    image_bytes = img.read()
    img_ext = Path(img.name).suffix.replace(".", "")

    return process_card_img(image_bytes, img_ext)


def main():

    # UI of the program
    uploaded_file = st.file_uploader("Sube la tarjeta", type=["jpg", "jpeg", "png"])
    comments = st.text_area("Comentarios")
    submit = st.button("Enviar")

    if submit and uploaded_file:

        result = convert_img_to_bytes(uploaded_file)
        result["Comments"] = comments
        insert_card_in_db(result)

    engine = create_engine(load_env_var("DATABASE_URL"))
    df = pd.read_sql('SELECT * FROM "CardsInfo"', engine)
    engine.dispose()
    st.dataframe(df)


if __name__ == "__main__":
    main()
