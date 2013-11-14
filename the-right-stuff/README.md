# The Right Stuff

I recently had the pleasure to listen to [Ilya Grigorik][1] give a talk at
Velocity in NYC on [Breaking the 1000ms Mobile Barrier][2].  During the talk,
Ilya used [PageSpeed Insights][3] to demonstrate that several high
profile websites had overlooked some very simple and common optimizations and
resulted in poor PageSpeed scores. For the unfamiliar, [Pagespeed Insights][3]
is a web based tool created by Google that analyzes the content of a web page,
then generates suggestions to make that page faster.

After Ilya's talk ended, I started to think more about *why* performance always
seems to be an afterthought with developers. As I pondered this thought, I kept
coming back to the following question:

> How hard is it to get a perfect PageSpeed Insights score?

It can't be that hard, right? Well...there is only one way to find out!

## Breaking the PageSpeed Barrier

To answer this question, I've decided to keep things as simple as possible, yet
realistic. So I selected the following constraints based on what *I* would
consider to be a simple website:

1. Use Amazon EC2 to host
1. Use a m1.small instance running Ubuntu 12.04 64-bit
1. Use Apache as a webserver with [mod_pagespeed][6]
1. Use an off the shelf [Bootstrap example][5] that depends on external CSS
   and JS (including jQuery)
1. Modify the Bootstrap example to add a single [image][9] (26kb in size)

I picked Apache over Nginx simply because I'm more familiar with setting it up
and configuring it. I choose the Bootstrap example because I felt it is
composed of the many elements you'll find on a modern website. These elements
include several exteral CSS and JS dependencies (3 CSS & 3 JS), a top
oriented navigation bar, and a decent amount of content. Plus, Bootstrap is
widely used across the web, so why not look at how we can make it potentially
faster?

### Going the Distance

I broke the experiment into several steps, where I would:

1. Get the current PageSpeed score
2. Pick a single failed optimization from the list of suggested improvements
3. Research and implement a change to overcome the failed optimization
4. Rinse and repeat until success

Easy enough, so let's get started!

#### 1. Bootstrap off the shelf

Let's begin by generating a PageSpeed score from the off the shelf Bootstrap
example. This will act as a baseline for the rest of the test.

| Commit | Mobile Score | Desktop Score | DOMContentLoaded |
| ------ | ------------ | ------------- | ---- |
| [Bootstrap off the shelf][21] | [77][28] | [90][28] | [833 ms][27] |

So it seems Bootstrap scores much better in desktop then mobile, along with a
[DOMContentLoaded][39] of 833ms. Not to shabby to start off with, so let's see
how we can improve.

#### 2. Enable mod_pagespeed

For the first optimization, we're simply going to enable the Apache PageSpeed
module and let it do all the hard work for us! Well think again, because
enabling PageSpeed with its default set of filters only gives a boost of 3
points for both mobile and desktop.

![Enable mod_pagespeed score][29]

| Commit | Mobile Score | Desktop Score | DOMContentLoaded |
| ------ | ------------ | ------------- | ---- |
| [Enable mod_pagespeed][22] | [80][29] | [93][29] | [660 ms][30] |

Sigh. It looks like we're gonna have to get under the hood and get our hands
dirty with some good old manual optimizations. So let's start with some low
hanging fruit.

#### 3. Minify CSS

Bootstrap fortunately ships with minified copies of most of it's CSS, with the
exception of `theme.css`. So we'll be using the trusty old [yuicompressor][10]
to get the job done!

```bash
$ cp bower_components/bootstrap/dist/css/bootstrap.min.css app/styles/
$ cp bower_components/bootstrap/dist/css/bootstrap-theme.min.css app/styles/
$ yui-compressor app/styles/theme.css -o app/styles/theme.min.css
```

| Commit | Mobile Score | Desktop Score | DOMContentLoaded |
| ------ | ------------ | ------------- | ---- |
| [Minify CSS][23] | [80][31] | [94][31] | [843 ms][32] |

This change is very straight forward, but doesn't yield many points. So now
we are left with the last optimization.

#### Enter The Fold

Welcome to The Fold. No no [the band][41], but that imaginary line in a website
that divides the top 600 pixels of content a user first sees from the rest of
the content they will eventually scroll to.

![Above the Fold][31]

In the world of The Fold, anything "below the fold" is considered a second-class
citizen. And according to Google, we're going to eliminate them from blocking
our need for speed.

So optimizing for above the fold is basically:

1. Prioritize the delivery of any content that is "above the fold". This
   ensures the minimal amount of time for content to be rendered in the browser,
   and ultimately *should* make users happy.
