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
    data = f.readlines()
    if len(data) < 3:
        print('Less than 3 lines found!')
        sys.exit()
    data = b''.join(data[1:-1])
    data = base64.b64decode(data.strip())

    # https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys
    '''
    #define AUTH_MAGIC      "openssh-key-v1" (NULL terminated)

        byte[]	AUTH_MAGIC
        string	ciphername
        string	kdfname
        string	kdfoptions
        uint32	number of keys N
        string	publickey1
        string	publickey2
        ...
        string	publickeyN
        string	encrypted, padded list of private keys
    '''

    AUTH_MAGIC = 'openssh-key-v1'
    LEN_AUTH_MAGIC = len(AUTH_MAGIC)
    print_as_string('type', data[:LEN_AUTH_MAGIC+1])

    i = LEN_AUTH_MAGIC+1

    # cipher name
    v, i = get_next_element(data, i, 'string')
    print_as_string('cipher name', v)

    # kdf name
    v, i = get_next_element(data, i, 'string')
    print_as_string('kdf name', v)

    # kdf options
    v, i = get_next_element(data, i, 'string')
    print_as_string('kdf options', v)

    # number of keys
    v, i = get_next_element(data, i, 'uint32')
    print_as_int('number of keys', v)
    
    key_count = v
    # loop through all the public keys
    print('public keys')
    for ii in range(key_count):
        '''
        int32  length of public key
        string type    ("ssh-rsa")
        mpint  e       (RSA public exponent)
        mpint  n       (RSA modulus)
        '''
        print('key %d' % (ii+1))

        # lengh of key[ii]
        v, i = get_next_element(data, i, 'uint32')
        # print_as_int('    length of key', v, hex=True)

        # type of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_string('    type', v)

        # e of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_int('    e', v, hex=True)

        # n of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_int('    n', v, hex=True)

    # loop through all the public keys
    print('private keys:')
    for ii in range(key_count):
        '''
        uint32  checkint
        uint32  checkint
        string  type
        mpint   n
        mpint   e
        mpint   d
        mpint   iqmp
        mpint   p
        mpint   q
        string  comment
        byte[n] padding
        '''

        print('key %d' % (ii+1))

        # length of key[ii]
        v, i = get_next_element(data, i, 'uint32')
        # print_as_int('    private key size', v, hex=True)
        private_key_size = v
        start_of_private_key = i

        # check-int of key[ii]
        v, i = get_next_element(data, i, 'uint32')
        print_as_int('    check-int', v, hex=True)

        # check-int of key[ii]
        v, i = get_next_element(data, i, 'uint32')
        print_as_int('    check-int', v, hex=True)

        # type of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_string('    private key type', v)

        # n of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_int('    n', v, hex=True)

        # e of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_int('    e', v, hex=True)

        # d of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_int('    d', v, hex=True)

        # iqmp of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_int('    iqmp', v, hex=True)

        # p of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_int('    p', v, hex=True)

        # q of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_int('    q', v, hex=True)

        # comment of key[ii]
        v, i = get_next_element(data, i, 'string')
        print_as_string('    comment', v)

        # padding (so that size % 256 = 0)
        padding = data[i:start_of_private_key + private_key_size]
        print_as_string('    padding', b'0x' + b''.join([(hex(j)[2:]).zfill(2).encode() for j in padding]))
        i = start_of_private_key + private_key_size
