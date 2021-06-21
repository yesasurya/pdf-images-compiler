from models.pdf_file import PDFFile
from models.slide import Slide


def YOUR_SAMPLE_FUNCTION_TO_GENERATE_MATPLOTLIB_FIGURES():
    MATPLOTLIB_FIGURES = []

    import numpy as np
    import matplotlib.pyplot as plt

    slides = ['Slide 1', 10, 'Good'], ['Slide 2', 20, 'Bad']

    for slide in slides:
        print(f'This is {slide[0]}')

        # Create data
        t = np.arange(0.01, slide[1], 0.01)
        data1 = np.exp(t)
        data2 = np.sin(2 * np.pi * t)

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('exp', color=color)
        ax1.plot(t, data1, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx() # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('sin', color=color) # we already handled the x-label with ax1
        ax2.plot(t, data2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout() # otherwise the right y-label is slightly clipped

        MATPLOTLIB_FIGURES.append(fig)
    return MATPLOTLIB_FIGURES


def create_pdf():
    pdf = PDFFile()
    MATPLOTLIB_FIGURES = YOUR_SAMPLE_FUNCTION_TO_GENERATE_MATPLOTLIB_FIGURES()
    for i, figure in enumerate(MATPLOTLIB_FIGURES):
        slide = Slide()
        slide.add_title('Slide {0}'.format(i + 1))
        slide.add_image_from_matplotlib_figure(figure)
        slide.add_note(('Outcome', 'Good'))
        pdf.add_slide(slide)

    for i in range(2):
        slide = Slide()
        slide.add_title('EXAMPLE SLIDE')
        slide.add_image_from_file('./res/images/example_image.jpg')
        slide.add_note(('Image Source', 'Google'))
        pdf.add_slide(slide)
        
    pdf.save_as_file('./res/pdfs/EXAMPLE_PDF.pdf')


if __name__ == '__main__':
    create_pdf()