2. Defer everything else, especially anything that will block rendering for
   "below the fold" content.

This is where things get interesting.

#### 4. Remove render-blocking Javascript

After reading over Google's [recommendations][11] for removing render-blocking
Javascript, it's clear that we have way to much Javascript to simply inline it
all, so we will have to use their [inline Javascript snippet][13] to defer the
loading.

Immediately, there is a problem. If I defer the loading of all the Javascript
files, how can I guarantee that they are loaded in a specific order? Both
`holder.js` and `bootstrap.js` have a dependency on `jquery.js`, and loading
them out of order will result in broken Javascript. So I'm forced to manually
concatenate (and minify) all the Javascript files before we defer the loading:

```bash
$ cat jquery.js bootstrap.js holder.js > all.js
$ yui-compressor all.js -o all.min.js
$ ls -alh
total 476K
drwxrwxr-x 2 ubuntu ubuntu 4.0K Nov 11 03:06 .
drwxrwxr-x 5 ubuntu ubuntu 4.0K Nov 11 02:58 ..
-rw-rw-r-- 1 ubuntu ubuntu 161K Nov 11 02:58 all.js
-rw-rw-r-- 1 ubuntu ubuntu 127K Nov 11 03:06 all.min.js
-rw-rw-r-- 1 ubuntu ubuntu  58K Nov  9 01:27 bootstrap.js
-rwxrwxr-x 1 ubuntu ubuntu  13K Nov  9 01:26 holder.js
-rw-rw-r-- 1 ubuntu ubuntu 2.4K Nov  9 01:25 html5shiv.js
-rw-rw-r-- 1 ubuntu ubuntu  91K Nov  9 01:26 jquery.js
-rw-rw-r-- 1 ubuntu ubuntu 4.0K Nov  9 01:25 respond.min.js
```

Now we simply include the defer loading snippet into our HTML and see what
happens...

| Commit | Mobile Score | Desktop Score | DOMContentLoaded |
| ------ | ------------ | ------------- | ---- |
| [Remove render blocking JS][24] | [91][33] | [98][33] | [286 ms][34] |

Wow.

Not only did our scores jump considerably, but our time to first render
(via DOMContentLoaded) has improved significantly! However, it looks like defer
loading has some side effects, so let's dig deeper.

#### 5. Leverage browser caching

As a side effect of deferring the loading of Javascript, we are no longer
getting the automagic browser caching from mod_pagespeed. So sounds like we
need to get a bit hands on with Apache.

The HTML Boilerplate has a fantastic [example][14] of expires headers for
cache control.

**NOTE**: Make sure you're using a [cache busting][] file name scheme so users
          get served new files.

| Commit | Mobile Score | Desktop Score | DOMContentLoaded |
| ------ | ------------ | ------------- | ---- |
| [Leverage browser caching][25] | [92][35] | [98][35] | [231 ms][36] |

Holy crap, we've matched Google's score in 5 steps!

#### 6. Optimize CSS Delivery

[Optimize CSS Delivery][12]

Unfortunately, none of Google's suggestions would help us out much here. So
now the only thing left is to remove render blocking CSS.

Wait...what did you just say? CSS is render blocking by definition!

Yes it is, but we're not gonna let something simple like a stylesheet stop us
from our need for speed (and a perfect score). To do so, we're going to attempt
to leverage an *extremely experimental* technique I learned from
[Addy Osmani][18] and [Paul Kinlan][17] that goes something like this:

1. Run a [Javascript bookmarklet][19] to detect and list CSS that is "above the
   fold"
2. Inline the "above the fold" CSS directly into the HTML
3. Defer loading the rest of the "below the fold" CSS using a simple, yet
   **non-cross browser** solution by [Paul Irish][20]

Sounds kind of crazy? It is, but so is breaking the sound barrier. And that
didn't stop Chuck Yeager, so it won't stop us either.

**NOTE**: For more technical detail, visit the links below:

- Video: [Detecting Critical CSS For Above-The-Fold Content][15]
- Blog: [Detecting Critical Above-the-fold CSS][16]

