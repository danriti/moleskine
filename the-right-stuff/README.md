# The Right Stuff

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

### Le Goals

For this experiment, I've decided on the following scoring goals:

1. **Goal**: Match [Google's PageSpeed score][7] (92 Mobile and 98 Desktop)
2. **Stretch Goal**: Get a perfect score (100 in both Mobile and Desktop)

### Going the Distance

Below is a table marking each change and how it effected the PageSpeed score:

|  #  | Commit | Mobile Score | Desktop Score |
| --- | ------ | ------------ | ------------- |
| 1 | [Bootstrap off the shelf][8] | 77 | 90 |
| 2 | [Enable mod_pagespeed][8] | 80 | 93 |
| 3 | [Minify CSS][8] | 80 | 94 |
| 4 | [Remove render blocking JS][8] | 91 | 98 |
| 5 | [Leverage browser caching][8] | 92 | 98 |
| 6 | [Remove render blocking CSS][8] | 100 | 100 |

**NOTE**: Any steps that change the Apache configuration assume that you have
          enabled the module and restarted the webserver.

#### 1. Bootstrap off the Shelf

Here we're simply creating a baseline, using the off the shelf Bootstrap
example with a single modification. Not to shabby to start off with, so let's
see how we can improve.

#### 2. Enable mod_pagespeed

For the first change, we're simply going to enable the PageSpeed Apache
module and let it do all the hard work for us! Well think again, because
the default set of filters enabled by just turning on PageSpeed only gives
us a boost of 3 points for both mobile and desktop.

Weak.

So let's start with some low hanging fruit.

#### 3. Minify CSS

Bootstrap fortunately ships with minified copies of most of it's CSS, however
`theme.css` does not, so we'll be using the trusty old [yuicompressor][] to
get the job done!

```bash
ubuntu@server:~/git/bootstrap-pagespeed$ cp bower_components/bootstrap/dist/css/bootstrap.min.css app/styles/
ubuntu@server:~/git/bootstrap-pagespeed$ cp bower_components/bootstrap/dist/css/bootstrap-theme.min.css app/styles/
ubuntu@server:~/git/bootstrap-pagespeed$ yui-compressor app/styles/theme.css -o app/styles/theme.min.css
```

This change is very straight forward, but doesn't yield many points. So now
we are left with the last optimization.

#### The Fold

Brief explanation of "Above the Fold".

> Eliminate render-blocking JavaScript and CSS in above-the-fold content

> Your page has 1 blocking script resources and 1 blocking CSS resources. This
  causes a delay in rendering your page.

> None of the above-the-fold content on your page could be rendered without
  waiting for the following resources to load. Try to defer or asynchronously
  load blocking resources, or inline the critical portions of those resources
  directly in the HTML.0

#### 4. Remove render-blocking Javascript

[Remove render-blocking JavaScript][11]

After reading over Google's recommendations for removing render-blocking
Javascript, it's clear that we have way to much Javascript to simply inline it
all, so we will have to use their [inline Javascript snippet][13] to defer the
loading.

Immediately, there is a problem. If I defer the loading of all the Javascript
files, how can I guarantee that they are loaded in a specific order? Both
`holder.js` and `bootstrap.js` have a dependency on `jquery.js`, so I'm forced
to manually concatenate all the Javascript files (and minify for good order):

```bash
ubuntu@server:~/git/bootstrap-pagespeed/app/scripts$ cat jquery.js bootstrap.js holder.js > all.js
ubuntu@ip-10-28-140-61:~/git/bootstrap-pagespeed/app/scripts$ yui-compressor all.js -o all.min.js
ubuntu@ip-10-28-140-61:~/git/bootstrap-pagespeed/app/scripts$ ls -alh
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

Holy point increase! Not to mention look how much faster our time to render
is after this improvement.

#### 5. Leverage browser caching

As side effect of deferring the loading of Javascript, we are no longer getting
the automagic browser caching from mod_pagespeed. So sounds like we need to
get a bit hands on with Apache.

The HTML Boilerplate has a fantastic [example][14] of expires headers for
cache control.

**NOTE**: Make sure you're using a [cache busting][] file name scheme so users
          get served new files.

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
ubuntu@ip-10-28-140-61:~/git/bootstrap-pagespeed/app/styles$ cat bootstrap.css bootstrap-theme.css theme.css > all.css
ubuntu@ip-10-28-140-61:~/git/bootstrap-pagespeed/app/styles$ yui-compressor all.css -o all.min.css
ubuntu@ip-10-28-140-61:~/git/bootstrap-pagespeed/app/styles$ ls -alh
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

### Conclusion

State observations, ask questions, and discuss if solutions are actually
"anti-patterns" (if so, how can they be improved?)

[1]: http://twitter.com/igrigorik
[2]: http://velocityconf.com/velocityny2013/public/schedule/detail/30174
[3]: https://developers.google.com/speed/pagespeed/insights/
[4]: https://developers.google.com/speed/docs/insights/v1/getting_started
[5]: http://getbootstrap.com/examples/theme/
[6]: https://developers.google.com/speed/pagespeed/module/
[7]: https://developers.google.com/speed/pagespeed/insights/?url=http%3A%2F%2Fwww.google.com&tab=desktop
[8]: https://github.com/danriti/bootstrap-pagespeed/commit/4adba0f15af3029d68bda9dd8b69ad8b44752ee6
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
