"""ASCII Art generator Click command
"""
import click

from ascii_art.generator import generate_ascii_art_from_img
from ascii_art.io import get_img_from_url
from ascii_art.io import get_img_url_list_from_keyword


@click.command()
@click.argument("keyword")
@click.option("-c", "--cols", default=79, help="Number of columns for ASCII Art.")
@click.option("-s", "--scale", default=0.43, help="Height scale for ASCII Art.")
@click.option(
    "-m",
    "--more-levels",
    default=True,
    help="Whether you want a grayscale of 70 or 10.",
)
def ascii_generator(keyword, cols, scale, more_levels):
    """Shows differents ASCII Art given a keyword

    You can change the number of columns and the scale.
    There are 2 gray scale available 10 and 70 (default is 70)
    """

    img_list = get_img_url_list_from_keyword(keyword)

    for title, url in img_list:
        img = get_img_from_url(url)
        ascii_img = generate_ascii_art_from_img(img, cols, scale, more_levels)

        print("Image name : %s" % title)
        print(ascii_img)

        ans = input("Do you want to keep this image ? (y/n)").lower()

        if ans == "y":
            print("Awesome !")
            exit(0)


if __name__ == "__main__":
    ascii_generator()
