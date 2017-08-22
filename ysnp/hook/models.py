from django.db import models


class Repo(models.Model):
    github_id = models.IntegerField(unique=True)  # Github ID
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField()
    users = models.ManyToManyField('account.User', related_name='repos')

    class Meta:
        unique_together = (('owner', 'name'),)

    @property
    def full_name(self):
        return '{}/{}'.format(self.owner, self.name)

    @property
    def has_hooks(self):
        return bool(self.hooks.count())


class Hook(models.Model):
    github_id = models.IntegerField(unique=True)
    repo = models.ForeignKey(Repo, related_name='hooks')
    is_active = models.BooleanField(default=False)
