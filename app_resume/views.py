from django.shortcuts import render
from django.db.models import Q
from app_accounting.models import User, Experience


def home(request):
    users = User.objects.filter(groups__name='user')
    context = {
        'users': users,
        'resume_count': users.count(),
        'companies': Experience.objects.values_list('company', flat=True),
        'users': User.objects.filter(groups__name='resume_makers'),
    }
    return render(request, 'home.html', context)


def resume(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'resume.html', context)


def search(request):
    q = request.GET.get('q')
    context = {
        'users': User.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
    }
    print(context)
    return render(request, 'search.html', context)