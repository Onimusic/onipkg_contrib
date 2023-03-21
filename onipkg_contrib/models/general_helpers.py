from django.db.models.fields.files import ImageFieldFile
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from contrib.log_helper import log_error


def default_get_youtube_embedded(youtube_video_id: str) -> str:
    """
    Código de embedded do youtube. Retorna apenas se tiver video_id
    Args:
        youtube_video_id: Id do vídeo a ser embedado
    Returns: html do vídeo embedado, caso haja video_id
    """
    if youtube_video_id:
        return format_html("""<div class="embed-responsive embed-responsive-16by9"> <iframe id="ytplayer"
        type="text/html" autoplay="true" src="https://www.youtube.com/embed/{}"  allow="accelerometer; autoplay; 
        encrypted-media; gyroscope; picture-in-picture" frameborder="0"></iframe></div>""".format(
            youtube_video_id))
    return "N/A"


def get_thumb_with_image_download_url(image: ImageFieldFile, thumb: ImageFieldFile, width: int = 100) -> str:
    """
    Retorna o html da imagem passada como parametro envolta de um elemento a, para que a imagem seja clicavel
    Args:
        image: arquivo da imagem
        thumb: arquivo da imagem
        width: tamanho inteiro representando a largura da imagem desejada
    Returns: string html
    """
    try:
        return format_html(
            '<a href={url} target="_blank"><img src={thumb_url} style="max-width: {width}px;"></a>'.format(
                url=image.url, thumb_url=thumb.url, width=width))
    except ValueError:
        return format_html(
            '<a href={url} target="_blank"><img src={thumb_url} style="max-width: {width}px;"></a>'.format(
                url=static('img/no_cover.png'), thumb_url=static('img/no_cover.png'), width=width))


def generic_slug_generator(model, text, field_name='slug'):
    """
    Gera um slug único para o modelo especificado
    Args:
        model: Modelo cujo objeto receberá o slug. Usado para garantir que não ocorram slugs iguais neste modelo
        text: Texto base que será escapado e possivelmente alterado aleatoriamente para gerar um slug único
        field_name: Nome do campo do slug no modelo. Por default é "slug"

    Returns:
        String única pra ser usada como slug
    """
    from random import choice as choice  # Pra não importar o pacote inteiro
    from unidecode import unidecode
    appendable_chars = '0123456789#@!*_-'
    temp_slug = ''.join(char for char in text.title() if not char.isspace())
    # A linha abaixo possibilita filtragem com base no nome do campo que contém o slug no modelo, qualquer que ele seja
    filter_query = {field_name: temp_slug}
    try:
        # Checagem de unicidade do slug no modelo especificado, com base no nome do campo
        while model.objects.filter(**filter_query).exists():
            temp_slug += choice(appendable_chars)
            filter_query[field_name] = temp_slug
    except AttributeError as e:  # Se o nome do campo do slug não for "slug", simplesmente retornamos a string
        log_error(e)
        pass
    return unidecode(temp_slug)


def get_unique_filename(filename: str) -> str:
    """
    Gera um nome aleatório único para os arquivos que serão salvos no bucket. Pegamos a data e hora atuais e convertemos
        para hexadecimal para gerar um filename garantidamente único.
    Args:
        filename: nome do arquivo que o usuário submeteu. Usado apenas para pegar a extensão do arquivo.

    Returns:
        String para ser usada como nome do arquivo.
    """
    from contrib.exceptions import InvalidFileNameError
    from datetime import datetime
    spliced_old_name = filename.split('.')
    if len(spliced_old_name) <= 1:
        raise InvalidFileNameError(_('Nome do arquivo não possui a extensão.'))
    extension = spliced_old_name[-1]
    return f'{hex(int(datetime.utcnow().strftime("%Y%m%d%H%M%S%f")))}.{extension}'


def generic_get_file_path(identifier: str, path: str, filename: str) -> str:
    """
    Método genérico para gerar filepaths para os arquivos que são salvos no sistema.
    Args:
        identifier: identificador único do objeto em que o arquivo está sendo salvo
        path: path para o diretório do arquivo
        filename: nome do arquivo que está sendo submetido pelo usuário

    Returns:
        Path final pro arquivo.
    """
    return f'{path}/{identifier}/{get_unique_filename(filename)}'
