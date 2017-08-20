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
    user = User.objects.get(id=user_id)

    url = '{}/user/repos'.format(settings.GITHUB_API_URL)
    params = {
        'per_page': 100,
        'sort': 'updated',
    }
    repos = requests.get(url, params=params, headers=user.github_headers)
    repos = repos.json()

    for repo in repos:
        repo = Repo.objects.get_or_create(owner=repo['owner']['login'],
                                          name=repo['name'])[0]
        repo.users.add(user)

    user.github_synced_at = now()
    user.save()

    return 'githut rebos synced: %s'% len(repos)
