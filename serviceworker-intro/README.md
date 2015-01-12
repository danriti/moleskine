# Fade to Black: Graceful Degradation with the Service Worker

At Velocity NY this past year, I was introduced by [Alex Russell][2] to
[service workers][1]. For the uninitiated, service workers are a bleeding edge
browser feature that provide event-driven scripts that run independently of web
pages. A service worker script runs in the background on it's own thread
and provides the ability to respond to events even when the user is offline.

Upon learning this, I immediately got excited because service workers open the
door for developers to be able to gracefully handle the offline experience for
users. This is especially game changing for mobile web developers where the
network can be unreliable.

Since I'm a big fan of graceful degradation, let's take a look at how we can
leverage the service worker to handle the following use cases for a simple
web application:

- If the network is available, I want to cache my resources.
- If the network is unavailable, I want to display my cached resources.
- If the network and cached resources are unavailable, I want to display a
  fallback resource.

## Allow Me To Re-Introduce Myself

Before getting started, there are a few notable points about service workers
that I should mention:

- The [service worker specification][7] is **not** complete and is still in
  active development.
- I'd recommend using Chrome 40+ for experimenting with service workers, as its
  the only browser that currently supports debugging service workers. Check
  [here][8] to see the current support status for service workers.
- service workers make extensive use of Promises. Ya heard?
- Client side + proxy notes?

Now that's out of the way, we're ready to get started! To begin, let's setup our
simple web application with some boilerplate:

- ([Commit][100]) Add boilerplate files.

Nothing interesting to see here, so let's quickly move into introducing a
bare bones service worker into our application:

- ([Commit][101]) Add serviceworker.js file.

Our service worker is quite basic, however we have setup event listeners for
two keys events:

- The `install` event is triggered when a service worker is first registered.
- The `fetch` event is triggered for all network requests made against our
  ServiceWorker scope.

For the purpose of this exercise, we will only need these leverage these two
events. However, if you have a burning desire to learn about other Service
Worker events, read on [here][13].

Now that we have some event listeners in place, let's go ahead and register our
service worker:

- ([Commit][102]) Update to register the service worker.

As you can see, the registration of a service worker is a pretty straightforward
task. The important thing to note is that service workers have a notion of scope
based on where they are located in your domain. Since our service worker is at
the root of our domain, the scope will be the entire origin.

![Registered service worker](https://raw.githubusercontent.com/danriti/moleskine/master/serviceworker-intro/images/03.png)

In the above screenshot, we can see that web application loads successfully and
the service worker is successfully registered in Chrome's console on the
left side. I mentioned that Chrome has debugging available for currently
running service workers, which is what we're looking at in the Developer Tools
console on the right side.

Looking closer at the service worker's console (right side), we can see that
our `install` event gets successfully triggered and we see two `fetch` events,
one for our `index.html` and one for our `styles.css`.

Thus, if we break it down in order, the following happens:

1. Browser fetches and loads `index.html`
2. The service worker gets registered with our browser via inline script in
   `index.html`
3. Our browser fetches `serviceworker.js` and spins off

Great, now we're ready to explore caching resources!

## More Money, More Cache

- polyfill
- cache init
- cache hit/miss


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
[101]: https://github.com/danriti/fade-to-black/commit/fc62151178da550bfcd0032cbe10449c9e8b20dd
[102]: https://github.com/danriti/fade-to-black/commit/992b80a7b4f383e50173f7f70298f52cd7f8f5e1