```
$ cat bootstrap.css bootstrap-theme.css theme.css > all.css
$ yui-compressor all.css -o all.min.css
$ ls -alh
total 516K
drwxrwxr-x 2 ubuntu ubuntu 4.0K Nov 11 04:31 .
drwxrwxr-x 5 ubuntu ubuntu 4.0K Nov 11 04:29 ..
-rw-rw-r-- 1 ubuntu ubuntu 134K Nov 11 04:31 all.css
-rw-rw-r-- 1 ubuntu ubuntu 110K Nov 11 04:31 all.min.css
-rw-rw-r-- 1 ubuntu ubuntu 118K Nov  9 01:24 bootstrap.css
-rw-rw-r-- 1 ubuntu ubuntu  96K Nov 11 02:21 bootstrap.min.css
-rw-rw-r-- 1 ubuntu ubuntu  17K Nov  9 01:24 bootstrap-theme.css
-rw-rw-r-- 1 ubuntu ubuntu  15K Nov 11 02:21 bootstrap-theme.min.css
-rw-rw-r-- 1 ubuntu ubuntu  199 Nov  9 01:23 theme.css
-rw-rw-r-- 1 ubuntu ubuntu  158 Nov 11 02:24 theme.min.css
```

| Commit | Mobile Score | Desktop Score | DOMContentLoaded |
| ------ | ------------ | ------------- | ---- |
| [Remove render blocking CSS][26] | [100][37] | [100][37] | [151 ms][38] |

Did you hear the sonic boom?

### Results

|  #  | Commit | Mobile Score | Desktop Score |
| --- | ------ | ------------ | ------------- |
| 1 | [Bootstrap off the shelf][21] | 77 | 90 |
| 2 | [Enable mod_pagespeed][22] | 80 | 93 |
| 3 | [Minify CSS][23] | 80 | 94 |
| 4 | [Remove render blocking JS][24] | 91 | 98 |
| 5 | [Leverage browser caching][25] | 92 | 98 |
| 6 | [Remove render blocking CSS][26] | 100 | 100 |

### Conclusion

State observations, ask questions, and discuss if solutions are actually
"anti-patterns" (if so, how can they be improved?)

[1]: http://twitter.com/igrigorik
[2]: http://www.youtube.com/watch?v=I4vX-twze9I
[3]: https://developers.google.com/speed/pagespeed/insights/
[4]: https://developers.google.com/speed/docs/insights/v1/getting_started
[5]: http://getbootstrap.com/examples/theme/
[6]: https://developers.google.com/speed/pagespeed/module/
[7]: https://developers.google.com/speed/pagespeed/insights/?url=http%3A%2F%2Fwww.google.com&tab=desktop
[9]: http://en.wikipedia.org/wiki/File:FA-18_Hornet_breaking_sound_barrier_(7_July_1999)_-_filtered.jpg
[10]: http://yui.github.io/yuicompressor/
[11]: https://developers.google.com/speed/docs/insights/BlockingJS
[12]: https://developers.google.com/speed/docs/insights/OptimizeCSSDelivery
[13]: https://developers.google.com/speed/docs/insights/BlockingJS#deferJS
[14]: https://github.com/h5bp/html5-boilerplate/blob/master/.htaccess#L441-L498
[15]: http://www.youtube.com/watch?v=CfmUf1_M9lI
[16]: http://paul.kinlan.me/detecting-critical-above-the-fold-css/
[17]: https://twitter.com/Paul_Kinlan
[18]: https://twitter.com/addyosmani
[19]: https://gist.github.com/PaulKinlan/6284142
[20]: https://plus.google.com/+PaulIrish/posts/Ahn8VkC36nM
[21]: https://github.com/danriti/bootstrap-pagespeed/commit/cfa89f748c39970889fb3ab84451966e3f5221ec
[22]: https://github.com/danriti/bootstrap-pagespeed/commit/8abbcec18b302778c7eef3b510afdf58024d10b5
[23]: https://github.com/danriti/bootstrap-pagespeed/commit/64a1e98e89e7ea5880994fcc220ce687a0c5e986
[24]: https://github.com/danriti/bootstrap-pagespeed/commit/50e10b6a908d71fa8b79b153c36042a5d29efe1b
[25]: https://github.com/danriti/bootstrap-pagespeed/commit/a5ac6b1dd9f7e8da3b7d03c4c91c3455a72d434a
[26]: https://github.com/danriti/bootstrap-pagespeed/commit/ba29bd20ce1f6f539d8e96eb1d2b4737c01ae51f
[27]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/01.timing.png
[28]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/01.score.png
[29]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/02.score.png
[30]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/02.timing.png
[31]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/03.score.png
[32]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/03.timing.png
[33]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/04.score.png
[34]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/04.timing.png
[35]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/05.score.png
[36]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/05.timing.png
[37]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/06.score.png
[38]: https://raw.github.com/danriti/moleskine/master/the-right-stuff/images/06.timing.png
[39]: https://developer.mozilla.org/en-US/docs/Web/Reference/Events/DOMContentLoaded
[40]: http://en.wikipedia.org/wiki/Above_the_fold
[41]: http://www.thefoldrock.com/
