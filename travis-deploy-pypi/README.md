# PyPI deployment with Travis CI

The TraceView team has added the ability to delete applications to our
Application Management API, so now users are enabled to programmatically delete
and clean up applications in TraceView that are no longer in use. Along with
this helpful addition, I've just released an updated version of the
[python-traceview][1] client library, to support this new functionality. For
those of you not familiar with the python-traceview library, it's an open-source
Python library for interacting with the TraceView API, granting power users the
ability to extract meaningful performance information and manage their
TraceView accounts.

As the sole maintainer of the python-traceview library, I've been following a
simple [deploy process][3] I cooked up for getting new releases of the library
on [PyPI][2] (the Python Package Index). Now that I've been maintaing the
project for almost 2 years, the "excitement" of doing a manual release has
come and gone. So naturally I began to ask myself:

> How can I automate releasing to PyPI?

Well, it turns out that the answer is quite simple with [Travis CI][4], a
continuous integration service used to build and test projects. So lets take a
closer look at how to get started!

## Release process changes

As it turns out, python-traceview is already [using][5] Travis CI, but only for
[running tests][6] against changes in the repository. So before we get into
using Travis CI for deployment, lets talk about how we want to augment the
release process. Since the python-traceview library uses Github, we are using
pull requests to introduce changes to the library. Thus, I want to update the
process to go something like this:

1. Developer submits a pull request against the repository that introduces a
   new feature or bug fix
2. Travis CI automatically runs the test suite against the pull request,
   indicating a passing or failing build
3. Once the build is passing and the feature is accepted, the pull request is
   merged into `master`
4. Travis CI automatically deploys to [Test PyPI][7] on *any* change to
   `master`
    * This allows me to use the Test PyPI site as a "staging" environment, where
      I can manually ensure that everything is good with the package
      (documentation, release history, etc)
5. Once I've determined that my "release candidate" is looking good, I can
   simply create a new [Github release][8], which will add a version tag
   to the repository
6. Travis CI automatically deploys to "production" PyPI on *any* tagged
   commit, effectively making the new release available to the public

This gives me the flexibility to *not* have to have release specific branches
and improves the "annoying" parts of my previous process by automating the
deploy to both PyPI environments.

So before we begin, I'd like to state a few assumptions:

- You are familiar with PyPI
- You are familiar with how a standard Python package is setup
- You are familiar with Travis CI

If any of these are a foreign topic for you, I'd suggest doing some more
reading on those topics before continuing. For the rest, lets get started!

## Deploying to Test PyPI

The first thing we want to do is update our `.travis.yml` file to include
a deploy configuration for Test PyPI (which we are treating as our staging
environment):

```yaml
deploy:
    # test pypi
  - provider: pypi
    distributions: sdist
    server: https://testpypi.python.org/pypi
    user: "Dan.Riti"
    password:
    on:
      branch: master
      tags: false
      condition: $TRAVIS_PYTHON_VERSION = "2.7"
```

Travis has some great documentation on the [pypi provider][10], so you can
check out that reference for any clarification. However, I'd like to point out
the following about my example above:

* The `server` setting allows us to override the default and deploy to the
  Test PyPI package index
* The `on` configuration allows us to set conditionals for when we want to
  release. So in this case, we're stating to *only* release to Test PyPI when
  the branch is `master`, there is no tag, and the Python version is `2.7`. We
  are adding the Python version because my Travis build runs against *multiple*
  [Python versions][15], so I only want to the deploy to occur once.

Great, so lets talk about passwords next. Travis provides the ability to
[encrypt][9] *any* sensitive value using the [`travis`][16] command line client.
So in our case, we want to generate an encrypted value for our PyPI password.
Once you have the command line client setup, you can simply run the following
command:

```bash
$ travis encrypt 'plain-text-password'
Please add the following to your .travis.yml file:

  secure: "<encrypted-password-string>"

```

And Travis will give us an encrypted string to use instead of our plain text
password. So now we can update our `.travis.yml` to include our secure password:

