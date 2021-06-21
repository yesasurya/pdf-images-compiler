import numpy as np
import io
from PIL import Image


def convert_hex_color_code_to_rgb(hex_color_code):
    hex_color_code = hex_color_code.replace('#', '')
    return tuple(int(hex_color_code[i:i + 2], 16) for i in (0, 2, 4))


def convert_matplotlib_figure_to_PIL_image(matplotlib_figure):
    buf = io.BytesIO()
    matplotlib_figure.savefig(buf)
    buf.seek(0)
    return Image.open(buf)
