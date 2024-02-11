import streamlit as st
from memorybackend import Memorypdf
from PIL import Image
import io
import os.path
from datetime import datetime
import pytz

st.title("Scuola Caffè - Creatore di Memorie")

# initialize state
if "image_count" not in st.session_state:
    st.session_state["image_count"] = 0

if "pdf" not in st.session_state:
    st.session_state["pdf"] = Memorypdf()

if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0

# file uploader, caption input, save button
st.write(f"Hai già caricato {st.session_state['image_count']} immagini.")
if st.session_state["image_count"] < 10:
    uploaded_file = st.file_uploader(label="Carica un'immagine...", key=st.session_state["file_uploader_key"])
    if uploaded_file is not None:
        st.image(image=uploaded_file)
        caption = st.text_input(label="Inserisci una didascalia.")
    submitted = st.button("Aggiungi immagine!")
    if submitted and uploaded_file is not None and caption is not "":
        image = Image.open(uploaded_file)
        st.session_state["pdf"].add_image(image, caption)
        st.session_state["file_uploader_key"] += 1
        st.session_state["image_count"] += 1
        st.write("Caricato!")
        st.rerun()
    elif submitted and uploaded_file is None:
        st.warning("Carica un'immagine!")
    elif submitted and caption is "":
        st.warning("Inserisci una didascalia prima di caricare l'immagine!")

# generate pdf button
if st.session_state["image_count"] > 0:
    button = st.button("Genera PDF della memoria!")
    if button:
        with st.spinner("Elaborazione del PDF in corso..."):
            st.session_state["pdf"].generate_pdf("output.pdf")
        if os.path.isfile("./output.pdf"):
            with open("output.pdf", "rb") as file:
                content = file.read()
                # get time for filename
                now = datetime.now(pytz.timezone("Europe/Berlin"))
                datestring = now.strftime("%d-%m-%Y")
                st.download_button(label="Scarica il PDF della memoria!", data=content, file_name=f"memory-scuola-caffe-{datestring}.pdf")
