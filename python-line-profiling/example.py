#!/usr/bin/python

from time import sleep

@profile
def so_slow(bar):
    """ Simulate a slow function. """
    sleep(5)
    return bar

@profile
def its_time_for_the_calculator(foo):
    """ It's time for the calculator. """
    if not isinstance(foo, int):
        return None

    a = []
    for i in xrange(foo):
        a.append(i)

    b = so_slow(a)

    c = 0
    for i in xrange(foo):
        c += i

    return None

def main():
    print its_time_for_the_calculator(100000)

if __name__ == "__main__":
    main()
