# Hold the Line: Line Profiling in Python

If you've ever [profiled][2] code in Python, you've probably used the
[cProfile][1] module. While the cProfile module is quite powerful, I find it
involves a lot of [boilerplate code][4] to get it setup and configured before
you can get useful information out of it. Being a fan of the [KISS][5]
principle, I want an easy and unobtrusive way to profile my code. Thus, I find
myself using the [line_profiler][3] module due to it's simplicity and superior
output format.

The `line_profiler` is not part of the standard python library, so let's go
ahead and install it in your virtual environment:

```bash
$ pip install line_profiler
```

For demonstration purposes, I created this [example program][6] which includes
an intentionally slow function to show off the `line_profiler` output. After
you've looked over the example program, let's assume we want to profile the
`its_time_for_the_calulator` function.

To do so, all you have to do is add a `@profile` decorator above the method
like [this][7]. Now we run the program:


```bash
$ kernprof.py -l -v example.py
None
Wrote profile results to example.py.lprof
Timer unit: 1e-06 s

File: example.py
Function: its_time_for_the_calulator at line 10
Total time: 5.21806 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    10                                           @profile
    11                                           def its_time_for_the_calulator(foo):
    12                                               """ It's time for the calculator. """
    13         1            7      7.0      0.0      if not isinstance(foo, int):
    14                                                   return None
    15
    16         1            1      1.0      0.0      a = []
    17    100001        47690      0.5      0.9      for i in xrange(foo):
    18    100000        65354      0.7      1.3          a.append(i)
    19
    20         1      5001312 5001312.0     95.8      b = so_slow(a)
    21
    22         1            3      3.0      0.0      c = 0
    23    100001        47836      0.5      0.9      for i in xrange(foo):
    24    100000        55853      0.6      1.1          c += i
    25
    26         1            0      0.0      0.0      return None
```

Just like that, line-by-line profiled output!

We can quickly analyze the `line_profiler` output by looking at the "**Time**"
and "**% Time**" columns, where you can clearly see that line 10 is taking the
most time. So let's go ahead and simply add the `@profile` decorator to the
`so_slow` function and re-run:

```bash
$ kernprof.py -l -v example.py
None
Wrote profile results to example.py.lprof
Timer unit: 1e-06 s

File: example.py
Function: so_slow at line 5
Total time: 5.00611 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     5                                           @profile
     6                                           def so_slow(bar):
     7                                               """ Simulate a slow function. """
     8         1      5006109 5006109.0    100.0      sleep(5)
     9         1            3      3.0      0.0      return bar

File: example.py
Function: its_time_for_the_calulator at line 11
Total time: 5.21587 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    11                                           @profile
    12                                           def its_time_for_the_calulator(foo):
    13                                               """ It's time for the calculator. """
    14         1            3      3.0      0.0      if not isinstance(foo, int):
    15                                                   return None
    16
    17         1            1      1.0      0.0      a = []
    18    100001        46257      0.5      0.9      for i in xrange(foo):
    19    100000        60212      0.6      1.2          a.append(i)
    20
    21         1      5006140 5006140.0     96.0      b = so_slow(a)
    22
    23         1            1      1.0      0.0      c = 0
    24    100001        47857      0.5      0.9      for i in xrange(foo):
    25    100000        55398      0.6      1.1          c += i
    26
    27         1            1      1.0      0.0      return None
```

And just like that, you can surgically step through your programs and get
fast and actionable profiling information with very little overhead!

[1]: http://docs.python.org/2/library/profile.html#module-cProfile
[2]: http://en.wikipedia.org/wiki/Profiling_(computer_programming)
[3]: http://pythonhosted.org/line_profiler/
[4]: http://docs.python.org/2/library/profile.html#profile.Profile
[5]: http://en.wikipedia.org/wiki/KISS_principle
[6]: https://gist.github.com/danriti
