import os
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
    
class ImageBuilder:
    
    start_image = Image.open(f"{os.path.abspath(os.curdir)}/bot/images/start_image_template.png")
    right_answer = Image.open(f"{os.path.abspath(os.curdir)}/bot/images/right_answer_template.png")
    wrong_answer = Image.open(f"{os.path.abspath(os.curdir)}/bot/images/wrong_answer_template.png")
    end_lesson = Image.open(f"{os.path.abspath(os.curdir)}/bot/images/end_lesson_template.png")
    font = ImageFont.truetype(
        font=f"{os.path.abspath(os.curdir)}/bot/fonts/Merriweather.ttf",
        size=34,
        encoding='UTF-8'
    )
    text_coords = (208, 168)

    def __write_in_buffer(self, image: Image) -> BytesIO:
        buffer = BytesIO()
        image.save(buffer, 'PNG')
        buffer.seek(0)
        return buffer
    
    def get_end_lesson_image(self) -> BytesIO:
        return self.__write_in_buffer(self.end_lesson)
    
    def get_start_image(self, word: str) -> BytesIO:
        start_image = self.start_image.copy()
        draw = ImageDraw.Draw(start_image)
        draw.text(
            xy=self.text_coords,
            text=word,
            fill=(0,0,0),
            font=self.font,
            anchor='mm'
        )
        return self.__write_in_buffer(start_image)
    
    def get_right_answer_image(self, word: str) -> BytesIO:
        right_answer = self.right_answer.copy()
        draw = ImageDraw.Draw(right_answer)
        draw.text(
            xy=self.text_coords,
            text=word,
            fill=(0,0,0),
            font=self.font,
            anchor='mm'
        )
        return self.__write_in_buffer(right_answer)
    
    def get_wrong_answer_image(self, word: str) -> BytesIO:
        wrong_answer = self.wrong_answer.copy()
        draw = ImageDraw.Draw(wrong_answer)
        draw.text(
            xy=self.text_coords,
            text=word,
            fill=(0,0,0),
            font=self.font,
            anchor='mm'
        )
        return self.__write_in_buffer(wrong_answer)