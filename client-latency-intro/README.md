client-latency-intro
====================

What is client latency?

Let's face it, users are impatient. They demand a blazingly fast experience
and accept no substitutes. Google performed a [study][1] in 2010 which proved 
that when a site responds slowly, visitors spend less time there.

> Speed as perceived by the end user is driven by multiple factors, including
> how fast results are returned and how long it takes a browser to display the
> content.

So while the effects of poor performance is obvious, it makes one wonder about 
the relationship between client latency and the "perception of speed". 
Afterall, the user can trigger many state change events (page load, submit a
form, interact with a visualization, etc) and all these events have an
associated latency to the client. However, are certain types of latency more
noticable to the user then others?

Let's look at all the different ways latency can creep in, throughout the
'request-to-render' cycle.

## Time To First Lag

The first place for *potential* client latency is the infamous [Time To First
Byte][2]. From a user perspective, this is the worst kind of client latency, 
as it leaves the user with the dreaded "white screen of death". (Screenshot?) 

Time To First Byte (TTFB) is the duration between a user making an HTTP request 
and first byte of the page being received by the browser. The following is a 
typical scenario for TTFB:

(insert an example image of the TTFB timeline?)

1. User enters a URL in browser and hits enter
2. The browser parses the URL
3. The browser performs a DNS lookup (Domain => IP address)
4. The browser opens a TCP connection and sends the HTTP Request
5. (Wait on the network)
6. The browser starts receiving the HTTP Response (first byte received)
 
As you can see, there are many places in this segment where latency can rear
it's ugly head. The DNS lookup may fail, the web server may be under heavy load
so it's [queueing requests][3], network channel congestion may be causing packet
loss, or [soft errors][5] due to [cosmic rays flipping bits][4]. 

This type of latency has negative effects on the user, as the user gets stuck
looking at a loading/waiting animation. This becomes a true test of the user's
patience, as an long TTFB can eventually lead the user to abandon the HTTP
Request and close the browser tab.

## Client Latency and the DOM

Now that the HTTP Response is pouring in, the browser engine can start doing 
what it does best...display content! But before the browser can render (or
paint) content on the screen, there is still more work to be done!

**NOTE**: Not all browsers engines are created equal! Consult your local open
source browser source code repository for detailed inner workings.

As the browser engine receives HTML, it begins constructing the HTML DOM tree.
While parsing the HTML and building the DOM tree, the browser is looking for any
assets (or sub-resources) so it can initiate a download of their content. 

So now that the HTTP Response has arrived, let's take a further look into the
associated latency for both CSS and Javascript sub-resource and how it effects
the user experience.

### CSS

CSS related latency gives the user the impression of a "broken page". This comes
in two forms, a "flash of unstyled content" (FOUC) where the page appears 
unstyled for a short period, then it flickers into the right design. However, if 
the stylesheet never loads, the DOM content will just remain unstyled. While 
this isn't ideal, its manageable because content is still available to the user 
but just in a degraded state.                                          

Let's look at the effect of latency on styling and rendering the DOM.

(Insert image of building a render tree)

1. The browser is parsing the HTML in the HTTP Reponse
2. When the browser locates a `link` tag, it initiates a non-blocking download 
   of the external CSS stylesheet
3. (Wait on network)
4. Once the download completes, the browser engine begins to parse the CSS
5. While parsing CSS, the browser engine is building all the CSS style rules
   and begins matching DOM elements to CSS styles
7. Once complete, the browser engine then applys the style rules with the DOM
   nodes by constructing a render tree
8. This builds a layout, which the browser then renders or paints to the screen

Latency in this segment is highly visible to the user, as it's the last hurdle
to overcome before we can actually display content to the user. The first
potential bottleneck is the placement of the stylesheet tag. We want the
stylesheet to be downloaded as soon as possible, so we can progressively render
the page. Thus, use your `HEAD` and [Put stylesheets at the Top][7]. The
user-visible effect of **not** following this is a "flash of unstyled content"
or a "white screen of death" (depending on the browser).

Our next stop on the latency express is the network. We always want to use an
external stylesheet, however this requires an extra download. So we want this
download to be fast, optimized for user location, and highly reliable. Well if
you haven't been living under a rock, then you know to [Use a Content Delivery
Network (CDN)][8].  The user-visible effect of **not** following is slower 
loading of styled content, as your webserver has to handle extra requests to 
serve the assets (increased load) and this can be slower for users in 
geographically distant locations.

