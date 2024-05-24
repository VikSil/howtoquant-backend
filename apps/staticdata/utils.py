from .models import organization
from apps.classifiers.models import organization_type


def check_if_public(id: int):
    org = organization.objects.get(pk=id)
    public_type = organization_type.objects.get(type_name='Public')
    if org.org_type == public_type:
        return True
    return False


def find_ultimate_owner_id(org: organization):
    if org.owner_org is None:
        return org.id
    else:
        return find_ultimate_owner_id(org.owner_org)
