import os

from io import BytesIO
from django.core.files import File
from PIL import Image


def make_thumbnail(image, size=(100, 100), filename=''):
    """Makes thumbnails of given size from given image"""
    if image:
        pil_image = Image.open(image).convert('RGB')
        pil_image.thumbnail(size)  # resize image
        # pil_image.convert('RGB') # convert mode
        thumb_io = BytesIO()  # create a BytesIO object
        pil_image.save(thumb_io, 'JPEG', quality=85)  # save image to BytesIO object
        thumbnail = File(thumb_io, name=filename)  # create a django friendly File object

        return thumbnail
    return None


def make_thumbnail_and_set_for_model(obj, image_fied, thumb_field):
    if image := getattr(obj, image_fied, None):
        cover_filename = os.path.basename(getattr(image, 'name', ''))
        image_thumbnail = getattr(obj, thumb_field, None)
        try:
            if not image_thumbnail or cover_filename != os.path.basename(
                    getattr(image_thumbnail, 'name', '')):
                setattr(obj, thumb_field, make_thumbnail(image, size=(150, 150), filename=cover_filename))
        except IOError:
            # aqui a imagem nao existe.
            pass


def compress_image_size(size: int, file_path: str) -> None:
    """
    Comprime a imagem até ficar menor que o tamanho passado por parâmetro
    Args:
        size: Tamanho limite desejado
        file_path: path para a imagem

    Returns: None
    """
    # Pegando o tamanho inicial da imagem. Se já estiver dentro do limite, não fazemos nada
    current_size = os.stat(file_path).st_size
    if current_size <= size:
        return
    picture = Image.open(file_path)
    # Começamos com redução para 90% de qualidade
    quality = 90
    # Enquanto a foto for maior que o limite
    while current_size > size:
        # Se a qualidade cair pra menor que 0, defina-a como 5%
        if quality <= 0:
            quality = 5
        # Comprime a imagem para a qualidade definida
        picture.save(file_path, optimize=True, quality=quality)
        current_size = os.stat(file_path).st_size
        # Diminui a qualidade em que a imagem será comprimida em 15%
        quality -= 15
