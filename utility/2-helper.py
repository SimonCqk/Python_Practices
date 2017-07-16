'''
:description  transition between str type and unicode type
'''


def to_str(str_or_bytes):
	if isinstance(str_or_bytes, str):
		return str_or_bytes.decode('utf-8')
	else:
		return str_or_bytes


def to_bytes(str_or_bytes):
	if isinstance(str_or_bytes, str):
		return str_or_bytes.encode('utf-8')
	else:
		return bytes
