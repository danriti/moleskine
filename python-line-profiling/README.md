# Hold the Line: Line Profiling in Python

If you've ever [profiled][2] code in Python, you've probably used the
[cProfile][1] module. While the `cProfile` module is quite powerful, I find it
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
`its_time_for_the_calculator` function.

To do so, all you have to do is add a `@profile` [decorator][8] above the
`its_time_for_the_calculator` function like [this][7]. Now we run the program:


```bash
[driti@ubuntu]$ kernprof.py -l -v example.py
None
Wrote profile results to example.py.lprof
Timer unit: 1e-06 s

File: example.py
Function: its_time_for_the_calculator at line 10
Total time: 5.22311 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    10                                           @profile
    11                                           def its_time_for_the_calculator(foo):
    12                                               """ It's time for the calculator. """
    13         1            3      3.0      0.0      if not isinstance(foo, int):
    14                                                   return None
    15
    16         1            1      1.0      0.0      a = []
    17    100001        49082      0.5      0.9      for i in xrange(foo):
    18    100000        62532      0.6      1.2          a.append(i)
    19
    20         1      5004922 5004922.0     95.8      b = so_slow(a)
    21
    22         1            2      2.0      0.0      c = 0
    23    100001        50113      0.5      1.0      for i in xrange(foo):
    24    100000        56456      0.6      1.1          c += i
    25
    26         1            0      0.0      0.0      return None
```

Just like that, line-by-line profiled output!

We can quickly analyze the `line_profiler` output by looking at the "**Time**"
and "**% Time**" columns, where you can clearly see that `line 10` is taking a
long time. So let's go ahead and also add the `@profile` decorator to the
`so_slow` function and re-run:

```bash
[driti@ubuntu]$ kernprof.py -l -v example.py
None
Wrote profile results to example.py.lprof
Timer unit: 1e-06 s

File: example.py
Function: so_slow at line 5
Total time: 5.00598 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     5                                           @profile
     6                                           def so_slow(bar):
     7                                               """ Simulate a slow function. """
     8         1      5005974 5005974.0    100.0      sleep(5)
     9         1            3      3.0      0.0      return bar

File: example.py
Function: its_time_for_the_calculator at line 11
Total time: 5.22016 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    11                                           @profile
    12                                           def its_time_for_the_calculator(foo):
    13                                               """ It's time for the calculator. """
    14         1            3      3.0      0.0      if not isinstance(foo, int):
    15                                                   return None
    16
    17         1            0      0.0      0.0      a = []
    18    100001        48222      0.5      0.9      for i in xrange(foo):
    19    100000        62404      0.6      1.2          a.append(i)
    20
    21         1      5006008 5006008.0     95.9      b = so_slow(a)
    22
    23         1            1      1.0      0.0      c = 0
    24    100001        48883      0.5      0.9      for i in xrange(foo):
    25    100000        54635      0.5      1.0          c += i
    26
    27         1            0      0.0      0.0      return None
```

As you can see in the `line_profiler` output, it organizes the results
by segmenting each decorated method into it's own report. This makes it easy
to spot that the real problem lies on `line 8`, where I included the call to
the `sleep` function.

Taking it all in, `line_profiler` enables you to surgically step through your
code and get fast and actionable profiling information all by just adding
a simple decorator. Not only is the `line_profiler` easy to use, but it's
profiling information is easy to digest and will empower developers to
react and diagnose performance problems with improved accuracy.

[1]: http://docs.python.org/2/library/profile.html#module-cProfile
[2]: http://en.wikipedia.org/wiki/Profiling_(computer_programming)
[3]: http://pythonhosted.org/line_profiler/
[4]: http://docs.python.org/2/library/profile.html#profile.Profile
[5]: http://en.wikipedia.org/wiki/KISS_principle
[6]: https://gist.github.com/danriti
[7]: https://gist.github.com/danriti
[8]: https://wiki.python.org/moin/PythonDecorators#What_is_a_Decorator
