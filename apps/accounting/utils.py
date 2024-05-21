from django.db.models import Q

from .models import strategy


def save_strategy(name: str, description: str = ''):
    new_strategy = strategy.objects.create(
        name=name, description=description, owner_org_id=9  # to be replaced by user management
    )
    new_strategy.save()
    return new_strategy
