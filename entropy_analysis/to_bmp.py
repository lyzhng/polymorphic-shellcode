import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from random import randrange

matrix = []


def run_process():
    os.system(r'python3 main.py -f example.sc > .temp && tail -n +2 .temp > output.sc && rm .temp')


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
    # plt.axis('off')
    plt.savefig('pict.png', bbox_inches='tight', pad_inches = 0)
    # plt.gca().set_axis_off()
    # plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    # plt.margins(0,0)
    plt.show()


def main():
    owd = os.getcwd()
    os.chdir('..')
    for i in range(50):
        print('Iteration', i)
        run_process()
        hexes = read_file('output.sc')
        dec = [int(h, 16) for h in hexes]
        matrix.append(dec)
    print(f'The length of the matrix is {len(matrix)}')
    os.chdir(owd)
    display_image()

main()
