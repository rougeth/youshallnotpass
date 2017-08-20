from django.conf import settings

import requests

from account.models import User
from ysnp.celery import app


STATES_DESCRIPTIONS = {
    'success': 'Ok, you can pass :)',
    'failure': 'Missing reviews!',
}


def pr_reviews(repo_fullname, pr_number, headers):
    url = '{}/repos/{}/pulls/{}/reviews'.format(settings.GITHUB_API_URL,
                                                repo_fullname, pr_number)
    return requests.get(url, headers=headers).json()


@app.task
def check_pr_reviews(user_id, pull_request):
    '''
    Update Pull Requests state according to the number of approved
    reviews.
    '''

    # First step is to request all PR reviews and check how many of
    # then is marked as approved.
    user = User.objects.get(id=user_id)
    repo_fullname = pull_request['head']['repo']['full_name']
    pr_number = pull_request['number']
    url = '{}/repos/{}/pulls/{}/reviews'.format(settings.GITHUB_API_URL,
                                                repo_fullname, pr_number)
    reviews = requests.get(url, headers=user.github_headers).json()

    approved_reviews = len([review for review in reviews
                            if review['state'] == 'APPROVED' ])

    # The second step it to mark the state of the PR as `success` if it
    # has more or equal to two approved reviews or otherwise as
    # `failure`.

    # `target_url` must be updated! It's a joke!
    state = 'success' if approved_reviews > 2 else 'failure'
    data = {
        'state': state,
        'description': STATES_DESCRIPTIONS[state],
        'target_url': 'https://www.youtube.com/watch?v=Sagg08DrO5U',
        'context': 'You shall not pass!',
    }
    sha = pull_request['head']['sha']
    url = '{}/repos/{}/statuses/{}'.format(settings.GITHUB_API_URL,
                                           repo_fullname, sha)
    response = requests.post(url, json=data, headers=user.github_headers)
    return response.status_code
