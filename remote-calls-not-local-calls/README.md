# Remote Calls != Local Calls: Graceful Degradation when Services Fail

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

[1]: https://github.com/danielfm/pybreaker
[2]: https://github.com/edgeware/python-circuit
[3]: http://techblog.netflix.com/2011/12/making-netflix-api-more-resilient.html
[4]: https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern
[5]: https://vimeo.com/33359539
