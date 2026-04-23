#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Pedro Escobedo Straffon.
Creation Date: 2026-04-22 09:54:40.
Description: UI to extract the relevant data of a business card.
"""
import streamlit as st
import pandas as pd

from pydantic_examples import process_card_img, insert_card_in_excel
from pydantic_examples import process_card_img
from load_env import load_env_var
from pathlib import Path
from streamlit.runtime.uploaded_file_manager import UploadedFile

CARDS_EXCEL_PATH = Path(load_env_var("CARDS_EXCEL_PATH"))


def convert_img_to_bytes(img: UploadedFile) -> dict:
    """Converts the image to bytes and sends it to process card"""
    image_bytes = img.read()
    img_ext = Path(img.name).suffix.replace(".", "")

    return process_card_img(image_bytes, img_ext)


# UI of the program
uploaded_file = st.file_uploader("Sube la tarjeta", type=["jpg", "jpeg", "png"])
comments = st.text_area("Comentarios")
submit = st.button("Enviar")

if submit and uploaded_file:

    result = convert_img_to_bytes(uploaded_file)
    result["comments"] = comments
    insert_card_in_excel(result)

    st.json(result)

st.dataframe(pd.read_excel(CARDS_EXCEL_PATH))
with open(CARDS_EXCEL_PATH, "rb") as f:
    st.download_button(
        label="Descargar Excel",
        data=f,
        file_name="cards.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
