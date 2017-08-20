import json

import requests

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from account.models import User

from .tasks import check_pr_reviews


def setup_hook(request, username, repo):
    url = '{}/repos/{}/{}/hooks'.format(settings.GITHUB_API_URL, username,
                                        repo)
    data = {
        'name': 'web',
        'config': {
            'url': 'https://e2a6da2d.ngrok.io/hook/pullrequest',
            'content_type': 'json',
        },
        'events': ['pull_request', 'pull_request_review'],
        'active': True,
    }
    response = requests.post(url, json=data,
                             headers=request.user.github_headers)

    r = 'setup hook for {}/{}: {}'.format(username, repo, response.status_code)
    return HttpResponse(r)


def get_reviews(user, repo, number):
    '''
    List reviews on a pull request
    https://developer.github.com/v3/pulls/reviews/#reviews
    '''
    url = '{}/repos/{}/pulls/{}/reviews'.format(settings.GITHUB_API_URL, repo,
                                                number)
    return requests.get(url, headers=user.github_headers).json()


def update_pr_state(user, repo, sha, state):
    '''
    Update Pull Request state
    https://developer.github.com/v3/repos/statuses/#create-a-status
    '''
    states_descriptions = {
        'success': 'Ok, you can pass :)',
        'failure': 'Missing reviews!',
    }

    # `target_url` must be updated! :P
    data = {
        'state': state,
        'description': states_descriptions[state],
        'target_url': 'https://www.youtube.com/watch?v=Sagg08DrO5U',
        'context': 'You shall not pass!',
    }
    url = '{}/repos/{}/statuses/{}'.format(settings.GITHUB_API_URL, repo, sha)
    return requests.post(url, json=data, headers=user.github_headers)


@csrf_exempt
def hook_pullrequest(request):
    github_event = request.META.get('HTTP_X_GITHUB_EVENT', '')

    if github_event == 'ping':
        return HttpResponse('pong')

    if github_event not in ['pull_request', 'pull_request_view']:
        return HttpResponse("I don't what to do :/")

    data = json.loads(request.body)
    user = User.objects.get(username=data['sender']['login'])

    check_pr_reviews.delay(user.id, data['pull_request'])

    return HttpResponse('ysnp')
