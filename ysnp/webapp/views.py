from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

import requests


def home(request):
    return render(request, 'webapp/home.html')


@login_required
def repos(request):
    repos = request.user.repos.all()

    return render(request, 'webapp/repos.html', {'repos': repos})
