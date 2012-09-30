# -*- coding: utf-8 -*-

import random
from django.conf import settings

def first(cond, iterable):
    for i in iterable:
        if cond(i):
            return i


def generate_number(key):
    target = key.split('/')[0]
    field = key.split('/')[2]
    if target == 'person':
        number_length = first(lambda rec: rec[0] == field, settings.ROLE_FIELDS)[2]
    else:
        number_length = first(lambda rec: rec[0] == field, settings.TRADITION_FIELDS)[2]

    while True:
        seq = range(10)
        random.shuffle(seq)
        number = "".join(str(i) for i in seq[:number_length])
        if check(target, field, number):
            return number


def check(target, field, number):
    if target == 'person':
        if field == 'tradition':
            return int(number[3]) % 3 == 0 and '2' in number and not number.endswith('0')

        if field == 'special':
            odd = "".join([str(int(digit) % 2) for digit in number])
            return (odd == '10101' or odd == '01010') and '5' in number

        if field == 'actions':
            return '3' in number and '7' not in number

        if field == 'actions_steal':
            return number[-1] == '3'

        if field == 'quest':
            return int(number[0]) % 2 == 0 and \
                '3' in number and \
                int(number[-1]) % 2 == 1 and \
                number[4] == '7' # !

        if field == 'criminal':
            return number.startswith('1') and int(number[-1]) % 2 == 1  # !

        if field == 'messages':
            return int(number[0]) % 2 == 0 and int(number[2]) % 3 == 0  # !

    if target == 'tradition':
        if field == 'document':
            return ordinal(int(number[1])) and int(number[1]) % 2 == 0 and number.endswith('3')

        if field == 'documents_list':
            return number[-1] == '0' and int(number[2]) % 2 == 0 and int(number[3]) % 2 == 0 and int(number[4]) % 2 == 0 and number[-2] == '3'

        if field == 'tradition_questbook':
            return number[0] == '5' and int(number[2]) % 2 == 1 and int(number[3]) % 2 == 1 and int(number[4]) % 2 == 1 and number.endswith('1')

        if field == 'corporation_questbook':
            return '7' in number and any(int(d) % 2 == 0 for d in number) and any(int(d) % 3 == 0 for d in number) # !


def ordinal(digit):
    for i in xrange(8):
        check = i + 2
        if digit % check == 0 and check != digit:
            return False
    return True



if __name__ == '__main__':
    generate_number('tradition/40/corporation_questbook')

    #for i in xrange(9):
    #    print i+1, ordinal(i+1)