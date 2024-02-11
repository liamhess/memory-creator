from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

class Memorypdf():

    def __init__(self):
        self.images = []

    def add_caption(self, image, caption_text):
        size = (1000,150)
        font=ImageFont.truetype("Roboto-Regular.ttf", size=60)
        W, H = size
        caption_image = Image.new("RGBA", size, "white")
        caption_draw = ImageDraw.Draw(caption_image)
        _, _, w, h = caption_draw.textbbox((0,0), caption_text, font=font)
        caption_draw.text(((W-w)/2, (H-h)/2), caption_text, font=font, fill="black")

        image.paste(caption_image, (0, 850))

        return image

    def add_border(self, image):
        border_size = 2
        resized_image = image.resize((1000-border_size*2, 1000-border_size*2))
        image_with_border = ImageOps.expand(resized_image, border=border_size, fill="black")
        return image_with_border

    def resize_image(self, image):
        image = image.resize((1000, 1000))
        return image

    def process_image(self, input_image, caption_text):
        image = self.resize_image(input_image)
        image = self.add_caption(image, caption_text)
        image = self.add_border(image)
        return image
    
    def add_image(self, input_image, caption_text):
        image = self.process_image(input_image, caption_text)
        self.images.append(image)
        self.images.append(image)

    def list_directory(self, folder):
        files = os.listdir(folder)
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        files.sort()
        filecounter = 0
        files = [f"images/{filename}" for filename in files]
        return files

    def generate_pdf(self, file_name):
        c = canvas.Canvas(file_name, A4)
        width, height = A4
        print(width, height)

        # draw all images
        xcount = 0
        ycount = 0
        for image in self.images:
            x = 14 + 141.732 * xcount
            y = 66 + 141.732 * ycount
            c.drawInlineImage(image=image, x=x, y=y, width=141.732, height=141.732)
            xcount += 1
            if xcount >= 4:
                xcount = 0
                ycount += 1
            if ycount > 5:
                raise Exception("You're trying to fit too many pictures. One page can only hold 20 at a time.")

        c.save()
