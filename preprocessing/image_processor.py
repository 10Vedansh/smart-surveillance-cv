import cv2


class ImageProcessor:
    """Preprocesses frames using resizing, denoising and contrast enhancement."""

    def __init__(self, output_width: int = 640):
        if output_width <= 0:
            raise ValueError("output_width must be positive")
        self.output_width = output_width

    def resize(self, image):
        height, original_width = image.shape[:2]
        if original_width == self.output_width:
            return image.copy()
        ratio = self.output_width / original_width
        new_height = max(1, int(height * ratio))
        return cv2.resize(image, (self.output_width, new_height), interpolation=cv2.INTER_AREA)

    @staticmethod
    def grayscale(image):
        if len(image.shape) == 2:
            return image.copy()
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def denoise(image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    @staticmethod
    def enhance_contrast(image):
        gray = ImageProcessor.grayscale(image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(gray)

    @staticmethod
    def edges(image):
        gray = ImageProcessor.grayscale(image)
        return cv2.Canny(gray, 80, 160)

    def process(self, image):
        resized = self.resize(image)
        denoised = self.denoise(resized)
        enhanced = self.enhance_contrast(denoised)
        edge_map = self.edges(enhanced)
        return {
            "resized": resized,
            "denoised": denoised,
            "enhanced": enhanced,
            "edges": edge_map,
        }
