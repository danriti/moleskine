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

It's important to note that we do **not** want to create our mocks within our
test files, as this does not promote the idea of reusability. Thus, I highly
recommend creating all your mocks within a [`mocks` module][36] to encourage
reuse among existing and future tests.

## Tear the Roof Off

The mock we created was quite basic. So let's take a look at how we can further
improve.

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

Since every GitHub resource is uniquely addressed, this makes it easy for us to
map a resource URI to a file on our file system. For example, the resource URI
`api.github.com/repos/appneta/burndown` can just be a file nested in several
directories containing JSON:

```bash
(env)[driti@ubuntu]$ mkdir -p api.github.com/repos/appneta
(env)[driti@ubuntu]$ echo '{"name":"burndown"}' > api.github.com/repos/appneta/burndown
(env)[driti@ubuntu]$ cat api.github.com/repos/appneta/burndown | python -m json.tool
{
    "name": "burndown"
}
```

Now let's go ahead and update our mock and test:

1. ([Commit][22]) Refactor the `repository` mock to use test fixtures.

```bash
(env)[driti@ubuntu]$ python test_github.py
.
----------------------------------------------------------------------
Ran 1 test in 0.009s

OK
```

Awesome!

Looking back at our `repository` mock, it actually contains *nothing* specific
about the repository endpoint anymore (other then the `path` parameter). In fact,
it seems like the mock can be reused for generic GET requests for *any* resource
that has a test fixture on our file system.

The proof is in the pudding, so let's update our mock:

1. ([Commit][25]) Rename `repository` mock to `resource_get`.

So let's go ahead and put our updated `resource_get` mock to the test and see
if it can properly handle requests for GitHub [user][24] information:

1. ([Commit][26]) Add a `get_user` function, for getting GitHub [user][24]
   information.
1. ([Commit][27]) Add a `test_get_user` test case, for testing our `get_user`
   function.
1. ([Commit][28]) Create a test fixture for user `danriti`.

Running our updated test suite yields sweet victory:

```bash
(env)[driti@ubuntu]$ python test_github.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.013s

OK
```

With our new and improved `resource_get` mock, we now only have to create test
fixtures anytime we want to add new functionality and test it!

## Whole Lot of Rhythm Going Round

Developers love refactoring, right? Well I can think of a few more changes that
are appropriate.

First, our mock knows to much! Thus, I propose we do some good old [information
hiding][30] and move the file open functionality out of our mock and into a new
class called `Resource`:

1. ([Commit][31]) Create Resource class for encapsulating file handling.

Secondly, let's introduce some error handling so our mock will respond properly
with a `404` if a resource is not available:

1. ([Commit][32]) Add error handling if resource is not available.

Now I can rest easy, knowing that I have created a realistic, reusable and easy
to maintain mock infrastructure!

## Conclusion

Mocking external services can get complicated, fast. In this article, we've only
covered the handling of GET requests (i.e. reading test fixtures), so it's
important to note that complexity can increase as you introduce mocking of
POST, PUT, and DELETE requests.

However complex, I hope I have demonstrated the value to your test suite when
using a structured and well organized approach when creating mocks of external
services. Not only will your test suite improve in speed, but you'll create a
set of reusable mocks that can be leveraged by future tests.

As a follow up, I highly encourage to you watch the PyCon 2014 talk by
[Augie Fackler][33] and [Nathaniel Manista][34] titled
[Stop Mocking, Start Testing][35].


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
[22]: https://github.com/danriti/python-mocked-service/commit/b8304d3a6e7225b2e2d2d9bdf3a7c623f095fba0
[23]: https://www.youtube.com/watch?v=zt6IyMYcyZk
[24]: https://developer.github.com/v3/users/#get-a-single-user
[25]: https://github.com/danriti/python-mocked-service/commit/f4e91a12fc401dd7f39f96a315e4eab19e8b115f
[26]: https://github.com/danriti/python-mocked-service/commit/9c7cad198d0e2eed8053198c08fe12f093ad17f5
[27]: https://github.com/danriti/python-mocked-service/commit/95e2c572fba2b7eec5bf6492876906b22c98e441
[28]: https://github.com/danriti/python-mocked-service/commit/c4f45acd4e29beff06b410892324c041f494641d
[29]: https://github.com/danriti/python-mocked-service/blob/f4e91a12fc401dd7f39f96a315e4eab19e8b115f/mocks/github.py#L20-L21
[30]: http://en.wikipedia.org/wiki/Information_hiding
[31]: https://github.com/danriti/python-mocked-service/commit/7fc95b4a8a53b5555ccef529271aaca76fd3cf8e
[32]: https://github.com/danriti/python-mocked-service/commit/40a4ef112e11cba668b4d62f528e98b50d0041cd
[33]: https://twitter.com/durin42
[34]: https://plus.google.com/+NathanielManista
[35]: http://www.youtube.com/watch?v=Xu5EhKVZdV8
[36]: https://github.com/danriti/python-mocked-service/tree/master/mocks
