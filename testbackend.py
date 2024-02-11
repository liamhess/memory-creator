from memorybackend import Memorypdf
from PIL import Image

pdf = Memorypdf()
image = Image.open("images/1.JPG")
for i in range(0,10):
    pdf.add_image(image, "asdf")
pdf.generate_pdf("testbackend.pdf")
