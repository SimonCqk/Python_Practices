from collections import Iterable

'''
 a script to unfold nested lists.
'''


def flatten(obj, ignore_itmes=(str, bytes)):
	for item in obj:
		if isinstance(item, Iterable) and not isinstance(item, ignore_itmes):
			yield from flatten(item)
		else:
			yield item

flatten_lambda = lambda nested: list(filter(lambda _: _, 
                                     (lambda _: ((yield from flatten(e)) if isinstance(e, Iterable) else (yield e) for e in _))(nested)))

obj = [1, 2, [3, 4], [5, 6, [7, 8, 9]]]

for i in flatten(obj):
	print(i)

for i in flatten_lambda(obj):
	print(i)