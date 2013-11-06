# The Right Stuff

Breaking the PageSpeed barrier.

I recently had the pleasure to listen to [Ilya Grigorik][1] give a talk at
Velocity in NYC on [Breaking the 1000ms Mobile Barrier][2].  During the talk,
Ilya kept using [PageSpeed Insights][3] to demonstrate that several high
profile websites had overlooked some very simple and common optimizations and
ultimately had scored poorly. For the unfamiliar, [Pagespeed Insights][3] is a
web based tool created by Google that analyzes the content of a web page, then
generates suggestions to make that page faster.

After Ilya's talk ended, I started to think more about *why* performance always
seems to be an afterthought with developers. As I pondered this thought, I kept
coming back to the following question:

> How hard is it to get a perfect score with PageSpeed?

It can't be that hard, right? Well...there is only one way to find out!

## The Experiment

> Can a Bootstrap example template get a perfect PageSpeed score?

To answer this question, I've decided to keep things as simple as possible, yet
realistic. So I selected the following constraints based on what *I* would
consider to be a simple website:

1. Use Amazon EC2 to host
1. Use a m1.small instance running Ubuntu 12.04 64-bit
1. Use Apache as a webserver with [mod_pagespeed][6].
1. Use a [Bootstrap example][5] that depends on external CSS and JS
   (including jQuery) assets.

## The Goals

For this experiment, I've decided on the following scoring goals:

1. **Goal**: Match [Google's PageSpeed score][7] (92 Mobile and 98 Desktop)
2. **Stretch Goal**: Get a perfect score (100 in both Mobile and Desktop)

## The Challenge

Below is a table marking each change and how it effected the PageSpeed score:

|  #  | Commit | Mobile Score | Desktop Score |
| --- | ------ | ------------ | ------------- |
| 1 | [Vanilla template][] | XX | XX |

[1]: http://twitter.com/igrigorik
[2]: http://velocityconf.com/velocityny2013/public/schedule/detail/30174
[3]: https://developers.google.com/speed/pagespeed/insights/
[4]: https://developers.google.com/speed/docs/insights/v1/getting_started
[5]: http://getbootstrap.com/examples/theme/
[6]: https://developers.google.com/speed/pagespeed/module/
[7]: https://developers.google.com/speed/pagespeed/insights/?url=http%3A%2F%2Fwww.google.com&tab=desktop
