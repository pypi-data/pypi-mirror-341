from utility_pack.logger import log_exception
from utility_pack.ocr_util import ocr_image_pipeline
from tempfile import NamedTemporaryFile
from PIL import Image, ImageOps
from enum import Enum
import numpy as np
import fitz, cv2

def get_pdf_page_as_image(pdf_path, page_num, zoom_factor=3.5):
    # 1 - Read PDF
    pdf_document = fitz.open(pdf_path)

    # 2 - Convert page to image
    page = pdf_document.load_page(page_num)

    # Define the zoom factor for the image resolution. Higher values mean more pixels.
    mat = fitz.Matrix(zoom_factor, zoom_factor)

    # Render the page to an image (pixmap)
    pix_image = page.get_pixmap(matrix=mat)

    return pix_image

def is_photo(pix_image, threshold=0.6):
    # Convert to PIL image
    with NamedTemporaryFile(delete=False, suffix='.png') as temp_image:
        pix_image.save(temp_image)

        # Open the image
        img = Image.open(temp_image.name)
        
        # Convert to grayscale
        img_gray = img.convert('L')
        
        # Convert to numpy array
        img_array = np.array(img_gray)

        # Calculate the percentage of white pixels
        white_pixels = np.sum(img_array > 200)

        # Calculate the percentage of white pixels
        total_pixels = img_array.size

        # Calculate the percentage of white pixels
        white_pixel_ratio = white_pixels / total_pixels

        return not (white_pixel_ratio > threshold)

def detect_if_darkmode_image(image, threshold=0.5):
    try:
        # Convert Pillow image to NumPy array
        np_image = np.array(image)

        # Convert to grayscale using OpenCV
        gray_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
        
        if gray_image is None:
            raise ValueError("Could not open the image file.")

        # Normalize pixel values between 0 and 1
        normalized = gray_image / 255.0

        # Calculate the mean pixel intensity
        mean_intensity = np.mean(normalized)

        # If the mean intensity is lower than threshold, assume black background
        return mean_intensity < threshold
    except Exception:
        log_exception()

    return False

def invert_image(input_pil_image):
    return ImageOps.invert(input_pil_image.convert("RGB"))

def ocr_page(pix_image):
    # Convert to PIL image
    with NamedTemporaryFile(delete=False, suffix='.png') as temp_image:
        pix_image.save(temp_image)
        image = Image.open(temp_image.name)
        return ocr_image_pipeline(image)

class OcrStrategy(str, Enum):
    Always = "always"
    Never = "never"
    Auto = "auto"

def pdf_to_text(filepath, strategy_ocr: OcrStrategy, zoom_factor=3.5):
    pdf_document = fitz.open(filepath)

    page_texts = []

    for page_number in range(pdf_document.page_count):
        print(f'Processando página {page_number + 1}', flush=True)

        page = pdf_document.load_page(page_number)
        page_text = page.get_text("text")

        if strategy_ocr == OcrStrategy.Never:
            pass
        elif strategy_ocr == OcrStrategy.Always:
            pix_image = get_pdf_page_as_image(filepath, page_number, zoom_factor)
            page_text = ocr_page(pix_image)
        else:
            pix_image = get_pdf_page_as_image(filepath, page_number, zoom_factor)
            if len(page_text.split(' ')) < 10 or is_photo(pix_image) or strategy_ocr == OcrStrategy.Always:
                page_text = ocr_page(pix_image)

        while '\n\n' in page_text:
            page_text = page_text.replace('\n\n', '\n')

        page_texts.append(page_text)

    return {
        "full_text": "\n".join(page_texts),
        "text_per_page": [{
            "page": idx + 1,
            "text": text
        } for idx, text in enumerate(page_texts)]
    }
