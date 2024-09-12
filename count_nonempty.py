# python3
import os
import sys
from base_dir import __BASE_SUBMIT_DIR


if __name__ == '__main__':
    print(sys.argv[1])
    count = 0
    total = 0
    _, dirs, _ = next(os.walk(os.path.join(__BASE_SUBMIT_DIR, sys.argv[1])))
    for d in dirs:
        try:
            _, _, files = next(os.walk(os.path.join(__BASE_SUBMIT_DIR,sys.argv[1],d)))
            if files:
                count += 1
        except StopIteration:
            pass
        total += 1

    print(count, total)
