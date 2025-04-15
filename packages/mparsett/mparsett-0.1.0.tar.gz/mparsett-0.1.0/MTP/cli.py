import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Parse filename or torrent name using Parsett")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse a filename or torrent name')
    parse_parser.add_argument('filename', type=str, help="The name of the file or torrent to be parsed")

    args = parser.parse_args()

    if args.command == 'parse':
        if not args.filename:
            parser.print_help()
            sys.exit(1)

        from MTP import parse_music_title
        result = parse_music_title(args.filename)
        print(json.dumps(result, indent=4))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
