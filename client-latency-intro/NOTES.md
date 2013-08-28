client-latency-intro
====================

What is client side latency?

If you ask any developer this question, I'm sure you'll get wide range of 
answers. Now this isn't necessarily a bad thing, but it gives the impression 
that it's a immature topic that needs more group discussion and some fine 
tuning. (I don't really like this paragraph and want to reword it!)

If I were to take a swing at providing a formal definition, I'd say:

> Client latency is the time between a user triggered event and rendering 
> something **useful** to keep the user engaged.

The user can trigger many state changing events. A new page load, submitting a 
form, interacting with a visualization, etc. All these events have an 
associated latency to the client, so to keep the user's attention we want 
latency to be barely noticable.

The request to render cycle has many segments where poor performance can
undermine our goal, so let's step through an example to highlight a few key
areas.

## Time To First Byte

TTFB is the first leg in *potential* client latency.  

Time To First Byte (TTFB) is the duration between a user making an HTTP
request and first byte of the page being received by the browser. 

High TTFB latency is indicative of poor responsiveness of either your webserver
or network resources between web server and user. From a user perception, this
is the worst kind of client latency, as it leaves the user with the dreaded
"white screen of death." (Screenshot?)

## Slow Loading Javascript

Let's consider the worst case scenario for slow loading Javascript:

1. You host your Javascript files on a different domain, so you have a slow
   DNS lookup
2. Webserver hosting Javascript files is under heavy load, so your request is
   stalled due to queueing
3. Javascript files download slowly
4. Javascript files execute slowly to load initial state.

Assuming your web application uses Javascript, this is most definitely a
negative user experience. This is definitely not ideal and will make your 
application feel "slow" to the user.

## From request to render

- Parse URL
- DNS request
- Open TCP connection, send HTTP Request
- TTFB
- Start getting Server HTTP Response
- As browser engine receieves HTML, it will construct the HTML DOM tree 
- Browser reads HTML and attempts to fetch any sub-resources
    - Images: launch a download, non-blocking
        - Decode image
        - Paint on screen
    - CSS: launch a download, non-blocking
        - Parse CSS
        - Add to buckets?
        - Matching CSS (DOM element -> CSS style) (Bottleneck if you use poor
          CSS selectors? non tag, id, class in right-most selector?)
        - Apply style rules with DOM nodes by constructing a render tree
        - This builds a layout, which we paint to the screen
    - JS: launch a download, almost blocking
        - Downloads started as soon as <script> tag is parsed, because network
          is slow
        - Use <script> defer or async attribute? Tells browser you aren't going
          to use the evil `document.write`.

NOTES:

- What is client latency? 
- Compare user perception of: 
    - time-to-first-byte
    - slow scripts
    - slow assets
    - slow CSS
    - large page size
    - too many ads, etc. 
- I think certain types of latency are more noticeable (waiting on white screen 
  sucks, waiting for ads to load doesn't). 
- http://googleresearch.blogspot.com/2009/06/speed-matters.html
- http://services.google.com/fh/files/blogs/google_delayexp.pdf
