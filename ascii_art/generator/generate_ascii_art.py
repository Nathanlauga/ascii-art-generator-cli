"""ASCII Art generator functions

Based on https://www.geeksforgeeks.org/converting-image-ascii-image-python/
"""
import numpy as np

GRAY_SCALE_70 = (
    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
)
GRAY_SCALE_10 = "@%#*+=-:. "


def get_average(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.average(im.reshape(w * h))


def generate_ascii_art_from_img(image, cols=70, scale=0.43, more_levels=True) -> str:
    """Generate a string of a ASCII Art given an image

    Parameters
    ----------
    image : Image
        PIL Image (gray scale)
    cols : int, optional
        Number of columns for the output, by default 70
    scale : float, optional
        Scale for the height, by default 0.43
    more_levels : bool, optional
        Whether you want 70 gray scales or 10, by default True

    Returns
    -------
    str
        ASCII Art string
    """
    # store dimensions
    W, H = image.size[0], image.size[1]
    # compute width of tile
    w = W / cols
    # compute tile height based on aspect ratio and scale
    h = w / scale
    # compute number of rows
    rows = int(H / h)

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    aimg = []

    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        # correct last tile
        if j == rows - 1:
            y2 = H

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(get_average(img))

            # look up ascii char
            if more_levels:
                gsval = GRAY_SCALE_70[int((avg * 69) / 255)]
            else:
                gsval = GRAY_SCALE_10[int((avg * 9) / 255)]

            # append ascii char to string
            aimg[j] += gsval

    # Convert as string
    aimg = "\n".join(aimg)

    # return txt image
    return aimg
