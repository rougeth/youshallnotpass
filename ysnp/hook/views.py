import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from . import tasks
from .models import Repo

GITHUB_EVENTS = {
    'pull_request': 'opened',
    'pull_request_review': 'submitted',
}


@login_required
def setup_hook(request, repo_id):
    try:
        repo = Repo.objects.get(github_id=repo_id)
    except Repo.DoesNotExists:
        return HttpResponse('Repository not found!')

    context = {
        'url': reverse('webapp_repos')
    }

    if not repo.has_hooks:
        tasks.setup_hook.delay(request.user.id, repo_id)
        context['message'] = 'The webhook is being activated...'
    else:
        context['message'] = 'Webhook already activated'

    return render(request, 'redirect.html', context)


@csrf_exempt
def hook_pullrequest(request):
    gh_event = request.META.get('HTTP_X_GITHUB_EVENT', '')

    if gh_event == 'ping':
        return HttpResponse('pong')

    data = json.loads(request.body)
    action = data['action']
    if (gh_event not in GITHUB_EVENTS.keys() or
            action != GITHUB_EVENTS[gh_event]):
        return HttpResponse("I don't what to do :/")

    pr = data['pull_request']
    repo = Repo.objects.get(github_id=pr['head']['repo']['id'])

    tasks.check_pr_reviews.delay(repo.users.first().id, pr)

    return HttpResponse('ysnp')
