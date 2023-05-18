import numpy as np
from sys import argv
from PIL import Image
from math import floor
from random import randrange
from alive_progress import alive_bar

filters = {
    "+red": lambda px: px[0],
    "+grn": lambda px: px[1],
    "+blu": lambda px: px[2],
    "+sat": lambda px: 0 if sorted(px)[-1] == 0 else int(255*(sorted(px)[-1] - sorted(px)[0]) / sorted(px)[-1]),
    "+val": lambda px: sorted(px)[-1],
    "+brg": lambda px: int((px[0] + px[1] + px[2])/3),
    "+lum": lambda px: int((0.299*px[0]**2 + 0.587*px[1]**2 + 0.114*px[2]**2)**0.5),
    "+rnd": lambda px: randrange(0, 255),
    "-red": lambda px: -px[0],
    "-grn": lambda px: -px[1],
    "-blu": lambda px: -px[2],
    "-sat": lambda px: 0 if sorted(px)[-1] == 0 else -int(255*(sorted(px)[-1] - sorted(px)[0]) / sorted(px)[-1]),
    "-val": lambda px: -sorted(px)[-1],
    "-brg": lambda px: -int((px[0] + px[1] + px[2])/3),
    "-lum": lambda px: -int((0.299*px[0]**2 + 0.587*px[1]**2 + 0.114*px[2]**2)**0.5),
    "-rnd": lambda px: -randrange(0, 255),
}

def get_image_data(image_file: str):
    """Takes file name of image and returns image size and list of pixels."""
    img = Image.open(image_file)
    pixel_list = list(img.getdata())
    return img.size, pixel_list

def get_lines(pixel_list: list, image_size: tuple, vertical: bool = False):
    """Takes a list of pixel values and returns a 2d list of pixels."""
    w, h = image_size
    if vertical:
        return [[pixel_list[b + a*w] for a in range(h)] for b in range(w)]
    else:
        return [[pixel_list[a + b*w] for a in range(w)] for b in range(h)]

def export(img: list, image_size: tuple, name: str):
    """Exports the image."""
    print("\rExporting.", end="")
    w, h = image_size
    if len(img[0]) == w:
        pass
    elif len(img[0]) == h:
        img = [[img[a][b] for a in range(w)] for b in range(h)]
    else:
        img = [[img[a + b*w] for a in range(w)] for b in range(h)]

    Image.fromarray(np.array(img, dtype=np.uint8)).save(name)

def split_lines(cmd, image, _filter, count):
    """Splits lines with specified filter."""
    with alive_bar(len(image), title=cmd, title_length=20, spinner=None, refresh_secs=0.1) as bar:
        for b in range(len(image)):
            temp = []
            last = -1
            for a in image[b]:
                if floor((_filter(a) * count) / 256) != last:
                    last = floor((_filter(a) * count) / 256)
                    temp.append([])
                temp[-1].append(a)
            image[b] = temp
            bar()
    return image

def unpack_lines(image):
    """Undoes split_lines."""
    print("\rUnpacking.", end="")
    for a in range(len(image)):
        raw = list(str(image[a]).replace("[", "").replace("]", "")
                   .replace("(", "").replace(")", "").replace(" ", "").split(","))
        image[a] = [(int(raw[_]), int(raw[_ + 1]), int(raw[_ + 2])) for _ in range(0, len(raw), 3)]
    return image

def sort_image(cmd, image, _filter, div, rem):
    """Sorts streaks."""
    with alive_bar(len(image), title=cmd, title_length=20, spinner=None, refresh_secs=0.1) as bar:
        for b in image:
            for c in range(len(b)):
                if c % div == rem:
                    b[c] = sorted(b[c], key=_filter)
            bar()
    return image

def main(script: str):
    """Interpreter for fň"""
    a, size, out_file = 0, 0, "out.jpg"
    for line in open(script, "r"):
        command = line.split(";")[:-1][0].replace(" ", "").lower()

        # File names
        if "->" in command:
            if a != 0:
                a = unpack_lines(a)
                export(a, size, out_file)
            in_file, out_file = command.split("->")
            print(f"\r{'-'*102}\n{in_file: >49} -> {out_file: <49}\n{'-'*102}")
            size, a = get_image_data(in_file)
            continue

        if command == "":
            continue
        elif ":" in command:
            command, args = command.split(":")
            args = args.split(",")
            prnt = f"{command}: {str(args)[1:-1]}".replace("'", "")
        else:
            args = []
            prnt = command

        # Lines
        if command == "hor":
            print("hor")
            a = get_lines(a, size)

        # Columns
        elif command == "vrt":
            print("vrt")
            a = get_lines(a, size, True)

        # Splitting
        elif command == "spl":
            a = unpack_lines(a)
            a = split_lines(prnt, a, filters[args[0]], int(args[1]))

        # Sorting
        elif command == "srt":
            if args[1].lower() != "a":
                a = sort_image(prnt, a, filters[args[0]], int(args[1]), int(args[2]))
            else:
                a = sort_image(prnt, a, filters[args[0]], 1, 0)

    a = unpack_lines(a)
    export(a, size, out_file)
    print("\r            ")

if __name__ == "__main__":
    main(argv[1])
