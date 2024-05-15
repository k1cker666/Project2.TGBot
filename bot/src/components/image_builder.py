import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


class ImageBuilder:

    start_image = Image.open(
        f"{os.path.abspath(os.curdir)}/bot/images/start_image_template.png"
    )
    right_answer = Image.open(
        f"{os.path.abspath(os.curdir)}/bot/images/right_answer_template.png"
    )
    wrong_answer = Image.open(
        f"{os.path.abspath(os.curdir)}/bot/images/wrong_answer_template.png"
    )
    end_lesson = Image.open(
        f"{os.path.abspath(os.curdir)}/bot/images/end_lesson_template.png"
    )
    progress_bar = Image.open(
        f"{os.path.abspath(os.curdir)}/bot/images/progress_bar_template.png"
    )
    font = ImageFont.truetype(
        font=f"{os.path.abspath(os.curdir)}/bot/fonts/Merriweather.ttf",
        size=34,
        encoding="UTF-8",
    )
    stat_font = ImageFont.truetype(
        font=f"{os.path.abspath(os.curdir)}/bot/fonts/Merriweather.ttf",
        size=28,
        encoding="UTF-8",
    )
    text_coords = (208, 168)
    common_word_count: int

    def __init__(self, common_word_count: int):
        self.common_word_count = common_word_count

    def __get_percent(self, number: int) -> float:
        percent = number / self.common_word_count * 100
        return int(percent) if percent.is_integer() else round(percent, 1)

    def __get_x_by_percent(self, percent: int) -> int:
        return int(12 + 291 / 100 * percent)

    def __write_in_buffer(self, image: Image) -> BytesIO:
        buffer = BytesIO()
        image.save(buffer, "PNG")
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
            fill=(0, 0, 0),
            font=self.font,
            anchor="mm",
        )
        return self.__write_in_buffer(start_image)

    def get_right_answer_image(self, word: str) -> BytesIO:
        right_answer = self.right_answer.copy()
        draw = ImageDraw.Draw(right_answer)
        draw.text(
            xy=self.text_coords,
            text=word,
            fill=(0, 0, 0),
            font=self.font,
            anchor="mm",
        )
        return self.__write_in_buffer(right_answer)

    def get_wrong_answer_image(self, word: str) -> BytesIO:
        wrong_answer = self.wrong_answer.copy()
        draw = ImageDraw.Draw(wrong_answer)
        draw.text(
            xy=self.text_coords,
            text=word,
            fill=(0, 0, 0),
            font=self.font,
            anchor="mm",
        )
        return self.__write_in_buffer(wrong_answer)

    def get_progress_bar_image(
        self, passed_words: int, learned_words: int
    ) -> BytesIO:
        passed_words_percent = self.__get_percent(passed_words)
        learned_words_percent = self.__get_percent(learned_words)
        passed_words_x = self.__get_x_by_percent(passed_words_percent)
        learned_words_x = self.__get_x_by_percent(learned_words_percent)
        progress_bar_image = self.progress_bar.copy()
        draw = ImageDraw.Draw(progress_bar_image)
        draw.rounded_rectangle(
            xy=[(12, 69), (passed_words_x, 95)], radius=3, fill=(94, 186, 24)
        )
        draw.text(
            xy=(310, 63),
            text=f"{passed_words_percent}%",
            fill=(0, 0, 0),
            font=self.stat_font,
        )

        draw.rounded_rectangle(
            xy=[(12, 154), (learned_words_x, 180)],
            radius=3,
            fill=(94, 186, 24),
        )
        draw.text(
            xy=(310, 148),
            text=f"{learned_words_percent}%",
            fill=(0, 0, 0),
            font=self.stat_font,
        )
        return self.__write_in_buffer(progress_bar_image)
