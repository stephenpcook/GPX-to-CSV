#! python

import sys
import argparse

from bs4 import BeautifulSoup


__version__ = '0.1.0'


def gpx_to_csv(xml_input, header=None):
    if header is None:
        header = True

    soup = BeautifulSoup(xml_input, 'xml')

    if header:
        csv_string = 'UTC,lat,lon\n'
    else:
        csv_string = ''

    for pt in soup.find_all('trkpt'):
        csv_string += '{},{},{}\n'.format(pt.time.text, pt['lat'], pt['lon'])

    return csv_string


def get_arguments(args):
    parser = argparse.ArgumentParser(description=(
        'Extract trackpoints from a GPX file into a CSV format.'))
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        help='GPX input file; if omitted, read from stdin',
                        default=sys.stdin)
    parser.add_argument('-v', '--version', action='store_true',
                        help='output version information and exit')
    parser.add_argument('--no-header', dest='header', action='store_false',
                        help='Do not include a header in the output CSV')
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
                        help='CSV output file; if omitted, write to stdout',
                        default=sys.stdout)
    return parser.parse_args(args)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = get_arguments(argv)

    if args.version:
        print(__version__)
        return

    with args.infile as f:
        xml_input = f.read()

    csv_out = gpx_to_csv(xml_input, header=args.header)

    with args.outfile as f:
        f.write(csv_out)


if __name__ == "__main__":
    sys.exit(main())
