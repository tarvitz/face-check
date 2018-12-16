from operator import eq, lt, gt, le, ge, ne


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


def and_expression(payload, **query):
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
    :rtype: bool
    :return: True if all query applied upon payload with True result
    """
    get = payload.get
    for raw_field, value in query.items():
        if '__' in raw_field:
            field, op = raw_field.split('__')
        else:
            op = 'eq'
            field = raw_field
        assert op in op_map, "Operation '%s' is not supported" % op

        if not op_map[op](get(field), value):
            return False
    else:
        return True
