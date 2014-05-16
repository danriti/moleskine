""" github.py

"""

import requests


def repos(owner, repo):
    url = 'https://api.github.com/repos/{0}/{1}'.format(owner, repo)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    results = repos('appneta', 'burndown')
    repository = results.json()

    print repository['name']


if __name__ == '__main__':
    main()
