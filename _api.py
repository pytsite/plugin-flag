"""PytSite Flag Plugin API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Callable
from pytsite import events, errors
from plugins import auth, odm

_variants = {}


def define(variant: str, default: float = 1.0, min_score: float = 1.0, max_score: float = 1.0):
    """Define a flag variant.
    """
    if variant in _variants:
        raise RuntimeError("Flag variant '{}' is already defined".format(variant))

    _variants[variant] = {
        'default': default,
        'min_score': min_score,
        'max_score': max_score,
    }


def is_defined(variant: str) -> bool:
    """Check whether a flag variant is defined.
    """
    return variant in _variants


def find(variant: str = 'like', author: auth.model.AbstractUser = None) -> odm.SingleModelFinder:
    """Create ODM finder to search for flags
    """
    if variant not in _variants:
        raise RuntimeError("Flag variant '{}' is not defined".format(variant))

    f = odm.find('flag').eq('variant', variant)

    if author:
        f.eq('author', author)

    return f


def count(entity: odm.model.Entity, variant: str = 'like') -> int:
    """Get flags count for the entity
    """
    return find(variant).eq('entity', entity).count()


def is_flagged(entity: odm.model.Entity, author: auth.model.AbstractUser = None, variant: str = 'like') -> bool:
    """Check if an entity is flagged by a user.
    """
    return bool(find(variant).eq('entity', entity).eq('author', author or auth.get_current_user()).count())


def create(entity: odm.model.Entity, author: auth.model.AbstractUser = None, variant: str = 'like',
           score: float = 1.0) -> int:
    """Create a flag.
    """
    if not author:
        author = auth.get_current_user()

    if author.is_anonymous or author.is_system:
        raise errors.ForbidCreation('Authentication required')

    if is_flagged(entity, author, variant):
        return count(entity, variant)

    # Check and set score of the flag
    f_info = _variants[variant]
    if score < f_info['min_score']:
        score = f_info['min_score']
    elif score > f_info['max_score']:
        score = f_info['max_score']

    # Save
    flag = odm.dispense('flag').f_set_multiple({
        'entity': entity,
        'author': author,
        'variant': variant,
        'score': score,
    })
    events.fire('flag@create', flag=flag)
    flag.save()

    return count(entity, variant)


def delete(entity: odm.model.Entity, author: auth.model.AbstractUser, variant: str = 'like') -> int:
    """Delete a flag
    """
    if not is_flagged(entity, author, variant):
        return count(entity, variant)

    # Find and delete
    flag = find(variant).eq('entity', entity).eq('author', author).first()
    events.fire('flag@delete', flag=flag)
    flag.delete()

    return count(entity, variant)


def toggle(entity: odm.model.Entity, author: auth.model.AbstractUser, variant: str = 'like',
           score: float = 1.0) -> int:
    """Toggle a flag
    """
    if is_flagged(entity, author, variant):
        return delete(entity, author, variant)
    else:
        return create(entity, author, variant, score)


def delete_all(entity: odm.model.Entity) -> int:
    """Delete all flags for particular entity
    """
    r = 0
    for flag_entity in odm.find('flag').eq('entity', entity).get():
        try:
            flag_entity.delete()
        except odm.error.EntityDeleted:
            # Entity was deleted by another instance
            pass

        r += 1

    return r


def on_flag_create(handler: Callable, priority: int = 0):
    """Shortcut
    """
    events.listen('flag@create', handler, priority)


def on_flag_delete(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('flag@delete', handler, priority)
