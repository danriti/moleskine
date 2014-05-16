""" test_github.py

"""

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

#---------------------------------------
# Mocks
#---------------------------------------

@urlmatch(netloc=NETLOC, path='/repos', method=GET)
def repos(url, request):
    name = url.path.split('/')[-1]
    content = {'name': name}
    return response(200, content, HEADERS, None, 5, request)

@urlmatch(netloc=NETLOC, path='/repos', method=GET)
def repos_rate_limit_exceeded(url, request):
    content = {'message': 'API rate limit exceeded'}
    return response(403, content, HEADERS, None, 5, request)

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
