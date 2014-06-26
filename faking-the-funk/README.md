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

Let's start with a simple example with the Github **repos** endpoint, were we
add the following:

1. `test_get_repository` function, for testing our newly created
   `get_repository` function.
1. `get_repository` function, for getting Github repository information.

Running the test, we can see the test pass and it takes XXX time. I don't know
about you, but that's way to long for me. Let's speed things up a bit by
creating a simple mock:

1. `repos` mock, for faking the **repos** endpoint.

Nice, well that was easy.

### Insert Inception Reference About Going Deeper

Now the mock we created was quite basic, so let's look at how we can improve
it further.

I'm a big fan of separation of concerns. The way I see it, we have two concerns
in this case, the mock itself and the resource content. Looking through a MVC
lens, the mock is similar to a controller, while the resource content is
similar to the model(?).

The easiest way to separate the resource content is to move it into a test
fixture that lives on the file system. Immediately, following the "single URI
for each resource" RESTful best practice becomes our best friend here, because
our resource URI `api.github.com/repos.appneta/burndown` easily maps to a file
path, where `burndown` can be a file containing JSON:

```bash
$ mkdir -p api.github.com/repos/appneta
$ echo '{"name":"burndown"}' > api.github.com/repos/appneta/burndown
$ jsonlint api.github.com/repos/appneta/burndown
{
  "name": "burndown"
}
```

Now let's go ahead and update our mock and test:

1. Link to diff

Analyzing on the `repos` mock, it actually has *nothing* specific about the
**repos** endpoint anymore. In fact, it seems we have created a mock that will
correctly handle a GET for any resource that has a test fixture on our file
system.

The proof is in the pudding, so let's make some Jello:

1. Create test fixture for user data endpoint `/user/danriti`?
2. Create test case for GET of user data

Finally, we can add some basic exception handling for the case that a

## Integrity

## Notes

- Create tests to confirm mock assumptions and protect mismatching mocks and implementation.
- Disabling mocks will enable you to see mock vs implementation diffs
- Link to urlmock/response argument types (advanced usage)
- Handling GET (read fixtures)
- Handling POST (create fixtures)
- Handling exceptions (resource does not exist)
- Encapsulating mocks behind configuration variable


[1]: https://dev.twitter.com/docs/auth
[2]: https://developer.github.com/v3/issues/
[3]: http://foaas.herokuapp.com/
[4]: http://blog.codinghorror.com/the-prototype-pitfall/
[5]: https://twitter.com/futuresanta
[6]: http://robots.thoughtbot.com/how-to-stub-external-services-in-tests
[7]: http://docs.python-requests.org/
[8]: https://github.com/patrys/httmock
[9]: https://developer.github.com/v3/
