from django.db import models

class ResumeMakerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name='resume_makers')