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
from pydantic_ai.exceptions import ModelHTTPError

from ai_agent import process_card_img, insert_card_in_db, update_cards_in_db
from db_config import create_db_engine


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
        try:
            result = convert_img_to_bytes(uploaded_file)
            result["Comments"] = comments
            insert_card_in_db(result)

        except ModelHTTPError:
            st.error("Error de comunicación con Gemini, vuelve a intentarlo.")

    engine = create_db_engine()
    df = pd.read_sql('SELECT * FROM "CardsInfo"', engine)
    engine.dispose()

    db_df = st.data_editor(df, key="cards_editor", disabled=["Id"], num_rows="fixed")

    if st.button("Guardar cambios"):
        update_cards_in_db(db_df)
        del st.session_state["cards_editor"]
        st.success("Cambios guardados.")
        st.rerun()


if __name__ == "__main__":
    main()
