from operator import eq, lt, gt, le, ge, ne

from . path import traverse


op_map = {
    'eq': eq,
    'lt': lt,
    'gt': gt,
    'gte': ge,
    'le': le,
    'lte': le,
    'ge': ge,
    'ne': ne
}


def expression(payload, **query):
    """
    Simply traverses over payload (one level depth) and query filters
    verifying payload fields with operations passed over query entries

    supported operations:

    - <none> - =
    - eq - =
    - lt - <
    - gt - >
    - lte, le - <=
    - gte, ge - >=
    - ne - !=

    :param dict payload:
    :param dict query:
    """
    for raw_field, value in query.items():
        path_chunks = raw_field.split('__')
        #: default operation
        op = 'eq'
        if path_chunks[-1] in op_map.keys():
            op = path_chunks[-1]
            path = ".".join(path_chunks[:-1])
        else:
            path = ".".join(path_chunks)
        yield op_map[op](traverse(payload, path), value)


#: in case if you need something more sophisticated, consider implementing
#: or taking django.db.models.Q interface to construct logical expressions
#: from user perspective
def and_expression(payload, **query):
    return all(expression(payload, **query))


def or_expression(payload, **query):
    return any(expression(payload, **query))
