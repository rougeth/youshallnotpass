from django.conf import settings
from django.utils.timezone import now

import requests
from celery.utils.log import get_task_logger

from hook.models import Hook
from ysnp.celery import app

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
            hook = Hook.objects.get(repo_github_id=user_repo['id'])
        except Hook.DoesNotExist:
            hook = Hook(
                repo_github_id=user_repo['id'],
                repo_owner=user_repo['owner']['login'],
                repo_name=user_repo['name'])

        hook.repo_updated_at = user_repo['updated_at']
        hook.save()
        hook.users.add(user)

    user.github_synced_at = now()
    user.save()

    return 'githut rebos synced: %s' % len(user_repos)
