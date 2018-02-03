"""
match one list with another, make current list have same structure
with the former.
"""
from collections import Iterable

def _reshape(shaper, recursive_types):
    fn_lst = [_reshape(e, recursive_types) if e.__class__ in recursive_types else next for e in shaper]
    ret_cls = shaper.__class__
    def apply(itor):
        return ret_cls(fn(itor) for fn in fn_lst)
    return apply

def reshape(shaper, recursive_types=(list, tuple, set)):
    _apply = _reshape(shaper, set(recursive_types))
    def apply(seq):
        return _apply(iter(seq))
    return apply


shaper = [(1, 2, 3, 6), {2, 3, 6}, [2, [2]]]
print(shaper)
# [(1, 2, 3, 6), {2, 3, 6}, [2, [2]]]

flatten = lambda nested: list(filter(lambda _: _, 
                                     (lambda _: ((yield from flatten(e)) if isinstance(e, Iterable) else (yield e) for e in _))(nested)))
lst = flatten(shaper)
print(lst)
# [1, 2, 3, 6, 2, 3, 6, 2, 2]

reshaper = reshape(shaper)

print(reshaper(lst))