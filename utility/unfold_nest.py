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


obj = [1, 2, [3, 4], [5, 6, [7, 8, 9]]]

for i in flatten(obj):
	print(i)
