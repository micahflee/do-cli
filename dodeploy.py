#!/usr/bin/env python3
import os
import sys
import argparse
from dopy.manager import DoManager
from colored import fg, bg, attr
from tabulate import tabulate


# Make sure we have a DigitalOcean API key
if 'DO_API_KEY' not in os.environ:
    print("You must have a DigitalOcean API key stored in the DO_API_KEY environment variable")
    sys.exit()
do = DoManager(None, os.environ['DO_API_KEY'], api_version=2)


def list(args):
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


def create(args):
    print("create not implemented")


def delete(args):
    print("delete not implemented")


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    list_parser = subparsers.add_parser('list', help='List droplets')
    list_parser.set_defaults(func=list)
    create_parser = subparsers.add_parser('create', help='Create a new droplet')
    create_parser.set_defaults(func=create)
    delete_parser = subparsers.add_parser('delete', help='Delete a droplet')
    delete_parser.set_defaults(func=delete)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
