# Faking the Funk: Mocking External Services in Python Tests

In this day and age, it's difficult to build an application that does **not**
rely on some type of external service. Whether the service is handling
[user identity][1], analyzing [interesting data][2], or hurling RESTful
[insults][3], you have to accept the fact that you now have a dependency on
something you do **not** control.

One place where this dependency can become painfully obvious is running your
test suite. Making requests to an external service can cause your tests
to become *extremely* slow. According to [Harlow Ward][6], these extra requests
during tests can cause a wide range of problems:

> - Tests failing intermittently due to connectivity issues.
> - Dramatically slower test suites.
> - Hitting API rate limits on 3rd party sites (e.g. Twitter).
> - Service may not exist yet (only documentation for it).
> - Service doesn’t have a sandbox or staging server.

We want to ensure our test suite is fast and consistent. Thus, let's take a
look at how we can leverage mocks to create an isolated test environment in
Python.

## We Want the Funk

To begin, let's take a look at some of the tools we're going to use in this
exercise:

- [Github API][9], external service we are going to mock
- [requests][7], a fantastic HTTP library
- [httmock][8], a mocking library for requests


[1]: https://dev.twitter.com/docs/auth
[2]: https://developer.github.com/v3/issues/
[3]: http://foaas.herokuapp.com/
[4]: http://blog.codinghorror.com/the-prototype-pitfall/
[5]: https://twitter.com/futuresanta
[6]: http://robots.thoughtbot.com/how-to-stub-external-services-in-tests
[7]: http://docs.python-requests.org/
[8]: https://github.com/patrys/httmock
[9]: https://developer.github.com/v3/
