#!/usr/bin/env python

import os
import bcrypt
import getpass
import json
import argparse
import tempfile

def main():
    parser = argparse.ArgumentParser(description='Update the database file.')
    parser.add_argument('username', type=str, help='username')
    parser.add_argument('pwdstore', type=str, help='path to password store')
    args = parser.parse_args()

    password = getpass.getpass("password: ")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    if os.path.exists(args.pwdstore):
        with open(args.pwdstore) as f:
            store = json.load(f)
    else:
        store = []

    def update():
        for x in store:
            if x['email'] == args.username:
                x['bcrypt_password'] = hashed
                return
        store.append(dict(email=args.username, bcrypt_password=hashed))

    update()

    with tempfile.NamedTemporaryFile(dir='.', delete=False) as f:
        json.dump(store, f, indent=4)
        f.close()
        os.rename(f.name, args.pwdstore)


if __name__ == '__main__':
    main()