Finally, we have how you write your CSS as the last chokepoint. Inefficiently
written CSS causes the browser to take longer to build a complete render tree,
thus the user-visible effect is a slower loading page render. Fortunately, this
is easily avoidable if you just [Write efficient CSS][9].

Following CSS best practices will not only improve your user experience but
also provide your users with the *appearance* that your pages are loading
faster.

### Javascript

Javascript related latency can have differing effects on the user experience.
Clicking links that don't seem to do anything, stalled loading of the page,
or a "laggy" feeling when scrolling through a page.

There are many places where client latency can appear with Javascript, so let's
take a *highly simplified* look at how the browser deals with Javascript.

1. The browser is parsing the HTML in the HTTP Reponse
2. When the browser locates a `script` tag, it initiates a **blocking** 
   download of the external Javascript file
3. (Wait on network)
4. The browser parses the Javascript file
5. The browser executes the Javascript file
6. (The browser is no longer blocked)
7. Once complete, if the Javascript made changes to the DOM, this forces the
   construction of a new render tree.
8. This builds a layout, which the browser then renders or paints to the screen

You read that correct, the browser **blocks** when downloading Javascript 
files. This can be a real deal breaker for users and can cause a progressively 
loading page to stop dead in it's tracks. This blocking is a result of the 
*potential* use of `document.write` which can write HTML or Javascript to the
document. This means the user has to wait patiently for the Javascript to
download, parse, and run before any progress can be made with the page
rendering. To avoid this type of client latency, you want to [Put Scripts at the
Bottom][10] or [use async or defer script tags][11].

All sub-resources have been downloaded, the page has been rendered, and now the
user gets to actually do something. As the user navigates around your web
application, Javascript is executing as your user triggers state changing 
events. 

Inefficient or slow executing Javascript has the effect of reducing the browsers
render/paint rate. This can cause "[jank][12]" which is defined as "problematic
blocking of a software application's user interface due to slow operations."
Without going into great detail, it's important to note that this type of 
latency is highly noticable to the user. Understanding how to properly use your
[developer tools][14] is key in the battle against jank. Visit 
[jankfree.org][13] for more information.

Javascript that heavily manipulates the DOM is prone to reduced
performance and increased client latency due to the triggering of excessive
reflows. Excessive reflows will make the user's browser stutter, which is quite
noticable. Everytime you change the DOM, this triggers reflows which forces the
construction of a new render tree and then a re-paint of the screen. The DOM is
slow, so it's best to take a [batch approach when dealing with the DOM][16].
This means, do all your DOM reads first and then do all your DOM writes
second (and minimizing the amount of DOM writes).

```javascript
// Bad!
var height = $('.container').height();
$('.container').height(height + 100);
var width = $('.container').width();
$('.container').width(width + 100);

// Good!
var height = $('.container').height();
var width = $('.container').width();
$('.container').height(height + 100);
$('.container').width(width + 100);
```

Finally, client latency can also appear when you make a [XMLHttpRequest][15] in 
Javascript. The user has to yet again wait on the network, however clever UX
tricks (i.e. loading & transition animations) can help make this feel less 
noticable to the user.

## Conclusion

At the end of the day, the performance of your web application directly affects
the user experience. Latency is a given in any networking application, so
understanding how to mitigate its effects on your application will help improve
performance and your overall user experience.

(Plug Appneta products?)

[1]: http://services.google.com/fh/files/blogs/google_delayexp.pdf 
[2]: http://en.wikipedia.org/wiki/Time_To_First_Byte
[3]: http://www.appneta.com/blog/traceview-and-webserver-queing-problems/
[4]: http://stackoverflow.com/questions/4109218/do-gamma-rays-from-the-sun-really-flip-bits-every-once-in-a-while
[5]: http://en.wikipedia.org/wiki/Soft_error
[6]: http://developer.yahoo.com/performance/rules.html
[7]: http://developer.yahoo.com/performance/rules.html#css_top
[8]: http://stackoverflow.com/questions/2145277/what-are-the-advantages-and-disadvantages-of-using-cdncontent-delivery-network
[9]: https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Writing_efficient_CSS
[10]: http://developer.yahoo.com/performance/rules.html#js_bottom
[11]: http://stackoverflow.com/questions/10808109/script-tag-async-defer
[12]: https://www.google.com/search?q=what+is+jank
[13]: http://jankfree.org/
[14]: http://www.igvita.com/slides/2012/devtools-tips-and-tricks/#1
[15]: https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
[16]: https://github.com/stevekwan/best-practices/blob/master/javascript/best-practices.md#causing-excessive-document-reflows
