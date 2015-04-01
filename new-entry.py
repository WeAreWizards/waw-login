#!/usr/bin/env python

import bcrypt
import getpass
import json

email = raw_input("email: ")
password = getpass.getpass("password: ")
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print "add the following entry to your database:"
print json.dumps(dict(email=email, bcrypt_password=hashed))
