from django.db import models

from utils.models import HashedAutoField


class Repo(models.Model):
    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    updated_at = models.DateTimeField()

    users = models.ManyToManyField('account.User', related_name='repos')
    hook_active = models.BooleanField(default=False)
    hook_id = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (('name', 'owner'),)

    @property
    def full_name(self):
        return '{}/{}'.format(self.owner, self.name)
