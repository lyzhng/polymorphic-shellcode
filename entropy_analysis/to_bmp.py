import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from random import randrange

matrix = []


def run_process():
    os.system('make clean && make')


def read_file(filename):
    builder = []
    count = 0
    with open(filename, 'r') as f:
        while count != 2048:
            _hex = f.read(2)
            if not _hex:
                break
            builder.append(_hex)
            count += 2
    return builder


def display_image():
    im = np.array(matrix)
    # im = np.matrix(matrix)
    plt.imshow(im, cmap='gray')
    plt.axis('off')
    plt.savefig('pict.png', bbox_inches='tight', pad_inches = 0)
    # plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.show()


def main():
    for i in range(512):
        # run_process()
        # hexes = read_file('hex_copy.txt')
        hexes = []
        hexes = [randrange(0, 255) for j in range(1024)]
        # dec = [int(_hex, 16) for _hex in hexes]
        matrix.append(hexes)
        print(f'The length of each row is {len(hexes)}')
    print(f'The length of the matrix is {len(matrix)}')
    display_image()

main()
