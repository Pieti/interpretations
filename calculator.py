#!/usr/bin/env python

from interpreter import Interpreter

def main():
    interpreter = Interpreter()
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        result = interpreter.expr(text)
        print(result)

if __name__ == '__main__':
    main()
