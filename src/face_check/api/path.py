from functools import reduce


def _object_get(entry, attr):
    """
    simple getter over object entry

    Example::

        class A(object):
            def __init__(self, attribute):
                self.attribute = attribute

            def foo():
                return self.attribute

        a = A(10)
        #: calls foo as it's callable
        _object_get(a, 'foo')
        #: returns attribute
        _object_get(a, 'attribute')

    :param object entry: an object to operate with
    :param str attr: object's attribute to get or to invoke (if it's callable,
        i.e. method)

        .. note::

            You can not use methods with one or more mandatory parameters
    :rtype: object
    :return: entry's attribute
    """
    return (
        getattr(entry, attr)() if callable(getattr(entry, attr))
        else getattr(entry, attr)
    ) if hasattr(entry, attr) else None


def _dict_get(entry, item):
    """
    simple getter over dict entry

    Example::

        sample = {'attribute': 10, 'foo': lambda: 10 * 10}

        a = A(10)
        #: calls foo as it's callable
        _object_get(sample, 'foo')
        #: returns 'attribute' value
        _object_get(sample, 'attribute')

    :param object entry: an dict object to operate with
    :param str item: entry's item to get or to invoke (if it's callable,
        i.e. method)

        .. note::

            You can not use methods with one or more mandatory parameters
    :rtype: object
    :return: entry's attribute
    """
    return (
        (entry.get(item)() if callable(entry.get(item)) else entry.get(item))
        if isinstance(entry, dict) else {}
    ) if item in entry else {}


def traverse(entry, path, *, delimiter='.'):
    """
    traverses over ``entry`` with given ``path``

    :param object | dict entry: instance to traverse through
    :param str path: path to traverse with
    :param str delimiter: path delimiter, `.` by default
    :return: anything found
    """
    if isinstance(entry, dict):
        return _traverse_dict(entry, path, delimiter=delimiter)
    return _traverse_object(entry, path, delimiter=delimiter)


def _traverse_object(entry, path, *, delimiter='.'):
    """
    safe method get obj.attr.attr1 and so on

    :param object entry: some object entry
    :param str path: iteration path
    :param str delimiter: path delimiter, `.` by default
    :return: attribute
    :example:

        .. code-block:: python
            # safe method get obj.attr.attr1 and so on
            traverse(cell, 'room.pk')
            traverse(cell, 'room.base.pk')
    :test:

        >>> class A(object):
        ...     def __init__(self, parent=None):
        ...         self.parent = parent
        >>> root = A()
        >>> node = A(parent=root)
        >>> children = A(parent=node)
        >>> traverse(children, 'parent.parent') is root
    """
    return reduce(_object_get, [entry, ] + path.split(delimiter))


def _traverse_dict(dic, path, *, delimiter='.'):
    """
    traverse dict with its path and get given item

    :param dict dic: dict object
    :param str path: path to traverse
    :param str delimiter: path delimiter, `.` by default
    :rtype: object | dict | collections.Iterable
    :return: object or empty dict
    :test:

        >>> entry = {'start': {'location': {'city': 'St.Petersburg'}}}
        >>> traverse(entry, 'start.location.city')
        'St.Petersburg'
    """
    return reduce(_dict_get, [dic, ] + path.split(delimiter))
