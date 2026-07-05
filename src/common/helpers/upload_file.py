from imagekitio import ImageKit

from common.config.env_config import IMAGEKIT_PRIVATE_KEY, IMAGEKIT_PUBLIC_KEY, IMAGEKIT_URL_ENDPOINT

imagekit = ImageKit(private_key=IMAGEKIT_PRIVATE_KEY)

def upload_file(file_byte: bytes, file_name: str, folder: str, content_type: str = "image/jpeg/png") -> str:
    """ Uploads a file to ImageKit and returns the CDN URL of the uploaded file. """
    response = imagekit.files.upload(
        file = (file_byte, file_name, content_type),
        file_name = file_name,
        folder = folder,
        is_private_file = False,
        use_unique_file_name = True,
    )

    return response.url