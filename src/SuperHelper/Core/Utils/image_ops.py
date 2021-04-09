import io
import logging

from PIL import Image, UnidentifiedImageError

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)


class ImageOps:
    @staticmethod
    def open_image(file: io.IOBase):
        try:
            return Image.open(file)
        except UnidentifiedImageError as e:
            logger.exception("Not an image file!")
            raise
        except OSError:
            logger.exception("Unable to read file!")
            raise

    @staticmethod
    def show_image(image: Image.Image, title: str = "Demo") -> None:
        image.show(title)


__all__ = ["ImageOps"]
