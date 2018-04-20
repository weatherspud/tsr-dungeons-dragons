#!/usr/bin/env python3
import argparse
import collections
import csv
import sys


def stats(stats, input_path, fout):
    data = []

    with open(input_path) as f:
        header = None
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if header:
                data.append(dict(zip(header, row)))
            else:
                header = row

    _stats = collections.defaultdict(dict)
    for datum in data:
        for stat in stats:
            _stats[stat][datum[stat]] = _stats[stat].get(datum[stat], 0) + 1

    fout.write('total: {}\n\n'.format(len(data)))

    for stat in stats:
        fout.write(stat)
        fout.write('\n')
        for key in sorted(_stats[stat].keys()):
            key_or_none = '<none>' if not key else key
            fout.write('\t'.join([key_or_none, str(_stats[stat][key])]))
            fout.write('\n')
        fout.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', '-i',
                        dest='input_path',
                        required=True)
    parser.add_argument('--stats', '-s',
                        dest='stats',
                        nargs='+',
                        required=True)
    args = parser.parse_args()

    stats(args.stats, args.input_path, sys.stdout)
