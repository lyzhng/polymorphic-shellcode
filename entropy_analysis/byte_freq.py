import os
import matplotlib.pyplot as plot 


freq = {}

def run_process():
    # need to apply substitution to the program here
    os.system(r'for i in `objdump -D -EL output | tr "\t" " " | tr " " "\n" | egrep "^[0-9a-f]{2}$"`; do echo -n "$i"; done > hex.txt')


def read_file(filename):
	builder = []
	with open(filename, 'r') as f:
		for line in f.readlines():
			line = line.strip()
			builder.append(line.strip())
	return ''.join(builder)


def plot_graph():
	plot.bar(list(freq.keys()), freq.values(), color='b')
	plot.show()


def main():
	for i in range(1):
		run_process()
		builder = read_file('hex.txt');
		hexes = [builder[j:j+2] for j in range(0, len(builder), 2)]
		# print(hexes)
		for _hex in hexes:
			dec = int(_hex, 16)
			if dec > 255 or dec < 0:
				print('Decimal is not between 0 and 255.')
				return
			freq.setdefault(dec, 0);
			freq[dec] += 1
	plot_graph()


main()
