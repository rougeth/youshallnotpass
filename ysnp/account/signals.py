from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import sync_github_repos


@receiver(post_save, sender='social_django.UserSocialAuth')
def sync_github(sender, instance, created, **kwargs):
    if created:
        sync_github_repos.delay(instance.user_id)
