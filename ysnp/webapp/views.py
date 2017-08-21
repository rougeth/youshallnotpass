from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'webapp/home.html')


@login_required
def repos(request):
    repos = request.user.repos.order_by('-hook_activated', 'owner',
                                        '-updated_at').all()
    return render(request, 'webapp/repos.html', {'repos': repos})
