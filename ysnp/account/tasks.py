from django.conf import settings
from django.utils.timezone import now

import requests
from celery.utils.log import get_task_logger

from ysnp.celery import app
from hook.models import Repo
from .models import User


logger = get_task_logger(__name__)


@app.task
def sync_github_repos(user_id):
    '''Sync Github repositories'''
    user = User.objects.get(id=user_id)
    user_repos = []

    # Request all user reposities taking care of pagination.
    # Requests <3.
    next_page = '{}/user/repos'.format(settings.GITHUB_API_URL)
    params = {
        'per_page': 100,
        'sort': 'updated',
    }
    while next_page:
        response = requests.get(next_page, params=params,
                                headers=user.github_headers)
        user_repos.extend(response.json())
        next_page = response.links.get('next', {}).get('url')

    # Once all repositories were requested, saves them. They will be
    # used to show repository list on /repos page.
    for user_repo in user_repos:
        try:
            repo = Repo.objects.get(github_id=user_repo['id'])
        except Repo.DoesNotExist:
            repo = Repo(
                github_id=user_repo['id'],
                owner=user_repo['owner']['login'],
                name=user_repo['name'])

        repo.private = user_repo['private']
        repo.updated_at = user_repo['updated_at']
        repo.save()
        repo.users.add(user)

    user.github_synced_at = now()
    user.save()

    return 'githut rebos synced: %s' % len(user_repos)
