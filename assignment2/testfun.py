import sys
import random

class randline:
    def __init__(self, filename):
        self.filename = filename

    def chooseline(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        random.shuffle(lines)
        return lines
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    random_line_selector = randline(filename)
    shuffled_lines = random_line_selector.chooseline()

    for line in shuffled_lines:
        print(line, end='')