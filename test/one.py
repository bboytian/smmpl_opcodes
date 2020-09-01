# imports
import time

# params
_counter = 0

# main func
def main(p):
    global _counter

    while True:
        print(p, _counter)
        _counter += 1
        time.sleep(1)


# testing
if __name__ == '__main__':
    main()