```yaml
deploy:
    # test pypi
  - provider: pypi
    distributions: sdist
    server: https://testpypi.python.org/pypi
    user: "Dan.Riti"
    password:
      secure: "<encrypted-password-string>"
    on:
      branch: master
      tags: false
      condition: $TRAVIS_PYTHON_VERSION = "2.7"
```

This is nice because I can let Travis handle the security and I'm not worried
about exposing any sensitive information, even in a publicly available
repository.

So with this configuration in place, if I had a pull request that was just
merged to master, I'll be able to view my [Travis CI build logs][11] to see the
deployment to Test PyPI:

```bash
Installing deploy dependencies
Preparing deploy
Deploying application
...
Uploading distributions to https://testpypi.python.org/pypi
```

And if I examine the logs for the Python 3.X builds, I'll see the following
[log output][12] indicating that my `on` conditional is preventing a deploy for
those versions:

```bash
...
Skipping a deployment with the pypi provider because a custom condition was not met
...
```

Pretty cool! So as you would expect, my [new version][13] is now sitting on Test PyPI,
ready for me to verify:

![Test PyPI][17]

Assuming my verification of the release candidate is looking great, lets move
onto releasing to production PyPI.

## Deploying to PyPI

Releasing to production PyPI through Travis is as simple as adding a second
deploy configuration. We can follow the steps we outlined above to add the
production specific configuration:

```yaml
deploy:
    # test pypi
    ...

    # production pypi
  - provider: pypi
    distributions: sdist
    user: "Dan.Riti"
    password:
      secure: "<encrypted-password-string>"
    on:
      branch: master
      tags: true
      condition: $TRAVIS_PYTHON_VERSION = "2.7"
```

The major differences are:

* No need for a `server` setting, as we want to use the default value
* The `tags` setting gets set to `true`, since we want to release only on tagged
  commits

Continuing on the assumption that we're doing a release, now all I have to do is
fill out the Github release form to create a new release (which will
automatically add a tagged commit):

![Github Release][18]

And by simply clicking "Publish Release", Travis does the rest of the
[work][14]:

```bash
Installing deploy dependencies
Preparing deploy
Deploying application
...
Uploading distributions to https://pypi.python.org/pypi
```

And now my brand new release is on PyPI and available to users. Now that was
easy!

![PyPI release][19]

References:

1. [Travis CI - Deployment](https://docs.travis-ci.com/user/deployment)
2. [Travis CI - PyPI Deployment](https://docs.travis-ci.com/user/deployment/pypi)
3. [Travis CI - Building a Python Project](https://docs.travis-ci.com/user/languages/python/)
4. [Travis CI - Environment Variables](https://docs.travis-ci.com/user/environment-variables/)

[1]: https://pypi.python.org/pypi/python-traceview/
[2]: https://pypi.python.org/
[3]: https://gist.github.com/danriti/b070fe229afc035aa03b
[4]: https://travis-ci.org/
[5]: https://github.com/danriti/python-traceview/blob/54e08dfbbeb323de26634b9535f68fcbdb0acf13/.travis.yml
[6]: https://travis-ci.org/danriti/python-traceview
[7]: https://testpypi.python.org/pypi
[8]: https://github.com/danriti/python-traceview/releases
[9]: https://github.com/travis-ci/travis.rb#encrypt
[10]: https://docs.travis-ci.com/user/deployment/pypi
[11]: https://travis-ci.org/danriti/python-traceview/jobs/103210541#L471-L514
[12]: https://travis-ci.org/danriti/python-traceview/jobs/103210545#L193
[13]: https://testpypi.python.org/pypi/python-traceview
[14]: https://travis-ci.org/danriti/python-traceview/jobs/103211151#L483-L526
[15]: https://github.com/danriti/python-traceview/blob/54e08dfbbeb323de26634b9535f68fcbdb0acf13/.travis.yml#L2-L7
[16]: https://github.com/travis-ci/travis.rb
[17]: https://raw.githubusercontent.com/danriti/moleskine/master/travis-deploy-pypi/images/01.png
[18]: https://raw.githubusercontent.com/danriti/moleskine/master/travis-deploy-pypi/images/02.png
[19]: https://raw.githubusercontent.com/danriti/moleskine/master/travis-deploy-pypi/images/03.png
