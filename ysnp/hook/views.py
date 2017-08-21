import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from account.models import User

from . import tasks
from .models import Repo


@login_required
def setup_hook(request, github_id):
    repo = Repo.objects.get(github_id=github_id)
    if repo.hook_activated:
        return redirect(reverse('webapp_repos'))

    tasks.setup_hook.delay(request.user.id, repo.id)
    return HttpResponse('The webhook is being activated...')


@csrf_exempt
def hook_pullrequest(request):
    github_event = request.META.get('HTTP_X_GITHUB_EVENT', '')

    if github_event == 'ping':
        return HttpResponse('pong')

    if github_event not in ['pull_request', 'pull_request_view']:
        return HttpResponse("I don't what to do :/")

    data = json.loads(request.body)
    user = User.objects.get(username=data['sender']['login'])

    tasks.check_pr_reviews.delay(user.id, data['pull_request'])

    return HttpResponse('ysnp')
