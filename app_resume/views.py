from django.shortcuts import render
from app_accounting.models import User, Experience


def home(request):
    users = User.objects.filter(groups__name='user')
    context = {
        'users': users,
        'resume_count': users.count(),
        'companies': Experience.objects.values_list('company', flat=True),
    }
    return render(request, 'home.html', context)


def resume(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'resume.html', context)