import random
from tqdm import tqdm
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_accounting.models import Education, Experience, Task, Skill, Language, Course, Social

from app_accounting.models.choices import LEVEL_CHOICES


User = get_user_model()

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        User.objects.all().delete()
        
        # ایجاد گروه resume_makers
        resume_makers_group, created = Group.objects.get_or_create(name='resume_makers')

        # لیست مدل‌ها
        models = [Education, Experience, Task, Skill, Language, Course, Social]

        # اضافه کردن دسترسی‌های add, change و view به گروه
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                if any([perm.codename.startswith(i) for i in ('add_', 'change_', 'view_', 'delete_')]):
                    resume_makers_group.permissions.add(perm)

        PASSWORD = 'asdf@1234'
        fake = Faker()
        admin = User.objects.create_superuser('admin', '', PASSWORD)
        for i in tqdm(range(1, 61), desc="Creating users"):
            user = User.objects.create_user(
                username=f'user{i}', 
                password=PASSWORD, 
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            user.groups.add(resume_makers_group)
            data = [
                {
                    "start_date": fake.date_between(start_date='-10y', end_date='-1y'),
                    "end_date": fake.date_between(start_date='-1y', end_date='today'),
                    "company": fake.company(),
                    "position": fake.job(),
                    "user_id": user.id
                } for i in range(5)
            ]
            user.experiences.bulk_create([Experience(**d) for d in data])

            for user_experience in user.experiences.all():
                levels = [i[0] for i in LEVEL_CHOICES]
                Skill.objects.create(**{
                    "level": random.choice(levels),
                    "title": fake.job(),
                    "user": user,
                    "tech_stack": user_experience
                })
                
                # TODO: complete later
                #         [
                #   {
                #     "model": "app_accounting.language",
                #     "pk": 1,
                #     "fields": { "level": "advanced", "name": "English", "user": 2 }
                #   },
                #   {
                #     "model": "app_accounting.course",
                #     "pk": 1,
                #     "fields": {
                #       "academy_name": "Qom University",
                #       "title": "Engineering",
                #       "description": "some text",
                #       "user": 2
                #     }
                #   },
                #   {
                #     "model": "app_accounting.social",
                #     "pk": 1,
                #     "fields": { "user": 2, "url": "https://test.com", "image": "", "name": "X" }
                #   },
                #   {
                #     "model": "app_accounting.social",
                #     "pk": 2,
                #     "fields": {
                #       "user": 2,
                #       "url": "https://test.com",
                #       "image": "",
                #       "name": "linkedin"
                #     }
                #   }
                # ]

        
