import io
import uuid
from PIL import Image


def upload_thumbnails(thumbnails, supabase):
    """
    Uploads thumbnail images to Supabase Storage and returns their URLs.

    Parameters:
        thumbnails (List[FileUploader]): A list of thumbnail images.

    Returns:
        List[str]: A list of thumbnail URLs.
    """
    thumbnail_urls = []
    for thumbnail in thumbnails:
        resized_io, preview_img = resize_image_keep_alpha(thumbnail)

        file_path = f"thumbnails/{uuid.uuid4()}.png"
        supabase.storage.from_("product-media").upload(
            file_path,
            resized_io.getvalue(),
            {"content-type": "image/png"}
        )

        thumbnail_url = supabase.storage.from_(
            "product-media").get_public_url(file_path)
        thumbnail_urls.append(thumbnail_url)

    return thumbnail_urls


def upload_description_images(thumbnails, supabase):
    """
    Uploads thumbnail images to Supabase Storage and returns their URLs.

    Parameters:
        thumbnails (List[FileUploader]): A list of thumbnail images.

    Returns:
        List[str]: A list of thumbnail URLs.
    """
    thumbnail_urls = []
    for thumbnail in thumbnails:
        resized_io, preview_img = resize_image_keep_alpha(thumbnail)

        file_path = f"description_images/{uuid.uuid4()}.{preview_img.format.lower()}"
        supabase.storage.from_("product-media").upload(
            file_path,
            resized_io.getvalue(),
            {"content-type": "image/png"}
        )

        thumbnail_url = supabase.storage.from_(
            "product-media").get_public_url(file_path)
        thumbnail_urls.append(thumbnail_url)

    return thumbnail_urls


def resize_image_keep_alpha(image_file):
    MAX_WIDTH = 1280
    MAX_HEIGHT = 720
    img = Image.open(image_file)

    # Resize while maintaining aspect ratio
    img.thumbnail((MAX_WIDTH, MAX_HEIGHT))

    # Save to PNG in-memory
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return buffer, img
