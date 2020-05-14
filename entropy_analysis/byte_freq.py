import os
import sys
import matplotlib.pyplot as plot 


freq = {}

def run_process():
    os.system(r'python3 main.py -f example.sc > .temp && tail -n +2 .temp > output.sc && rm .temp')


def read_file(filename):
    builder = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            builder.append(line.strip())
    return ''.join(builder)


def plot_graph():
    plot.bar(list(freq.keys()), freq.values(), color='b')
    plot.suptitle('Hex (in decimal) vs. Frequency', fontsize=16)
    plot.xlabel('Hex (in decimal)', fontsize=12)
    plot.ylabel('Frequency', fontsize=12)
    plot.show()


def main():
    owd = os.getcwd()
    os.chdir('..')
    for i in range(1024):
        print('Iteration', i)
        run_process()
        builder = read_file('output.sc')
        hexes = [builder[j:j+2] for j in range(0, len(builder), 2)]
        for _hex in hexes:
            dec = int(_hex, 16)
            if dec > 255 or dec < 0:
                print('Decimal is not between 0 and 255.')
                sys.exit(1)
            freq.setdefault(dec, 0);
            freq[dec] += 1
    os.chdir(owd)
    plot_graph()


main()
