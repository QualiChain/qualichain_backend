import io

from PIL import Image

from settings import ALLOWED_EXTENSIONS


def image_to_byte_array(image: Image):
    """This function is used to save user avatar to Postgresql"""
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def allowed_file(filename):
    """Allowed formats to be uploaded on QC db"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
