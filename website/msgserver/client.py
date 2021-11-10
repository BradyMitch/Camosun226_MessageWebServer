#!/usr/bin/python3

import requests
import sys
import random

HOST = ''
PORT = 12345

KEY_SIZE = 8
GETKEY_OFFSET = 28
REQ_ARGS = 3
ERROR_MSG = "Error: needs 2 arguments (URL, KEY)"
HTTP = "http://"

# PURPOSE:
# If program run without 2 command line arguments (URL and KEY),
# give error message and exit.
#
if len(sys.argv) != REQ_ARGS:
    print(ERROR_MSG)
    sys.exit(-1)

URL = sys.argv[1]
KEY = sys.argv[2]

# PURPOSE:
# Generate an 8 digit random key
# This is a numeric key, but could be changed to alphanumeric
#
# RETURN/NOTES:
# Returns string of 8 digit numeric key
#
def gen_key():
    range_start = 10**(KEY_SIZE-1)
    range_end = (10**KEY_SIZE)-1
    return str(random.randint(range_start, range_end))

# PURPOSE:
# Get message using initial KEY, if there is a message display it,
# grab the first 8 characters of msg to use as next KEY, repeat until
# no message is given.
# Then ask user to input a message. Attach a random key at the start of this
# new message using gen_key(). Create a new key-value pair using this message
# and the last KEY (the one that didnt return a message). Exit.
#
# PARAMETERS:
# URL for msgserver from command line argument 1
# KEY (initial key) from command line argument 2
#
# RETURN/NOTES:
# Ends after user creates a message for the last KEY.
# Note: keyStr removes first 28 characters from msg string,
# the next line takes the first 8 characters of that string as the next KEY
#
def client(URL, KEY):
    while(True):
        data = requests.get(HTTP + URL + "/get/" + KEY)
        msg = data.text

        if len(msg) > KEY_SIZE:
            msg = msg.strip()
            keyStr = msg[GETKEY_OFFSET:]
            KEY = keyStr[0:KEY_SIZE]
            print(msg)
        elif len(msg) == 0:
            break
    
    clientToken = requests.session()
    NEXT_KEY = gen_key()
    inputMsg = str(input("Enter a message: "))
    message = NEXT_KEY + ''.join(inputMsg)
    clientToken.get(HTTP + URL + "/create")
    dictionary = {"key": KEY, "msg": message, "csrfmiddlewaretoken": clientToken.cookies['csrftoken']}
    post = clientToken.post(HTTP + URL + "/create", data = dictionary)

client(URL, KEY)