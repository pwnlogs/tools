#!/usr/bin/env python3

import sys
import base64


def get_next_element(data, i, dtype):
    if dtype == 'string':
        l = int.from_bytes(data[i:i+4], "big", signed=False)
        # print('l: %x' % l, flush=True)
        i += 4
        content = data[i:i+l]
        i += l
        return content, i
    
    elif dtype == 'uint64':
        content = int.from_bytes(data[i:i+8], "big", signed=False)
        i += 8
        return content, i
    
    elif dtype == 'uint32':
        content = int.from_bytes(data[i:i+4], "big", signed=False)
        i += 4
        return content, i

def print_as_string(k, v, decode_bytes=True):
    if decode_bytes and type(v) == bytes:
        v = v.decode()
    print('%s: %s' % (k, v), flush=True)

def print_as_int(k, v, hex=False):
    format = '%s: 0x%x' if hex else '%s: %d' 
    if type(v) == int:
        print(format % (k, v), flush=True)
    else:
        print(format % (k, int.from_bytes(v, 'big', signed=False)), flush=True)


if len(sys.argv) > 2:
    print('Usage: parse-pem <pem-file>\nOr use it with stdin (echo "content" | parse-pem)')

if len(sys.argv) == 1:
    input_file = '/dev/stdin'
else:
    input_file = sys.argv[1]

with open(input_file, 'rb') as f:
    data = f.read()
    split_data = data.split(b' ')
    if len(split_data) > 3:
        print('More than 3 components found!')
        sys.exit()
    
    # print('comment: %s' % split_data[0], flush=True)
    # sys.stdout.buffer.write(b'\n')
    data = base64.b64decode(split_data[1].strip())

    # https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys
    '''
    RSA certificate

    string    "ssh-rsa"
    mpint     e
    mpint     n
    '''

    i = 0
    # type string
    v, i = get_next_element(data, i, 'string')
    print_as_string('type', v)

    # e
    v, i = get_next_element(data, i, 'string') # mpint is stored as string
    print_as_int('e', v, hex=True)

    # n
    v, i = get_next_element(data, i, 'string')
    print_as_int('n', v, hex=True)


