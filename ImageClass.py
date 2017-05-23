#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import pickle


class ImageError(Exception): pass


class CoordinateError(ImageError): pass


class LoadError(ImageError): pass


class SaveError(ImageError): pass


class ExportError(ImageError): pass


class NoFilenameError(ImageError): pass


class Image:
	def __init__(self, width, height, filename='', background='#FFFFFF'):
		self.filename = filename
		self.__background = background
		self.__data = dict()
		self.__width = width
		self.__height = height
		self.__colors = {self.__background}

	# Use @property to directly access to attributes
	@property
	def background(self):
		return self.__background

	@property
	def height(self):
		return self.__height

	@property
	def width(self):
		return self.__width

	@property
	def colors(self):
		return set(self.__colors)

	def __getitem__(self, coordinate):
		"""
		:param coordinate: (x,y) 
		:return:  color presented by coordinate
		"""
		assert len(coordinate) == 2, "coordinate should be a 2-tuple"
		if not 0 <= coordinate[0] < self.width or not 0 <= coordinate[1] < self.height:
			raise CoordinateError(str(coordinate))
		return self.__data.get(tuple(coordinate), self.__background)

	def __setitem__(self, coordinate, color):
		assert len(coordinate) == 2, "coordinate should be a 2-tuple"
		if not 0 <= coordinate[0] < self.width or not 0 <= coordinate[1] < self.height:
			raise CoordinateError(str(coordinate))
		if color == self.__background:
			self.__data.pop(tuple(coordinate), None)
		else:
			self.__data[tuple(coordinate)] = color
			self.__colors.add(color)

	def __delitem__(self, coordinate):
		assert len(coordinate) == 2, "coordinate should be a 2-tuple"
		if not 0 <= coordinate[0] < self.height or not 0 <= coordinate[1] < self.width:
			raise CoordinateError(str(coordinate))
		self.__data.pop(tuple(coordinate), None)

	def save(self, filename=None):
		if filename is not None:
			self.filename = filename
		if not self.filename:
			raise NoFilenameError()
		fh = None
		try:
			data = [self.width, self.height, self.__background, self.__data]
			fh = open(self.filename, 'wb')
			pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)  # HIGHEST_PROTOCOL = 4
		except (EnvironmentError, pickle.PickleError) as error:
			raise SaveError(str(error))
		finally:
			if fh is not None:
				fh.close()

	def load(self, filename=None):
		if filename is not None:
			self.filename = filename
		if not self.filename:
			raise NoFilenameError()
		fh = None
		try:
			fh = open(self.filename, 'rb')
			data = pickle.load(fh)
			(self.__width, self.__height, self.__background, self.__data) = data
			self.__colors = (set(self.__data.values()) | {self.__background})
		except(EnvironmentError, pickle.UnpicklingError)as error:
			raise LoadError(str(error))
		finally:
			if fh is not None:
				fh.close()

	def export(self, filename: str):
		if filename.lower().endswith('.xpm'):
			self.__export_xpm(filename)
		else:
			raise ExportError("Unsupported export format:" + os.path.splitext((filename)[1]))

	def __export_xpm(self, filename):
		"""Exports the image as an XPM file if less than 8930 colors are
		used
		"""
		name = os.path.splitext(os.path.basename(filename))[0]
		count = len(self.__colors)
		chars = [chr(x) for x in range(32, 127) if chr(x) != '"']
		if count > len(chars):
			chars = []
			for x in range(32, 127):
				if chr(x) == '"':
					continue
				for y in range(32, 127):
					if chr(y) == '"':
						continue
					chars.append(chr(x) + chr(y))
		chars.reverse()
		if count > len(chars):
			raise ExportError("cannot export XPM: too many colors")
		fh = None
		try:
			fh = open(filename, "w", encoding="ascii")
			fh.write("/* XPM */\n")
			fh.write("static char *{0}[] = {{\n".format(name))
			fh.write("/* columns rows colors chars-per-pixel */\n")
			fh.write('"{0.width} {0.height} {1} {2}",\n'.format(
				self, count, len(chars[0])))
			char_for_colour = {}
			for color in self.__colors:
				char = chars.pop()
				fh.write('"{char} c {color}",\n'.format(**locals()))
				char_for_colour[color] = char
			fh.write("/* pixels */\n")
			for y in range(self.height):
				row = []
				for x in range(self.width):
					color = self.__data.get((x, y), self.__background)
					row.append(char_for_colour[color])
				fh.write('"{0}",\n'.format("".join(row)))
			fh.write("};\n")
		except EnvironmentError as err:
			raise ExportError(str(err))
		finally:
			if fh is not None:
				fh.close()


if __name__ == "__main__":
	import doctest

	doctest.testmod()
