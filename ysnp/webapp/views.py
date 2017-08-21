from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'webapp/home.html')


@login_required
def repos(request):
    hooks = request.user.hooks.order_by('-activated', 'repo_owner',
                                        '-repo_updated_at').all()
    return render(request, 'webapp/repos.html', {'hooks': hooks})
