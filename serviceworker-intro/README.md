# Introducing the ServiceWorker

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
leverage Service Workers to handle the following use cases:

- If the network is available, I want to cache my resources.
- If the network is unavailable, I want to display my cached resources.
- If the network and cached resources are unavailable, I want to display a
  fallback resource.


[1]: http://velocityconf.com/velocityny2014/public/schedule/detail/35821
[2]: https://twitter.com/slightlylate
[3]: https://slightlyoff.github.io/ServiceWorker/spec/service_worker/index.html
[4]: http://www.html5rocks.com/en/tutorials/service-worker/introduction/
[5]: https://github.com/GoogleChrome/samples/tree/gh-pages/service-worker
[6]: https://github.com/slightlyoff/ServiceWorker/blob/master/explainer.md
