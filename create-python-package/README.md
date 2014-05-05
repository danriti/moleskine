# create-python-package

https://docs.python.org/2.7/distutils/packageindex.html

1. create a project following: https://github.com/pypa/sampleproject
1. edit/change/write code
1. create a login on pypi
1. check your email for a 'complete registration'
1. use test site: https://wiki.python.org/moin/TestPyPI
1. `python setup.py register`
1. `python setup.py sdist upload`

1. `pip install -e ~/work/python-traceview/`
1. version numbers are EVIL
1. MANIFEST.in file is fucking just as evil
1. testpypi will fail if dependencies don't exist on there (i.e. requests)
