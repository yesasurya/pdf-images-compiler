from PIL import Image
from numpy import append


class PDFFile:
    '''
    There are two ways to add slide to the PDF:
    1. Add slide from the instance of Slide model. By this way, we DO NOT NEED to save the slide as image file first.
    2. Add slide from image file. By this way, we NEED to save the slide as image file first.
    '''
    def __init__(self):
        self.__slides = []


    def add_slide(self, slide):
        self.__slides.append(slide.get_slide())


    def add_slide_from_file(self, path):
        image = Image.open(path, 'r')
        self.__slides.append(image)


    def save_as_file(self, path):
        if len(self.__slides) < 1:
            raise Exception('There is no slide. Please add at least one slide.')

        first_slide = self.__slides.pop(0)
        first_slide.save(path, save_all=True, append_images=self.__slides)
