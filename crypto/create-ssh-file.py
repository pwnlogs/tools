#!/usr/bin/env python3

import sys
import base64
import argparse
import yaml
import binascii
from textwrap import wrap




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
    return bytes([int(s[2*i:2*(i+1)], base=16) for i in range(int(l/2))])


def get_formatted(d, t):
    if t == 'int32':
        return str_to_raw(hex(d)[2:].zfill(8))

    elif t == 'int64':
        return str_to_raw(hex(d)[2:].zfill(16))

    elif t == 'str':
        if type(d) == str:
            d = d.encode()
        return get_size(d) + d
    
    elif t == 'mpint':
        d = hex(d)[2:]
        d = d.encode()
        d = str_to_raw(d)
        return get_formatted(d, 'str')


def get_encoded(conf):
    d = b''
    for key in conf:
        if conf[key]['type'] == 'list':
            dd = get_encoded(conf[key]['value'])
            d = d + get_formatted(dd, 'str')
        elif conf[key]['type'] == 'bytes':
            d = d + conf[key]['value'].encode()
        else:
            d = d + get_formatted(conf[key]['value'], conf[key]['type'])
    return d



parser = argparse.ArgumentParser(
                    prog='Modify SSH Public Key',
                    description='Extend an existing SSH-public key',
                    epilog='Text at the bottom of help')

parser.add_argument('-o', '--output-file', default='/dev/stdout')
parser.add_argument('-i', '--input-file', default='file-struct.yaml') 

args = parser.parse_args()

with open(args.input_file) as stream:
    try:
        conf = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

if conf['file-type'] == 'public-key' or conf['file-type'] == 'cert':
    pre_text = conf['pre-text'].encode()
    post_text = conf['post-text'].encode()
    seperator = b' '

elif conf['file-type'] == 'private-key':
    pre_text = b'-----BEGIN OPENSSH PRIVATE KEY-----'
    post_text = b'-----END OPENSSH PRIVATE KEY-----'
    seperator = b'\n'


with open(args.output_file, 'wb') as f:

    data = get_encoded(conf['data'])
    data = base64.b64encode(data)

    if conf['file-type'] == 'private-key':
        data = '\n'.join(wrap(data.decode(), width=70))
        data = data.encode()

    f.write(seperator.join([
        pre_text,
        data,
        post_text
    ]))

