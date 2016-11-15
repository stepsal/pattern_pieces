from PIL import Image, ImageEnhance
from random import randint
import itertools
import argparse
import os
import binascii

BLOCK_SIZE = 0
NO_OF_PIECES = 0
SAVE_IMAGE = True
INPUT_DIR = ""
image_formats = ['.jpg', '.jpeg', '.png', '.tif', '.bmp', 'gif', 'tiff']
OUTPUT_FORMAT = '.png'


def get_all_images_from_the_input_dir(input_dir):
    images = []
    for file in os.listdir(input_dir):
        filepath = os.path.join(input_dir, file)
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1].lower() in image_formats:
                img = Image.open(filepath)
                images.append(img)
    return images


def blocks(width, height, n):
    for x in range(0, width, n):
        for y in range(0, height, n):
            if (x + n > width) or (y + n > height):
                continue
            yield (x, y, x+n, y+n)


def create_image(images, block_size, no_of_pieces):
    image_pieces = []
    images_cycle = itertools.cycle(images)
    side_size = 1000 - (1000 % block_size)
    output_image = Image.new('RGB', (side_size, side_size))
    while len(image_pieces) <= no_of_pieces:
        img = next(images_cycle)
        h, w = img.size
        randh = randint(0, h - block_size)
        randw = randint(0, w - block_size)
        coords = (randh, randw, randh + block_size, randw + block_size)
        piece = img.crop(coords)
        image_pieces.append(piece)
    pieces_cycle = itertools.cycle(image_pieces)
    for section in blocks(1000, 1000, block_size):
        output_image.paste(next(pieces_cycle), section)
    return output_image


def save_image(image):
    random_hash = str(binascii.b2a_hex(os.urandom(15)))[2:-1]
    output_image_name = "pattern_pieces_" + random_hash + "_" + OUTPUT_FORMAT
    output_dir = "output"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir_path = os.path.join(script_dir, output_dir)
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    image_path = os.path.join(output_dir_path, output_image_name)
    print("Image saved to {0}".format(image_path))
    image.save(image_path)


def main():
    images = get_all_images_from_the_input_dir(INPUT_DIR)
    output_image = create_image(images, BLOCK_SIZE, NO_OF_PIECES)
    output_image.show()
    if SAVE_IMAGE:
        save_image(output_image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pattern Pieces Art Generator')
    parser.add_argument("-b", "--blocksize", dest="BLOCK_SIZE", default=20, type=int, help="Block Size")
    parser.add_argument("-p", "--pieces", dest="NO_OF_PIECES", default=200, type=int, help="Number of Pieces")
    parser.add_argument("-i", "--input", dest="INPUT_DIR", \
                        default="/home/stephen.salmon/Pictures/pattern_pieces/", help="input directory")
    try:
        args = parser.parse_args()
    except:
        print("Args Error")
        parser.print_help()
        exit(2)

    if args.BLOCK_SIZE:
        BLOCK_SIZE = int(args.BLOCK_SIZE)
    if args.NO_OF_PIECES:
        NO_OF_PIECES = args.NO_OF_PIECES
    if args.INPUT_DIR:
        if os.path.isdir(args.INPUT_DIR):
            INPUT_DIR = args.INPUT_DIR
        else:
            print("Not a valid input directory")
            parser.print_help()
            exit(2)
    main()
