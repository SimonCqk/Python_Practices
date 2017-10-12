#!/usr/bin/python
# -*- coding:utf-8 -*-
s = 'wow {name} ==== {var}'
name = '22'
var = 123
print(s.format_map(vars()))
