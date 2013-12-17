# Line Profiling in Python

If you've ever [profiled][2] code in Python, you've probably used the
[cProfile][1] module. While the cProfile module is quite powerful, I find it
involves a lot of [boilerplate code][4] to get it setup and configured before
you can get useful information out of it. Being a big fan of the [KISS][5]
principle, I find myself using the [line_profiler][3] module due to it's
simplicity and superior output format.

[1]: http://docs.python.org/2/library/profile.html#module-cProfile
[2]: http://en.wikipedia.org/wiki/Profiling_(computer_programming)
[3]: http://pythonhosted.org/line_profiler/
[4]: http://docs.python.org/2/library/profile.html#profile.Profile
[5]: http://en.wikipedia.org/wiki/KISS_principle
