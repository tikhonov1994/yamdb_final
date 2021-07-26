from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value > timezone.now().year:
        params = {'value': value, }
        raise ValidationError('Год не может быть больше текущего',
                              params=params)
