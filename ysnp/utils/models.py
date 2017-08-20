import decimal
import uuid

from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.functional import cached_property


@deconstructible
class GetHasher(object):

    def __init__(self, size=4):
        self.size = size

    def __call__(self):
        return self._get_hash_pk()

    def _get_hash_pk(self):
        return uuid.uuid4().hex[:self.size]


class HashedAutoField(models.CharField):
    def __init__(self, *args, **kwargs):
        size = kwargs.pop('size', 8)
        defaults = {
            'default': GetHasher(size),
            'max_length': 32,
            'editable': False,
        }
        defaults.update(kwargs)
        super().__init__(*args, **defaults)
