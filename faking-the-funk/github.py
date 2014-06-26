""" github.py

"""

import requests


class Repository(object):

    SCHEME = 'https'
    AUTHORITY = 'api.github.com'
    PATH = '/repos/{0}/{1}'

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.path = self.PATH.format(self.owner, self.repo)

    @property
    def uri(self):
        return self.SCHEME + '://' + self.AUTHORITY + self.path

    def get(self):
        response = requests.get(self.uri)
        response.raise_for_status()
        return response.json()


def get_repository(owner, repo):
    uri = 'https://api.github.com/repos/{0}/{1}'.format(owner, repo)
    response = requests.get(uri)
    response.raise_for_status()
    return response.json()


def main():
    r = Repository('appneta', 'burndown')
    results = r.get()
    repository = results.json()

    print repository['name']


if __name__ == '__main__':
    main()
