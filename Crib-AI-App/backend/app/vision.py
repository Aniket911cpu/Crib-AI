import os
from PIL import ImageGrab
import pytesseract
import base64
from io import BytesIO

# Configuration
# Point to tesseract executable if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class VisionEngine:
    def __init__(self):
        self.last_ocr_text = ""

    def capture_full_screen(self):
        """Captures the entire primary screen."""
        try:
            screenshot = ImageGrab.grab()
            return screenshot
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None

    def capture_region(self, bbox):
        """
        Captures a specific region.
        bbox = (left, top, right, bottom)
        """
        try:
            screenshot = ImageGrab.grab(bbox=bbox)
            return screenshot
        except Exception as e:
            print(f"Error capturing region: {e}")
            return None

    def extract_text(self, image):
        """
        Extracts text from an image using Tesseract OCR (Local).
        """
        try:
            text = pytesseract.image_to_string(image)
            self.last_ocr_text = text.strip()
            return self.last_ocr_text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

    def encode_image_base64(self, image):
        """Encodes PIL image to base64 for LLM usage."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

if __name__ == "__main__":
    # Test
    vision = VisionEngine()
    img = vision.capture_full_screen()
    if img:
        print("Screen captured successfully.")
        # text = vision.extract_text(img)
        # print(f"OCR Result: {text[:100]}...")
