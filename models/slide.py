import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from utilities import convert_hex_color_code_to_rgb, convert_matplotlib_figure_to_PIL_image
from config import *


class Slide:
    def __init__(self, width=1280, height=720):
        self.__slide = Image.new('RGB', (width, height), color='white')


    def add_title(self, text='EXAMPLE_TITLE'):
        '''
        Title is always in the center of the slide horizontally. Thus we do not need to adjust the horizontal margin.
        However, we need to be able to adjust the vertical margin.
        Vertically, the available space to draw text is height of the slide MINUS the text height.
        '''
        font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)

        draw = ImageDraw.Draw(self.__slide)
        text_width, text_height = draw.textsize(text, font=font)
        text_offset_x = int((self.__slide.width / 2) - (text_width / 2))
        available_slide_height = self.__slide.height - text_height
        text_offset_y = int(TITLE_AUTO_MARGIN_Y * available_slide_height)

        color = convert_hex_color_code_to_rgb(TITLE_FONT_COLOR)
        draw.text((text_offset_x, text_offset_y), text, color, font=font)

    
    def add_image_from_matplotlib_figure(self, matplotlib_figure):
        '''
        Image is always in the center of the slide horizontally as well as vertically.
        '''
        image = convert_matplotlib_figure_to_PIL_image(matplotlib_figure)
        image_offset_x = int((self.__slide.width / 2) - (image.width / 2))
        image_offset_y = int((self.__slide.height / 2) - (image.height / 2))
        self.__slide.paste(image, (image_offset_x, image_offset_y))


    def add_image_from_file(self, path):
        '''
        Image is always in the center of the slide horizontally as well as vertically.
        '''
        image = Image.open(path, 'r')
        image_offset_x = int((self.__slide.width / 2) - (image.width / 2))
        image_offset_y = int((self.__slide.height / 2) - (image.height / 2))
        self.__slide.paste(image, (image_offset_x, image_offset_y))

    
    def add_note(self, text=('EXAMPLE_TEXT_LEFT', 'EXAMPLE_TEXT_RIGHT')):
        '''
        Notes are organized into two parts: LEFT and RIGHT. Each part has a text and a box.
        Below is the order of the element we are going to draw:
            Left box -> Left text -> Right box -> Right text

        A.  Drawing the text
            1.  Split the slide width into two
            2.  Horizontally, the available space to draw text is half of the slide width MINUS the text width.
                By this mechanism, having 0% margin will put the text in the most outer part of the slide.
                In contrast, having 100% margin will put the text in the most inner part of the slide.
            3.  We apply this mechanism to draw the left text as well as the right text.

        B.  Drawing the box
            1.  Box is drawn to contain the text in its center. However, the box width is limited to as wide as the slide width.
                Thus, if the margin of the text is too small, it will fail to contain the text in its center.
        '''

        font = ImageFont.truetype(FONT_PATH, NOTES_FONT_SIZE)
        draw = ImageDraw.Draw(self.__slide)

        half_slide_width = int(self.__slide.width / 2)

        '''
        Drawing Left Box and Left text
        '''
        text_width, text_height = draw.textsize(text[0], font=font)
        available_left_slide_width = half_slide_width - text_width
        text_offset_x = int(NOTES_AUTO_MARGIN_X * available_left_slide_width)
        available_slide_height = self.__slide.height - text_height
        text_offset_y = int(NOTES_AUTO_MARGIN_Y * available_slide_height)

        box_offset_x0 = text_offset_x - (half_slide_width - text_offset_x - text_width)
        if box_offset_x0 < 0:
            box_offset_x0 = 0
        box_offset_y0 = text_offset_y - 10
        box_offset_x1 = half_slide_width
        box_offset_y1 = text_offset_y + text_height + 10
        box_shape = [(box_offset_x0, box_offset_y0), (box_offset_x1, box_offset_y1)]

        draw.rectangle(box_shape, fill=NOTES_BOX_FILL_COLOR, outline=NOTES_BOX_OUTLINE_COLOR)
        color = convert_hex_color_code_to_rgb(NOTES_FONT_COLOR)
        draw.text((text_offset_x, text_offset_y), text[0], color, font=font)

        '''
        Drawing Right Box and Right text
        '''
        text_width, text_height = draw.textsize(text[1], font=font)
        available_right_slide_width = half_slide_width - text_width
        text_offset_x = half_slide_width + available_right_slide_width - int(NOTES_AUTO_MARGIN_X * available_right_slide_width)
        available_slide_height = self.__slide.height - text_height
        text_offset_y = int(NOTES_AUTO_MARGIN_Y * available_slide_height)

        box_offset_x0 = half_slide_width
        box_offset_y0 = text_offset_y - 10
        box_offset_x1 = text_offset_x + text_width + (text_offset_x - half_slide_width)
        if box_offset_x1 > self.__slide.width:
            box_offset_x1 = self.__slide.width
        box_offset_y1 = text_offset_y + text_height + 10
        box_shape = [(box_offset_x0, box_offset_y0), (box_offset_x1, box_offset_y1)]

        draw.rectangle(box_shape, fill=NOTES_BOX_FILL_COLOR, outline=NOTES_BOX_OUTLINE_COLOR)
        color = convert_hex_color_code_to_rgb(NOTES_FONT_COLOR)
        draw.text((text_offset_x, text_offset_y), text[1], color, font=font)


    def get_slide(self):
        return self.__slide


    def save_as_file(self, path):
        self.__slide.save(path)
