#!/usr/bin/env python3

import sys
import base64
import argparse

parser = argparse.ArgumentParser(
                    prog='Modify SSH Public Key',
                    description='Extend an existing SSH-public key',
                    epilog='Text at the bottom of help')

parser.add_argument('-f', '--filename', default='/dev/stdout') 
parser.add_argument('-e', '--exponent', help='value in hex: 0x1001 or int:123') 
parser.add_argument('-n', '--modulus', help='value in hex') 
parser.add_argument('-c', '--comment') 

args = parser.parse_args()


def get_size(s):
    # get size of string
    return str_to_raw(hex(len(s))[2:].zfill(8).encode())


def str_to_raw(s):
    # convert '14231' to '\x01\x42\x31'
    # add a zero to left if the length is odd
    l = len(s)
    if l % 2 == 1:
        l += 1
        s = b'0' + s
    return b''.join([
            chr(int(s[2*i:2*(i+1)], base=16)).encode() for i in range(int(l/2))
        ])


def get_formatted_str(d, t):
    if t == 'int32':
        return str_to_raw(hex(d)[2:].zfill(8))

    elif t == 'int64':
        return str_to_raw(hex(d)[2:].zfill(16))

    elif t == 'str':
        return get_size(d) + d
    
    elif t == 'mpint':
        d = str_to_raw(d)
        return get_formatted_str(d, 'str')


with open(args.filename, 'wb') as f:
    # https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys
    '''
    RSA certificate

    string    "ssh-rsa"
    mpint     e
    mpint     n
    '''

    data = b''

    e = args.exponent[2:] if args.exponent.startswith('0x') else hex(int(args.exponent))[2:]
    n = args.modulus[2:] if args.modulus.startswith('0x') else hex(int(args.modulus))[2:]

    data += get_formatted_str(b'ssh-rsa', 'str')
    data += get_formatted_str(e.encode(), 'mpint')
    data += get_formatted_str(n.encode(), 'mpint')

    data = base64.b64encode(data)

    f.write(b' '.join([
        b'ssh-rsa',
        data,
        args.comment.encode()
    ]))

