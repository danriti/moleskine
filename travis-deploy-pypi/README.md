# Travis meets PyPI

## Introduction

- python-traceview new release
- what is it?
- i got fed up with manually deploying to pypi
- so lets talk about how to deploy automatically with travis ci

The TraceView team has added the ability to delete applications to our
Application Management API, so now users are enabled to programmatically delete
and clean up applications that are no longer in use. Along with this helpful
addition, I've just released an updated version of the [python-traceview][1]
client library, to include this new functionality. For those of you not familiar
with the python-traceview library, it's an open-source Python library for
interacting with the TraceView API, allowing power users the ability to extract
meaningful performance information and manage their TraceView accounts.

As the sole maintainer of the python-traceview library, I've been following a
simple [deploy process][3] I cooked up for getting new releases of the library
on [PyPI][2] (the Python Package Index). Now that I've been maintaing the
project for almost 2 years, the "excitement" of doing a manual release has
come and gone. Thus, my first thought when approaching this release was:

> How can I automate this release process?

Well, it turns out that the answer is quite simple; [Travis CI][4], a continuous
integration service used to build and test projects. So lets take a closer look
at how to get started!

## Process Delta

- already using travis for testing
- how does the process change? (pr, merge, release)

As it turns out, python-traceview is already [using][5] Travis CI, but only for
[running tests][6] against changes in the repository. So before we get into
using Travis CI for deployment, lets talk about how we want to augment the
release process. Since the python-traceview library uses Github, we using pull
requests to introduce changes to the library. Thus, I want to update the process
to go something like this:

1. Developer submits a pull request against the repository that introduces a
   new feature or bug fix
2. Travis CI automatically runs the test suite against the pull request,
   indicating a passing or failing build
3. Once the build is passing and the feature is accepted, the pull request is
   merged into `master`
4. Travis CI automatically deploys to [Test PyPI][7] on *any* change to
   `master`. This allows me to use the Test PyPI site as a "staging"
   environment, where I can manually ensure that everything is good with the
   package (documentation, release history, etc).
5. Once I've determined that my "release candidate" is looking good on `master`,
   I can simply create a new [Github release][8], which will add a version tag
   to the repository.
6. Travis CI automatically deploys to "production" PyPI on *any* tagged commit,
   effectively making the new release available to the public

This gives me the flexibility to *not* have to have release specific branches
and alters the "annoying" parts of my previous process by automating the deploy
to both PyPI environments. So lets get started!

## Deploy

- state assumptions
- do it

So before we begin, I just want to state a couple of assumptions:

- You're familiar with PyPI
- You're familiar with how a standard Python package is setup
- You're familiar with Travis CI

If any of these are a foreign topic for you, I'd suggest doing some more
reading on those topics before continuing. For the rest, lets continue.

So the first thing we want to do is update our `.travis.yml` file to include
a deploy to Test PyPI, our staging environment.

[1]: https://pypi.python.org/pypi/python-traceview/
[2]: https://pypi.python.org/
[3]: https://gist.github.com/danriti/b070fe229afc035aa03b
[4]: https://travis-ci.org/
[5]: https://github.com/danriti/python-traceview/blob/54e08dfbbeb323de26634b9535f68fcbdb0acf13/.travis.yml
[6]: https://travis-ci.org/danriti/python-traceview
[7]: https://testpypi.python.org/pypi
[8]: https://github.com/danriti/python-traceview/releases
