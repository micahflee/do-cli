#!/usr/bin/env python3
import argparse
import dopy

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', action="store_true", help="List DigitalOcean droplets in the 'ctf' project")
    group.add_argument('--create', action="store_true", help="Create a new droplet")
    group.add_argument('--delete', action="store_true", help="Delete a droplet")
    args = parser.parse_args()

    if args.list:
        pass

    elif args.create:
        pass

    elif args.delete:
        pass

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
