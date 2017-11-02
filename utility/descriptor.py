'''
利用描述符捕获关键的实例操作，达到限定行为的目的
还包括了一个类装饰器和元类
'''


class Typed:
	def __init__(self, name, expected_type):
		self.name = name
		self.expected_type = expected_type

	def __get__(self, instance, owner):
		if instance is None:
			return self  # important!!!
		else:
			return instance.__dict__[self.name]

	def __set__(self, instance, value):
		if not isinstance(value, self.expected_type):
			raise TypeError('Expected ' + str(self.expected_type))
		instance.__dict__[self.name] = value

	def __delete__(self, instance):
		del instance.__dict__[self.name]


# 类装饰器
def type_assert(**kwargs):
	def decorator(cls):
		for name, expected_type in kwargs.items():
			setattr(cls, name, Typed(expected_type))
		return cls

	return decorator


# 使用实例
@type_assert(name=str, shares=int, price=float)
class Stock:
	def __init__(self, name, shares, price):
		self.name = name
		self.shares = shares
		self.price = price


# 类似的设计
class Descriptor:
	def __init__(self, name=None, **opts):
		self.name = name
		for key, value in opts.items():
			setattr(self, key, value)

	def __set__(self, instance, value):
		instance.__dict__[self.name] = value


class Unsigned(Descriptor):
	def __set__(self, instance, value):
		if value < 0:
			raise ValueError('Expected >= 0')
		super().__set__(instance, value)


class MaxSized(Descriptor):
	def __init__(self, name=None, **opts):
		if 'size' not in opts:
			raise TypeError('missing size option')
		super().__init__(name, **opts)

	def __set__(self, instance, value):
		if len(value) >= self.size:
			raise ValueError('size must be < ' + str(self.size))
		super().__set__(instance, value)
