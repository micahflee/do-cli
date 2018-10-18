#!/usr/bin/env python3
import os
import sys
import argparse
import base64
import hashlib
from dopy.manager import DoManager
from colored import fg, bg, attr
from tabulate import tabulate


# Make sure we have a DigitalOcean API key
if 'DO_API_KEY' not in os.environ:
    print("You must have a DigitalOcean API key stored in the DO_API_KEY environment variable")
    sys.exit()
do = DoManager(None, os.environ['DO_API_KEY'], api_version=2)


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


def list(args):
    """
    List droplets
    """
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
    """
    Create a new droplet
    """
    ssh_key_id = add_ssh_key()


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
    create_parser.set_defaults(func=create)
    delete_parser = subparsers.add_parser('delete', help='Delete a droplet')
    delete_parser.set_defaults(func=delete)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
