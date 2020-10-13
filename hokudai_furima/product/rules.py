from .models import AccessLevelChoice
import rules

@rules.predicate
def has_access_permission(user, product):
    if product.access_level == AccessLevelChoice.private.name:
        if product.seller != user:
            return False
    return True

rules.add_perm('products.can_access', has_access_permission)
