# Fade to Black: Graceful Degradation with the ServiceWorker

At Velocity NY this past year, I was introduced by [Alex Russell][2] to
[Service Workers][1]. For the uninitiated, Service Workers are a bleeding edge
browser feature that provide event-driven scripts that run independently of web
pages. A Service Worker script runs in the background on it's own thread
and provides the ability to respond to events even when the user is offline.

Upon learning this, I immediately got excited because Service Workers open the
door for developers to be able to gracefully handle the offline experience for
users. This is especially game changing for mobile web developers where the
network can be unreliable.

Since I'm a big fan of graceful degradation, let's take a look at how we can
leverage the Service Worker to handle the following use cases for a simple
web application:

- If the network is available, I want to cache my resources.
- If the network is unavailable, I want to display my cached resources.
- If the network and cached resources are unavailable, I want to display a
  fallback resource.

## Allow Me To Re-Introduce Myself

Before getting started, there are a few notable points about Service Workers
that I should mention:

- The [Service Worker specification][7] is **not** complete and is still in
  active development.
- I'd recommend using Chrome 40+ for experimenting with Service Workers, as its
  the only browser that currently supports debugging Service Workers. Check
  [here][8] to see the current support status for Service Workers.
- Service Workers make extensive use of Promises. Ya heard?

Now that's out of the way, we're ready to get started! To begin, let's setup our
simple web application with some boilerplate:

- ([Commit][100]) Add boilerplate files.

Nothing interesting to see here, so let's quickly move into introducing a
bare bones Service Worker into our application:

- ([Commit][101]) Add serviceworker.js file.

Our Service Worker is quite basic, however we have setup event listeners for
two keys events:

- The `install` event is triggered when a Service Worker is first registered.
- The `fetch` event is triggered for all network requests made against our
  ServiceWorker scope.

For the purpose of this exercise, we will only need these leverage these two
events. However, if you have a burning desire to learn about other Service
Worker events, read on [here][13].

Now that we have some event listeners in place, let's go ahead and register our
Service Worker:

- ([Commit][102]) Update to register serviceworker.

![Registered service worker](https://raw.githubusercontent.com/danriti/moleskine/master/serviceworker-intro/images/03.png)

[1]: http://velocityconf.com/velocityny2014/public/schedule/detail/35821
[2]: https://twitter.com/slightlylate
[3]: https://slightlyoff.github.io/ServiceWorker/spec/service_worker/index.html
[4]: http://www.html5rocks.com/en/tutorials/service-worker/introduction/
[5]: https://github.com/GoogleChrome/samples/tree/gh-pages/service-worker
[6]: https://github.com/slightlyoff/ServiceWorker/blob/master/explainer.md
[7]: https://github.com/slightlyoff/ServiceWorker
[8]: https://jakearchibald.github.io/isserviceworkerready/
[9]: https://github.com/w3c-webmob/ServiceWorkersDemos
[13]: https://slightlyoff.github.io/ServiceWorker/spec/service_worker/index.html#execution-context-events

[100]: https://github.com/danriti/fade-to-black/commit/3b58eba256c9b934b10197cbd75590cd2dcc2965
[101]: https://github.com/danriti/fade-to-black/commit/65bac6e4004267b75d1045040bf4e1e9e4abb95f
[102]: https://github.com/danriti/fade-to-black/commit/ea59404db3d48e2d7d0b82887a305198f3ea9e49
