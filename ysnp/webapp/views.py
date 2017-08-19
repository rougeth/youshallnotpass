from django.shortcuts import render
from django.conf import settings

import requests


def home(request):
    return render(request, 'webapp/home.html')


def repos(request):
    url = '{}/user/repos'.format(settings.GITHUB_API_URL)
    response = requests.get(url, headers=request.user.github_headers).json()

    return render(request, 'webapp/repos.html', {'repos': response})
