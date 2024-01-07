#!/usr/local/cs/bin/python3

import random, sys
import string
import argparse

class randline:
    def __init__(self, filename):
        self.filename = filename

    def chooseline(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        random.shuffle(lines)
        return lines
def main():

    parser = argparse.ArgumentParser(usage="Randomly select lines or generate random numbers")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--echo', action='extend', nargs= '*',  help="treat each ARG as an input line")
    group.add_argument('-i', '--input-range', action = 'extend', dest='ranges', help="treat each number LO through HI as an input line")
    parser.add_argument('-n', '--head-count', action = 'store', dest= 'num', type=int, help="output at most COUNT lines")
    parser.add_argument('-r', '--repeat', action='store_true', help="output lines can be repeated")
    parser.add_argument('-', '--stdin', action='store_true', help="read from stdin")
    group.add_argument("filename", nargs='?',help="Input file to shuffle")
    
    args, extra = parser.parse_known_args()

    if len(extra) > 0:
        print(f"shuf: invalid option -- '{extra[0]}'")
        exit()

    if args.echo is not None:
        random.shuffle(args.echo)
        if args.repeat:
            if args.num is None:
                while True:
                    randomNum = random.randint(0, len(args.echo) - 1)
                    random_element = args.echo[randomNum]
                    print(random_element)
            else:
                for _ in range(args.num):
                    randomNum = random.randint(0, len(args.echo) - 1)
                    random_element = args.echo[randomNum]
                    print(random_element)
        elif args.num is not None:
            if args.num > len(args.echo):
                for i in args.echo:
                    print(i)
            else:
                for _ in range(args.num):
                    randomNum = random.randint(0, len(args.echo) - 1)
                    random_element = args.echo[randomNum]
                    print(random_element)
        else:
            for i in args.echo:
                print(i)
    elif args.stdin and args.filename is not None:
        print(f"shuf: extra operand '-'")
        exit()
    elif args.stdin and args.ranges is not None:
        print(f"shuf: extra operand '-'")
        exit()
    elif args.stdin and args.ranges is None:
        lines = [line.strip() for line in sys.stdin]
        random.shuffle(lines)
        if args.repeat:
            if args.num is None:
                while True:
                    randomNum = random.randint(0, len(lines) - 1)
                    random_element = lines[randomNum]
                    print(random_element)
            else:
                for _ in range(args.num):
                    randomNum = random.randint(0, len(lines) - 1)
                    random_element = lines[randomNum]
                    print(random_element)
        elif args.num is not None:
            if args.num > len(lines):
                for i in lines:
                    print(i)
            else:
                for _ in range(args.num):
                    randomNum = random.randint(0, len(lines) - 1)
                    random_element = lines[randomNum]
                    print(random_element)
        else:
            for i in lines:
                print(i)
    elif args.ranges is not None:
        if len(args.ranges) != 3:
            print("invalid range length")
            exit()
        lo = args.ranges[0]
        hi = args.ranges[2]
        lo = int(lo)
        hi = int(hi)
        if lo > hi:
            print(f"shuf: invalid input range: '{lo}-{hi}'")
            exit()
        nums = []
        for num in range(lo, hi + 1):
            nums.append(num)
            random.shuffle(nums)
        if args.repeat:
            if args.num is None:
                while True:
                    randomNum = random.randint(0, len(nums) - 1)
                    random_element = nums[randomNum]
                    print(random_element)
            else:
                for _ in range(args.num):
                    randomNum = random.randint(0, len(nums) - 1)
                    random_element = nums[randomNum]
                    print(random_element)
        elif args.num is not None:
            if args.num > len(nums):
                for i in nums:
                    print(i)
            else:
                for _ in range(args.num):
                    randomNum = random.randint(0, len(nums) - 1)
                    random_element = nums[randomNum]
                    print(random_element)
        else:
            for i in nums:
                print(i)
    else:
        filename = args.filename
        random_line_selector = randline(filename)
        shuffled_lines = random_line_selector.chooseline()
        if args.repeat:
            if args.num is None:
                while True:
                    randomNum = random.randint(0, len(shuffled_lines) - 1)
                    random_element = shuffled_lines[randomNum]
                    print(random_element, end='')
            else:
                for _ in range(args.num):
                    randomNum = random.randint(0, len(shuffled_lines) - 1)
                    random_element = shuffled_lines[randomNum]
                    print(random_element, end='')
        elif args.num is not None:
            if args.num > len(shuffled_lines):
                for i in shuffled_lines:
                    print(i, end='')
            else:
                for _ in range(args.num):
                    randomNum = random.randint(0, len(shuffled_lines) - 1)
                    random_element = shuffled_lines[randomNum]
                    print(random_element, end='')
        else:
            for i in shuffled_lines:
                print(i, end='')

if __name__ == "__main__":
    main()
