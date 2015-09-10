# Remote Calls != Local Calls: Graceful Degradation when Services Fail

## Reviewer Comments:

- "No discussions on this yet.  Please provide code examples.  You may also want
   to discuss toolsets to use (Hystrix, etc.)."
- "I really like the idea of presenting good patterns (as distinguished from
   "best practices"). Would attend this."
- "Interesting topic!  Great to see a talk that focuses on recovery/graceful
   failure rather than preventing failure."

## Release It Quotes

- "Develop a recovery-oriented mind-set." (89)
- "Your code can't just wait forever for a response that might never come;
   sooner or late, it needs to give up. Hope is not a design method." (89)
- "Well-placed timeouts provide fault isolations; a problem in some other
   system, subsystem, or device does not have to become your problem." (90)
- "More abstractly, the circuit breaker exists to allow one subsystem (an
   electrical circuit) to fail (excessive current draw, possibly from a
   short-cicruit) without destroying the entire system (the house). Furthermore,
   once the danger has passed, the circuit breaker can be reset to restore full
   function to the system." (93)
- "In software, we can wrap dangerous operations with a component that can
   circumvent calls when the system is not healthy. This differs from retries,
   in that circuit breakers exist to prevent operations rather then reexecute
   them." (93)
- State transition diagram on page 94
- "It is essential to involve the system's stakeholders when deciding how to
   handle calls made when the circuit is open." (95)

## Outline

### Introduction

- title slide
- who am i?
- growing trend over the last few years to decouple monoliths into small
  services
- this introduces new dependencies (network, the service itself, etc)
- and with new dependencies, comes more points of failure
- so knowing we have more points of failure, we have to give some extra
  consideration when making a remote call
    - remote calls != local calls
- so what can we do with our remote calls to
    - ensure graceful degradation
    - when *things* begin to fail
- introduce the techniques (timeouts, circuit breaker)
- introduce the demo application
    - data requirements (user is mandatory, time is nice to have)

### Timeouts

- so lets start by discussing when timeouts are appropriate
- and the short answer is *all the time*
    - not typically enabled by default, so your requests can theoretically take
      *forever* so RTFM
- lets take a look at an example of the time service failing
    - example of time service taking 1 minute
- we're treating our remote call like a local call, which results in a suffering
  user
- so let's introduce a timeout to indicate the limit of our patience with the
  time service
- and now we've degraded gracefully and a bit faster so the user hates us only
  slightly less
- but the interesting thing with a timeout is
    - we are failing *slightly* faster
    - but we still apply load to an unhealthy service, which isn't ideal
- so let's look at how we can augment our timeouts with a little something else

### Circuit Breaker Pattern

- what is a circuit breaker pattern?
    - when to use the pattern?
- introduced in Release It, i highly recommend you read this
- circuit breaker state diagram
- time based tabular data example + infrastructure diagram
- the circuit breaker gives us the bonus of:
    - failing the fastest
    - preventing load on failing service
    - gracefully degradation of user experience
    - an interface to monitor and measure points of integration in a system
- numerous libraries/implementations available in a variety of languages
    - pybreaker is roughly 500 lines of code, including comments and whitespace
- most notable is netflix's Hystrix library for you Java folks, which even
  includes a visualization for monitoring circuit breakers

### Reminders

- Involve the system's stakeholders when deciding how to handle remote calls
  that fail
- Use timeouts where it makes sense
- Explore adopting the circuit breaker pattern

### Questions?


[1]: https://github.com/danielfm/pybreaker
[2]: https://github.com/edgeware/python-circuit
[3]: http://techblog.netflix.com/2011/12/making-netflix-api-more-resilient.html
[4]: https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern
[5]: https://vimeo.com/33359539
[6]: https://github.com/Netflix/Hystrix
[7]: https://github.com/rubyist/circuitbreaker
[8]: http://www.mobify.com/blog/http-requests-are-hard/
[9]: http://docs.python-requests.org/en/latest/user/advanced/#timeouts
[10]: http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
[11]: https://twitter.com/PHP_CEO/status/629652685231390721
[12]: https://en.wikipedia.org/wiki/Antifragility
[13]: https://github.com/Netflix/Hystrix/wiki
