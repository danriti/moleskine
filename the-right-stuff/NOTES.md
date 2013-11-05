# The Right Stuff

Breaking the PageSpeed barrier.

I recently had the pleasure to listen to [Ilya Grigorik][1] give a talk at
Velocity in NYC on [Breaking the 1000ms Mobile Barrier][2]. During the talk,
Ilya used [PageSpeed Insights][3] to demonstrate that several high profile
websites scored poorly. Now his purpose wasn't to shame these websites, but to
show how some very simple and common optimizations were overlooked and have a
profound impact on performance for mobile.

Now I think think it's safe to assume that the developers of these websites do
in fact care about performance. After all, isn't performance drilled into our
heads the minute we learn the difference between sorting algorithms? So if we
care so much about performance, then why is it always an afterthought?

> "Just get it working first, then we'll worry about making it fast".

Sounds familiar? Well if we want to make the internet a better place, we have
to start treating performance like a first-class citizen.

So this got me thinking. What if we treated performance like unit tests?
You're not allowed to release code that fails unit tests, so why are you
allowed to release code that performs poorly? After all, Google does provide an
[API][4] for PageSpeed Insights, so why is it not automatically baked into
everyone's release process?

Without diving into the rabbit hole of *why* performance always seems to be
an afterthought, Ilya's talk got me thinking about the following question:

> How hard is it to get a perfect score with PageSpeed?

It can't be that hard right? I mean,

This is a very broad question, so I selected some constraints based on what I
would consider to be an simple web site:

1. Use Amazon EC2 to host
1. Use an m1.small instance running Ubuntu 12.04 64-bit
1. Use Apache as a webserver with [mod_pagespeed][6].
1. Use a [Bootstrap example][5] to simulate a site with a good amount of CSS
   and some JS.

The goals of the experiment were:

1. Perfect score with PageSpeed Insights
1. Reduce "time to first paint"

[1]: http://twitter.com/igrigorik
[2]: http://velocityconf.com/velocityny2013/public/schedule/detail/30174
[3]: https://developers.google.com/speed/pagespeed/insights/
[4]: https://developers.google.com/speed/docs/insights/v1/getting_started
[5]: http://getbootstrap.com/examples/theme/
[6]: https://developers.google.com/speed/pagespeed/module/
