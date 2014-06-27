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

- [GitHub API][9], external service we are going to mock
- [requests][7], a fantastic HTTP library
- [httmock][8], a mocking library for requests

Let's start by pretending our application relies on the GitHub [repository][14]
endpoint. Thus, we can begin with the following:

1. ([Commit][10]) Add a `get_repository` function, for getting GitHub repository
   information.
1. ([Commit][11]) Add a `test_get_repository` test case, for testing our newly
   created `get_repository` function.

Now let's go ahead and run the test:

```bash
(env)[driti@ubuntu]$ python test_github.py
.
----------------------------------------------------------------------
Ran 1 test in 0.245s

OK
```

We can see the test passes and it takes **0.245 seconds**. I don't know
about you, but that's *way* to long for me. Let's speed things up a bit by
mocking out the repository endpoint. To do this, we can make the following
changes:

1. ([Commit][12]) Create a `repository` mock, for faking the response from the
   repository endpoint.
1. ([Commit][13]) Update our unit test to use the `repository` mock.

Now we re-run the test and ...

```bash
(env)[driti@ubuntu]$ python test_github.py
.
----------------------------------------------------------------------
Ran 1 test in 0.009s

OK
```

Wow, talk about a speed up! In fact, it was a **27x** speed up off of a *single*
test:

```bash
(env)[driti@ubuntu]$ python -c "print(0.245 / 0.009)"
27.2222222222
```

The mock we created was quite basic, so let's look at how we can further
improve.

### Tear the Roof Off

Thinking ahead, I'd like to add many more methods to my GitHub library to
support the numerous functionalities of the GitHub API. However, I'm reluctant
because this means I have to create many more mocks.

Immediately, I realize that my initial approach at designing a mock was rushed
and has room for improvement. For starters, let's approach the problem through
a [separation of concerns][15] point of view. We have two concerns when it comes
to mocking a service, the mock and the [resource][18] response. Lumping both these
concerns into the same places makes my mock quite inflexible. So why don't we
try moving our resource response into a [test fixture][17]!

Lucky for us, GitHub followed the RESTful best practice of **Addressability** when
designing their API. Addressability is defined by [Leonard Richardson][20] and
[Sam Ruby][21] in [RESTful Web Services][19] as,

> A web service is addressable if it exposes the interesting aspects of its data
set through resources. **Every resource has it's own unique URI**: in fact,
URI just stands for "Universal Resource Identifier."

Since every resource is addressed unique, we can easily create test fixtures
on the file system. For example, our resource URI
`api.github.com/repos.appneta/burndown` easily maps to a file path, where
`burndown` can be a file containing JSON:

```bash
(env)[driti@ubuntu]$ mkdir -p api.github.com/repos/appneta
(env)[driti@ubuntu]$ echo '{"name":"burndown"}' > api.github.com/repos/appneta/burndown
(env)[driti@ubuntu]$ jsonlint api.github.com/repos/appneta/burndown
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
- Link to Nate's talk: http://www.youtube.com/watch?v=Xu5EhKVZdV8


[1]: https://dev.twitter.com/docs/auth
[2]: https://developer.github.com/v3/issues/
[3]: http://foaas.herokuapp.com/
[4]: http://blog.codinghorror.com/the-prototype-pitfall/
[5]: https://twitter.com/futuresanta
[6]: http://robots.thoughtbot.com/how-to-stub-external-services-in-tests
[7]: http://docs.python-requests.org/
[8]: https://github.com/patrys/httmock
[9]: https://developer.github.com/v3/
[10]: https://github.com/danriti/python-mocked-service/commit/c97eb466131c66cd3daf0b4c5e0014a5a4756bb0
[11]: https://github.com/danriti/python-mocked-service/commit/5003a893b1c52b662d4618a754e921e857e65f9f
[12]: https://github.com/danriti/python-mocked-service/commit/5c69623d77bbe5780d5d68dbc5e85bba08ae3770
[13]: https://github.com/danriti/python-mocked-service/commit/332f03211dbe307b8dcce9b11f7e939f54262276
[14]: https://developer.github.com/v3/repos/#get
[15]: http://en.wikipedia.org/wiki/Separation_of_concerns
[16]: http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
[17]: http://en.wikipedia.org/wiki/Test_fixture#Software
[18]: http://en.wikipedia.org/wiki/Web_resource
[19]: http://shop.oreilly.com/product/9780596529260.do
[20]: https://twitter.com/leonardr
[21]: https://twitter.com/samruby
