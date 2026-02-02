import json
import math
import random
import sys
import os
import struct


def get(filename):
	this_file = os.path.abspath(__file__)
	this_dir = os.path.dirname(this_file)
	wanted_file = os.path.join(this_dir, filename)
	return wanted_file


with open(get('encodings.json'),'r') as file:
	table = json.load(file)


def pml(item3,item4):
	item1 = item3
	item2 = item4
	mlt1 = []
	mlt2 = []
	loses = 0
	while loses < 100:
		for el in [2,3,5,7]:
			if round(item1%el) == 0:
				mlt1.append(el)
				item1 = round(item1/el)
				loses = 0
			else:
				loses+=1
	mlt1.append(item1)
	loses = 0
	while loses < 100:
		for el in [2,3,5,7]:
			if round(item2%el) == 0:
				mlt2.append(el)
				item2 = round(item2/el)
				loses = 0
			else:
				loses+=1
	mlt2.append(item2)

	unique1 = {}
	for el in mlt1:
		if el not in unique1:
			unique1[el] = 1
		else:
			unique1[el] = unique1[el]+1

	unique2 = {}
	for el in mlt2:
		if el not in unique2:
			unique2[el] = 1
		else:
			unique2[el] = unique2[el] + 1

	items = {}
	for el in unique1:
		if el not in items:
			items[el] = unique1[el]
		else:
			if items[el] < unique1[el]:
				items[el] = unique1[el]
	for el in unique2:
		if el not in items:
			items[el] = unique2[el]
		else:
			if items[el] < unique2[el]:
				items[el] = unique2[el]
	nums = []
	for el in items:
		for num in range(items[el]):
			nums.append(el)
	rnum = nums[0]
	for el in nums[1:]:
		rnum = rnum*el
	print(f'num: {rnum} | {rnum} / {item3} = {rnum/item3} | {rnum} / {item4} = {rnum/item4}')


class MultipleEncodings:
	def __init__(self,dict1):
		self.dict1 = dict1

	def __iter__(self):
		list = []
		for el in self.dict1:
			list.append((el,self.dict1[el]))
		return iter(list)

	def export(self):
		most_used = {}
		ddt = dict(self)
		for el in ddt:
			itnm = ddt[el].decode(el)
			itnm: str
			ddt[el] = itnm.lstrip("b'").rstrip("'").encode(el)

		for el in ddt:
			try:
				most_used[ddt[el]] = most_used[ddt[el]] + 1
			except KeyError:
				most_used[el] = 1
		reverted = {}
		for el in most_used:
			reverted[most_used[el]] = el
		print(reverted[min(reverted)],ddt)
		return ddt[reverted[min(reverted)]]


def shallow_encoding(item: str):
	popular = table['popular_encodings']
	properly_encoded = {}
	for el in popular:
		try:
			properly_encoded[el] = item.encode(el,
			                errors='surrogatepass')
		except Exception as err:
			pass
	mle = MultipleEncodings(properly_encoded)
	return mle


def deep_encoding(item: str):
	items = []
	for el in table['other_encodings']:
		s1 = ''.join(list(el))
		for i in table['other_encodings'][el]:
			s2 = s1+i
			items.append(s2)
	for el in table['popular_encodings']:
		items.append(el)
	properly_encoded = {}
	for el in items:
		try:
			properly_encoded[el] = item.encode(el,
			                errors='surrogatepass')
		except Exception as err:
			pass
	mle = MultipleEncodings(properly_encoded)
	return mle


def decode_(mle: MultipleEncodings):
	dmle = dict(mle)
	weights = {}
	for el in dmle:
		weights[sys.getsizeof(dmle[el])] = el
	# print(min_weights,weights)
	decoded_mul = []
	for encoding in range(len(weights)):
		min_enc = weights[min(weights)]
		min_enc_data = dmle[min_enc]
		try:
			decoded = min_enc_data.decode(min_enc)
			decoded_mul.append(decoded)
		except:
			pass
		weights.pop(min(weights))
	most_used = {}
	for el in decoded_mul:
		try:
			most_used[el] = most_used[el]+1
		except KeyError:
			most_used[el] = 1
	reverted = {}
	for el in most_used:
		reverted[most_used[el]] = el
	try:
		return reverted[max(reverted)]
	except:
		try:
			return decode_(mle)
		except RecursionError:
			return None


def encode_by_conversion(item: str):
	ords = []
	for el in item:
		ords.append(str(ord(str(el))))
	print('encoded:','|'.join(ords).encode())
	return '|'.join(ords).encode()


def decode_by_conversion(item: bytes):
	item = item.decode()
	items = item.split('|')
	rstr = ''
	for el in items:
		rstr+=chr(int(el))
	print('decoded:',eval(rstr))
	return eval(rstr)


def encode_structed(ss):
	encoded = encode_by_conversion(ss)
	raw_numbers = encoded.decode()
	items = raw_numbers.split('|')
	items = list(map(lambda item: int(item),items))
	structed = struct.pack('B'*len(items),*items)
	rstr = structed.decode()+'|'+str(len(items))
	return rstr


def decode_structed(rstr):
	lnitems = rstr.split('|')[1]
	structed = rstr.split('|')[0]
	items = struct.unpack('B'*int(lnitems),structed.encode())
	items = list(map(lambda item: str(item),items))
	raw_numbers = '|'.join(items)
	ss = decode_by_conversion(raw_numbers.encode())
	return ss