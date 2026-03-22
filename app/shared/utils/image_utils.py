from PIL import Image
import io


def pil_image_to_png_bytes(image: Image.Image):

    buffer = io.BytesIO()

    image.save(buffer, format="PNG")

    return buffer.getvalue()