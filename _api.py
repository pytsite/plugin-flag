"""PytSite Flag Plugin API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import cache as _cache, events as _events
from plugins import auth as _auth, odm as _odm, query as _query

_CACHE_TTL = 300  # 5 min
_flag_types = {}
_cache_p = _cache.create_pool('flag')


def define(flag_type: str, default: float = 1.0, min_score: float = 1.0, max_score: float = 1.0):
    """Define a flag type.
    """
    if flag_type in _flag_types:
        raise RuntimeError("Flag type '{}' is already defined".format(flag_type))

    _flag_types[flag_type] = {
        'default': default,
        'min_score': min_score,
        'max_score': max_score,
    }


def is_defined(flag_type: str) -> bool:
    """Check whether a flag type is defined.
    """
    return flag_type in _flag_types


def find(flag_type: str = 'like', author: _auth.model.AbstractUser = None) -> _odm.Finder:
    """Create ODM finder to search for flags
    """
    if flag_type not in _flag_types:
        raise RuntimeError("Flag type '{}' is not defined".format(flag_type))

    f = _odm.find('flag').eq('type', flag_type)

    if author:
        f.eq('author', author)

    return f


def count(entity: _odm.model.Entity, flag_type: str = 'like') -> int:
    """Get flag count for the entity.
    """
    if flag_type not in _flag_types:
        raise RuntimeError("Flag type '{}' is not defined".format(flag_type))

    return _odm.find('flag').eq('entity', entity).eq('type', flag_type).count()


def total(entity: _odm.model.Entity, flag_type: str = 'like') -> float:
    """Get sum of flag scores for the entity.
    """
    if flag_type not in _flag_types:
        raise RuntimeError("Flag type '{}' is not defined".format(flag_type))

    c_key = 'sum.{}.{}'.format(entity.id, flag_type)
    if _cache_p.has(c_key):
        return _cache_p.get(c_key)

    ag = _odm.aggregate('flag')
    ag.match(_query.And(_query.Eq('entity', entity)))
    ag.match(_query.And(_query.Eq('type', flag_type)))

    ag.group({
        '_id': None,
        'sum': {'$sum': '$score'}
    })

    r = list(ag.get())
    v = r[0]['sum'] if r else 0.0

    return _cache_p.put(c_key, v, _CACHE_TTL)


def average(entity: _odm.model.Entity, flag_type: str = 'like') -> float:
    """Get average score for the entity.
    """
    if flag_type not in _flag_types:
        raise RuntimeError("Flag type '{}' is not defined".format(flag_type))

    c_key = 'average.{}.{}'.format(entity.id, flag_type)
    if _cache_p.has(c_key):
        return _cache_p.get(c_key)

    ag = _odm.aggregate('flag')
    ag.match(_query.And(_query.Eq('entity', entity)))
    ag.match(_query.And(_query.Eq('type', flag_type)))

    ag.group({
        '_id': None,
        'avg': {'$avg': '$score'}
    })

    r = list(ag.get())
    v = r[0]['avg'] if r else 0.0

    return _cache_p.put(c_key, v, _CACHE_TTL)


def is_flagged(entity: _odm.model.Entity, author: _auth.model.AbstractUser, flag_type: str = 'like') -> bool:
    """Check if an entity is flagged by a user.
    """
    if flag_type not in _flag_types:
        raise RuntimeError("Flag type '{}' is not defined".format(flag_type))

    return bool(_odm.find('flag').eq('entity', entity).eq('author', author).eq('type', flag_type).count())


def create(entity: _odm.model.Entity, author: _auth.model.AbstractUser = None, flag_type: str = 'like',
           score: float = 1.0) -> int:
    """Create a flag.
    """
    if not author:
        author = _auth.get_current_user()

    if author.is_anonymous or author.is_system:
        raise RuntimeError('Author of a flag should not be anonymous or system user')

    if is_flagged(entity, author, flag_type):
        return count(entity, flag_type)

    f_info = _flag_types[flag_type]

    if score < f_info['min_score']:
        score = f_info['min_score']
    elif score > f_info['max_score']:
        score = f_info['max_score']

    _odm.dispense('flag').f_set_multiple({
        'entity': entity,
        'author': author,
        'type': flag_type,
        'score': score,
    }).save()

    _events.fire('flag@create', entity=entity, user=author, flag_type=flag_type, score=score)

    return count(entity, flag_type)


def toggle(entity: _odm.model.Entity, author: _auth.model.AbstractUser, flag_type: str = 'like',
           score: float = 1.0) -> int:
    """Toggle flag.
    """
    if is_flagged(entity, author, flag_type):
        return delete(entity, author, flag_type)
    else:
        return create(entity, author, flag_type, score)


def delete(entity: _odm.model.Entity, author: _auth.model.AbstractUser, flag_type: str = 'like') -> int:
    """Remove flag.
    """
    if not is_flagged(entity, author, flag_type):
        return count(entity, flag_type)

    try:
        _odm.find('flag').eq('entity', entity).eq('author', author).eq('type', flag_type).first().delete()
    except _odm.error.EntityDeleted:
        # Entity was deleted by another instance
        pass

    _events.fire('flag@delete', entity=entity, user=author, flag_type=flag_type)

    return count(entity, flag_type)


def delete_all(entity: _odm.model.Entity) -> int:
    """Delete all flags for particular entity.
    """
    r = 0
    for flag_entity in _odm.find('flag').eq('entity', entity).get():
        try:
            flag_entity.delete()
        except _odm.error.EntityDeleted:
            # Entity was deleted by another instance
            pass

        r += 1

    return r
