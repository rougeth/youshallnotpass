from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:
        return redirect('webapp_repos')
    return render(request, 'webapp/home.html')


@login_required
def repos(request):
    qs = request.user.repos.order_by('owner', '-updated_at')
    repos = qs.prefetch_related('hooks').all()
    return render(request, 'webapp/repos.html', {'repos': repos})
