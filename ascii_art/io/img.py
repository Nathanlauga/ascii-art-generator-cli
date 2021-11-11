from io import BytesIO

from PIL import Image

from .scrap import get_data_from_url


def get_img_from_url(url: str) -> Image:
    """Returns a gray image given an url

    Parameters
    ----------
    url : str
        Url where the image is

    Returns
    -------
    Image
        Gray image
    """
    ans = get_data_from_url(url)
    # Open as grayscale
    img = Image.open(BytesIO(ans.content)).convert("L")

    return img
