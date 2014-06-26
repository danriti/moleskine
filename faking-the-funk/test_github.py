""" test_github.py

"""

from decorator import decorator
import unittest

from httmock import response, urlmatch, HTTMock, with_httmock
import requests

import github


#---------------------------------------
# Constants
#---------------------------------------

NETLOC = r'(.*\.)?api\.github\.com$'
HEADERS = {'content-type': 'application/json'}
GET = 'get'

ENABLE_MOCKS = True

#---------------------------------------
# Mocks
#---------------------------------------

def fake_the_funk(mocks):
    """ I live for the funk, I die for the funk.

    """
    @decorator
    def decorated(func, *args, **kwargs):
        if ENABLE_MOCKS:
            with HTTMock(mocks):
                return func(*args, **kwargs)
        return func(*args, **kwargs)
    return decorated

@urlmatch(netloc=NETLOC, path='/repos', method=GET)
def repos(url, request):
    name = url.path.split('/')[-1]
    content = {'name': name}
    return response(200, content, HEADERS, None, 5, request)

@urlmatch(netloc=NETLOC, path='/repos', method=GET)
def repos_rate_limit_exceeded(url, request):
    content = {'message': 'API rate limit exceeded'}
    return response(403, content, HEADERS, None, 5, request)

@urlmatch(netloc=NETLOC, method=GET)
def resource_get(url, request):
    file_path = url.netloc + url.path
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except EnvironmentError:
        # catch any environment errors (i.e. file does not exist) and return a
        # 404.
        return response(404, {}, HEADERS, None, 5, request)
    return response(200, content, HEADERS, None, 5, request)


#---------------------------------------
# Tests
#---------------------------------------

class TestGithub(unittest.TestCase):

    def test_repos_context_manager(self):
        with HTTMock(repos):
            r = github.Repository('appneta', 'burndown')
            results = r.get()
        self.assertNotEqual(results, None)
        self.assertIsInstance(results, dict)

    @with_httmock(repos)
    def test_repos_decorator(self):
        r = github.Repository('appneta', 'burndown')
        results = r.get()
        self.assertNotEqual(results, None)
        self.assertIsInstance(results, dict)

    @with_httmock(repos)
    def test_repos_name(self):
        name = 'burndown'
        r = github.Repository('appneta', 'burndown')
        results = r.get()
        self.assertNotEqual(results, None)
        self.assertIsInstance(results, dict)
        self.assertTrue('name' in results)
        self.assertEqual(results['name'], name)

    @with_httmock(repos_rate_limit_exceeded)
    def test_repos_rate_limit_exceeded(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            r = github.Repository('appneta', 'burndown')
            r.get()

    @fake_the_funk(resource_get)
    def test_get_repository(self):
        results = github.get_repository('appneta', 'burndown')
        self.assertNotEqual(results, None)
        self.assertIsInstance(results, dict)
