#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
def log_getattribute(cls):
	# Get the original implementation
	# orig_getattr = cls.__getattr__

	# Make a new definition
	def new_getattribute(self, name):
		print('getting:', name)
		return super(cls, self).__getattribute__(name)

	def new_getattr(self, name):
		print('========getting:', name)
		return super(cls, self).__getattr__(name)

	# Attach to the class and return
	cls.__getattribute__ = new_getattribute
	cls.__getattr__ = new_getattr
	return cls


@log_getattribute
class Foo:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def compute(self):
		return self.x * self.y

	def show(self):
		print('show')

	@property
	def X(self):
		return self.x


if __name__ == '__main__':
	foo = Foo(1, 2)
	foo.x
	foo.y
	foo.compute()
	foo.show()
	foo.X
	foo.m
'''


def Tracer(aClass):
	class Wrapper:
		def __init__(self, *args, **kargs):
			self.fetches = 0
			self.wrapped = aClass(*args, **kargs)

		def __getattr__(self, attrname):
			print('Trace:' + attrname)
			self.fetches += 1
			return getattr(self.wrapped, attrname)

	return Wrapper


@Tracer
class Spam:
	def display(self):
		print('Spam!' * 8)


@Tracer
class Person:
	def __init__(self, name, hours, rate):
		self.name = name
		self.hours = hours
		self.rate = rate

	def pay(self):
		return self.hours * self.rate


food = Spam()
food.display()
print([food.fetches])

bob = Person('Bob', 40, 50)
print(bob.name)
print(bob.pay())

print('')
sue = Person('Sue', rate=100, hours=60)
print(sue.name)
print(sue.pay())

print(bob.name)
print(bob.pay())
print([bob.fetches, sue.fetches])
