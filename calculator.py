#!/usr/bin/env python

from interpretations.calculator import calculate


def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue

        print(calculate(text))

if __name__ == '__main__':
    main()
