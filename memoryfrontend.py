import streamlit as st
from memorybackend import Memorypdf

pdf = Memorypdf()
pdf.add_image("images/1.JPG", "il numero uno")
pdf.add_image("images/2.JPG", "il numero due")
pdf.add_image("images/3.JPG", "il numero tre")
pdf.generate_pdf("output.pdf")
