from django.db import models


class Hook(models.Model):
    repo_github_id = models.IntegerField(unique=True)
    repo_owner = models.CharField(max_length=255)
    repo_name = models.CharField(max_length=255)
    repo_updated_at = models.DateTimeField()

    users = models.ManyToManyField('account.User', related_name='hooks')
    activated = models.BooleanField(default=False)
    github_id = models.CharField(max_length=255, blank=True)

    @property
    def repo_full_name(self):
        return '{}/{}'.format(self.repo_owner, self.repo_name)
