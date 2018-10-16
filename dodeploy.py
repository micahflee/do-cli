#!/usr/bin/env python3
import os
import sys
import argparse
from dopy.manager import DoManager
from colored import fg, bg, attr
from tabulate import tabulate


def main():
    # Make sure we have a DigitalOcean API key
    if 'DO_API_KEY' not in os.environ:
        print("You must have a DigitalOcean API key stored in the DO_API_KEY environment variable")
        sys.exit()
    do = DoManager(None, os.environ['DO_API_KEY'], api_version=2)

    # Parse arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', action="store_true", help="List droplets")
    group.add_argument('--create', action="store_true", help="Create a new droplet")
    group.add_argument('--delete', action="store_true", help="Delete a droplet")
    args = parser.parse_args()

    if args.list:
        table = []
        headers = ['Droplet', 'IP address', 'id', 'Memory', 'Disk', 'Region']

        droplets = do.all_active_droplets()
        for droplet in droplets:
            table.append([
                "{}{}{}".format(attr('bold'), droplet['name'], attr('reset')),
                droplet['ip_address'],
                droplet['id'],
                droplet['memory'],
                droplet['disk'],
                droplet['region']['slug']
            ])
        print(tabulate(table, headers=headers))
        print("")

    elif args.create:
        pass

    elif args.delete:
        pass

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
