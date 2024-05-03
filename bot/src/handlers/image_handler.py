import os
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
    
class ImageHandler:
    
    start_image = Image.open(f"{os.path.abspath(os.curdir)}/bot/images/start_image_template.png")
    right_answer = Image.open(f"{os.path.abspath(os.curdir)}/bot/images/right_answer_template.png")
    wrong_answer = Image.open(f"{os.path.abspath(os.curdir)}/bot/images/wrong_answer_template.png")
    font = ImageFont.truetype(
        font=f"{os.path.abspath(os.curdir)}/bot/fonts/Merriweather.ttf",
        size=72,
        encoding='UTF-8'
    )

    def write_in_buffer(self, image: Image) -> BytesIO:
        buffer = BytesIO()
        image.save(buffer, 'PNG')
        buffer.seek(0)
        return buffer
        
