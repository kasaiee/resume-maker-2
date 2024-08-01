from django.shortcuts import render
from django.db.models import Q
from app_accounting.models import User, Experience
from app_resume.forms import UserForm, SocialForm
from app_accounting.models import Social
from django.forms import modelformset_factory

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


def resume_edit(request, user_id):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

        request.user.socials.all().delete()
        for url in request.POST.getlist('url'):
            request.user.socials.create(url=url)

    social_form_set = []
    for social in request.user.socials.all():
        social_form_set += [
            SocialForm(instance=social)
        ]
    context = {
        'form': UserForm(instance=request.user),
        'social_form_set': social_form_set
    }
    return render(request, 'resume-edit.html', context)


def search(request):
    q = request.GET.get('q')
    context = {
        'users': User.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
    }
    print(context)
    return render(request, 'search.html', context)