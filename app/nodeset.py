import itertools

def expand(txt):
    groups = noderanges(txt)
    fields = []
    last = -1
    for s, e in groups:
        if s > last:
            fields.append([txt[last+1:s]])
        fields.append(expand_noderange(txt[s+1:e]))
        last = e
    if last < len(txt) - 1:
        fields.append(txt[last+1], len(txt))
    nodes = product(fields)
    return [''.join(n) for n in nodes]


def noderanges(expression):
    """Return an array with the positions of all node groups"""
    start = []
    end = []
    for pos, char in enumerate(expression):
        if char == '[':
            start.append(pos)
        elif char == ']':
            end.append(pos)
    return zip(start, end)


def expand_noderange(value):
    """Expand a given node range like: '1-10,17,19'"""
    ranges = value.split(',')
    nodes = []
    for r in ranges:
        if '-' in r:
            start, end = r.split('-')
            nodes += [str(i) for i in range(int(start), int(end) + 1)]
        else:
            nodes.append(r.strip())
    return nodes


def replace(txt, start, end, repltxt):
    """Replaces the part of txt between index start and end with repltxt"""
    return txt[:start] + repltxt + txt[end+1:]


def product(lists):
    """Return a list with the cartesian product of the given lists"""
    return list(itertools.product(*lists))
