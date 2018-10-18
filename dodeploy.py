#!/usr/bin/env python3
import os
import sys
import argparse
import base64
import hashlib
from colored import fg, bg, attr
from tabulate import tabulate

import dopy.manager
# Monkeypath dopy to fix this exception related to python3, see https://stackoverflow.com/a/34803630
dopy.manager.basestring = str

# Make sure we have a DigitalOcean API key
if 'DO_API_KEY' not in os.environ:
    print("You must have a DigitalOcean API key stored in the DO_API_KEY environment variable")
    sys.exit()
do = dopy.manager.DoManager(None, os.environ['DO_API_KEY'], api_version=2)


def display_droplets(droplets):
    """
    Print out details about droplets in a table.
    """
    table = []
    headers = ['Droplet', 'IP address', 'id', 'Memory', 'Disk', 'Region']

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


def add_ssh_key():
    """
    If the user's ssh key, in ~/.ssh/id_rsa.pub, isn't already in the
    DigitalOcean account, add it. Returns the id of the ssh key.
    """
    # Load the local ssh key
    pubkey_path = os.path.expanduser('~/.ssh/id_rsa.pub')
    try:
        pubkey_text = open(pubkey_path).read()
        pubkey_base64 = pubkey_text.split()[1]
        pubkey_name = pubkey_text.split()[2]
    except:
        print("You must have an ssh key in {}".format(pubkey_path))
        return

    # Calculate the ssh fingerprint (thanks https://stackoverflow.com/a/6682934)
    pubkey = base64.b64decode(pubkey_base64.encode('ascii'))
    pubkey_fingerprint_plain = hashlib.md5(pubkey).hexdigest()
    pubkey_fingerprint = ':'.join(a+b for a,b in zip(pubkey_fingerprint_plain[::2], pubkey_fingerprint_plain[1::2]))

    try:
        # Make sure the ssh key exists in the DigitalOcean account
        ssh_key_id = None
        ssh_keys = do.all_ssh_keys()
        for ssh_key in ssh_keys:
            if ssh_key['fingerprint'] == pubkey_fingerprint:
                ssh_key_id = ssh_key['id']
                break

        # If the ssh key isn't in DigitalOcean, add it
        if not ssh_key_id:
            res = do.new_ssh_key(pubkey_name, pubkey_text)
            ssh_key_id = res['id']
            print("Added your SSH key, '{}' to DigitalOcean".format(pubkey_name))

        return ssh_key_id
    except dopy.manager.DoError as err:
        print(err)
        return None


def list(args):
    """
    List droplets
    """
    try:
        droplets = do.all_active_droplets()
        display_droplets(droplets)
    except dopy.manager.DoError as err:
        print(err)


def create(args):
    """
    Create a new droplet
    """
    ssh_key_id = add_ssh_key()
    if not ssh_key_id:
        return

    try:
        droplet = do.new_droplet(args.name, args.size, args.image, args.region, [ssh_key_id])
        display_droplets([droplet])
    except dopy.manager.DoError as err:
        print(err)


def delete(args):
    """
    Delete a droplet
    """
    print("delete not implemented")


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    list_parser = subparsers.add_parser('list', help='List droplets')
    list_parser.set_defaults(func=list)

    create_parser = subparsers.add_parser('create', help='Create a new droplet')
    create_parser.add_argument('name', help='Name of droplet')
    create_parser.add_argument('--size', default='512mb', help='Size (in RAM) of the droplet (default: 512mb)')
    create_parser.add_argument('--image', default='ubuntu-18-10-x64', help='Base image of the droplet (default: ubuntu-18-10-x64)')
    create_parser.add_argument('--region', default='sfo2', help='Region of the droplet (default: sfo2)')
    create_parser.set_defaults(func=create)

    delete_parser = subparsers.add_parser('delete', help='Delete a droplet')
    delete_parser.set_defaults(func=delete)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
