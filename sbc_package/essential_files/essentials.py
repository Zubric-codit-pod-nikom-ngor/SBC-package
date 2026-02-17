import hashlib
import datetime
import json
import random
import pickle
import zlib
from scipy.differentiate import derivative
from sbc_package.essential_files.string_mergers import combine_strings, combine_strings_with_ends
import base64
import socket
import stun
import sbc_package.encoding_problem.deep_encoding as dpen


def generate_member_key():
	rstr = ''
	for el in range(random.randint(32, 128)):
		rstr += str(chr(random.randint(0, 512)))
	return rstr


# def combine_strings(s1: str, s2: str) -> str:
# 	crossings = {}
# 	pi = 0
# 	for step in range(len(s2)):
# 		for el in range(len(s2)):
# 			period = s2[el:el + step + 1]
# 			if s1.find(period, pi) != -1:
# 				crossings[period] = s1.find(period, pi)
# 				pi = s1.find(period, pi)
# 		pi = 0
# 	max_cross = {}
# 	ss = []
# 	sl = []
# 	for el in crossings:
# 		ss.append(el)
# 		sl.append(len(el))
# 	if len(crossings) == 0:
# 		return s1 + s2
# 	maximum = ss[sl.index(max(sl))]
# 	max_cross[maximum] = crossings[maximum]
# 	past_max = maximum
# 	sl.pop(ss.index(maximum))
# 	ss.remove(maximum)
# 	for smthn in range(len(crossings)):
# 		try:
# 			maximum = ss[sl.index(max(sl))]
# 			approval = 0
# 			tapr = 0
# 			for el in max_cross:
# 				if maximum in el:
# 					pass
# 				else:
# 					approval += 1
# 				tapr += 1
# 			if approval < tapr:
# 				pass
# 			else:
# 				position = 0
# 				if s2.find(maximum) + len(maximum) > len(s2) / 2:
# 					position = 1
# 				elif s2.find(maximum) + len(maximum) < len(s2) / 2:
# 					position = -1
# 				if position == 1 and s2.find(maximum) + len(maximum) == len(s2):
# 					max_cross[maximum] = crossings[maximum]
# 				elif position == -1 and s2.find(maximum) == 0:
# 					max_cross[maximum] = crossings[maximum]
# 			# print(position,maximum,s2.find(maximum),len(s2)/2,s2.find(maximum) + len(maximum))
# 			sl.pop(ss.index(maximum))
# 			ss.remove(maximum)
# 		except Exception as err:
# 			pass
# 	anchors = {}
# 	name = []
# 	index = []
# 	for el in max_cross:
# 		name.append(el)
# 		index.append(max_cross[el])
# 	if len(index) == 0:
# 		return s1 + s2
# 	anchors[name[index.index(min(index))]] = min(index)
# 	anchors[name[index.index(max(index))]] = max(index)
# 	# print(anchors,crossings,max_cross)
# 	# print('anchors',anchors)
# 	if s1 == s2:
# 		return s1
# 	elif len(anchors) == 0:
# 		return s1 + s2
# 	elif len(anchors) >= 2:
# 		vals = []
# 		name = []
# 		for el in anchors:
# 			name.append(el)
# 			vals.append(anchors[el])
# 		minval = {"min": [name[vals.index(min(vals))], min(vals)]}
# 		maxval = {"max": [name[vals.index(max(vals))], max(vals)]}
# 		lfind = 0
# 		vals_ord = []
# 		vals1 = []
# 		order = []
# 		hole = ''
# 		for el in anchors:
# 			vals1.append(s2.find(el))
# 			vals_ord.append(el)
# 		for el in range(len(vals1)):
# 			order.append(vals_ord[vals1.index(min(vals1))])
# 			vals_ord.pop(vals1.index(min(vals1)))
# 			vals1.pop(vals1.index(min(vals1)))
# 		for el in range(1000):
# 			frst = s1.find(order[0], lfind)
# 			lfind = frst
# 			scnd = s1.find(order[1], lfind)
# 			if scnd != -1:
# 				intersection = set(order[0]) & set(order[1])
# 				difference = set((*list(order[0]), *list(order[1]))) - intersection
# 				# print(difference,'int')
# 				hole = s1[frst:frst + len(difference) + 1]
# 				# print(hole, frst, scnd)
# 				break
# 		r1 = s1[:frst]
# 		r1 = r1 + s1[frst:].replace(hole, s2, 1)
# 		return r1
# 	else:
# 		r2 = s1
# 		r2 = r2.replace(max(anchors), s2, 1)
# 		return r2


initial_data = {}


def get_external_ip():
	nstun = stun.get_ip_info()
	external_ip = nstun[1]
	return external_ip


def get_local_ip():
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.connect(("8.8.8.8", 80))
			return s.getsockname()[0]
	except Exception:
		return get_external_ip()


def compress(string: str):
	compression = zlib.compress(string)
	return compression


def decompress(string):
	decompression = zlib.decompress(string)
	return decompression


class Member:
	def __init__(self,
		conn_time: datetime.datetime,
		conn_name: str,
		key: str):
		self.__creation_time = conn_time
		self.__connection_ip = conn_name
		self.__validation_key = key

	def __export(self):
		process_hidden = {}
		for el in vars(self):
			process_hidden[el[el.index('__') + 2:]] = vars(self)[el]
		rdat = ()
		for el in process_hidden:
			rdat = (*rdat, (el, process_hidden[el]))
		return rdat

	def __iter__(self):
		return iter(self.__export())


class Block:
	def __init__(self):
		self.data = None
		self.creation_time = datetime.datetime.now()
		self.sender = None

	def hash(self):
		self.__check_structure()
		return self.__hash()

	def __hash(self):
		variables = vars(self)
		hash = ''
		for el in variables:
			hash += hashlib.sha1(el.encode()).hexdigest()
			hash += hashlib.sha1(str(variables[el]).encode()).hexdigest()
		return hashlib.sha224(hash.encode()).hexdigest()

	def __check_structure(self):
		variables = vars(self)
		if 'data' in variables:
			pass
		else:
			raise SyntaxError
		if 'sender' in variables:
			pass
		else:
			raise SyntaxError
		if 'creation_time' in variables:
			pass
		else:
			raise SyntaxError
		if len(self.__hash()) > 384:
			raise SyntaxError

	def __str__(self):
		string = '-------------------------\n'
		for el in vars(self):
			string += f'| {el}: {vars(self)[el]}\n'
		string += '-------------------------'
		return string

	def export_(self):
		converted = pickle.dumps(self)
		return converted

	def import_(self, string):
		classed = pickle.loads(string,
		                       fix_imports=True)
		return classed


class Proof_of_Slowness:
	def __init__(self, block1: Block, block2: Block):
		self.data1 = block1.data
		self.data2 = block2.data

	def __get_ints(self, str):
		nums = []
		blank = 0
		while True:
			if blank >= 3:
				break
			num = ''
			is_num = False
			for el in str:
				try:
					int(el)
					if is_num == False:
						num += el
				except:
					if el == '.':
						if len(num) > 0:
							num += el
					else:
						if is_num == False:
							if len(num) > 0:
								is_num = True
								break
			if num != '':
				if '.' not in num:
					nums.append(int(num))
					str = str
				else:
					blank += 1
			else:
				blank += 1
			try:
				str = str[:str.index(num)] + str[str.index(num) + len(num):]
			except:
				pass
		return nums

	def __get_floats(self, str):
		nums = []
		blank = 0
		while True:
			if blank >= 3:
				break
			num = ''
			is_num = False
			for el in str:
				try:
					int(el)
					if is_num == False:
						num += el
				except:
					if el == '.':
						if len(num) > 0:
							num += el
					else:
						if is_num == False:
							if len(num) > 0:
								is_num = True
								break
			if num != '':
				if '.' in num:
					try:
						nums.append(float(num))
					except:
						blank += 1
				else:
					blank += 1
			else:
				blank += 1
			try:
				str = str[:str.index(num)] + str[str.index(num) + len(num):]
			except:
				pass
		return nums

	def __index_data(self, data: str):
		nums = self.__get_ints(data)
		nums = [*nums, *self.__get_floats(data)]
		processed_data = data
		order = []

		for num in nums:
			num = str(num)
			try:
				processed_data = processed_data[:processed_data.index(num)] + processed_data[
				                                                              processed_data.index(num) + len(num):]
			except:
				processed_data = data
				break

		processed_data = base64.b64encode(processed_data.encode())
		processed_data = processed_data.decode()

		for el in processed_data:
			order.append(ord(el))

		index = 0
		for el in [*nums, *order]:
			index += el

		return index

	def __der_funk(self, ind1):
		return self.diff ** ind1

	def validate(self):
		self.ind1 = self.__index_data(self.data1)
		self.ind2 = self.__index_data(self.data2)
		if self.ind2 >= self.ind1:
			self.diff = self.ind2 - self.ind1
		else:
			self.diff = self.ind1 - self.ind2
		self.deriv = derivative(self.__der_funk, 1)
		# print(f'PoW derivative = {self.deriv}')
		if self.deriv.df >= 100000:
			return False
		else:
			return True


class Chain:
	def __init__(self):
		self.blocks = []
		self.members = []
		self.fetched_by = []

	def copy(self):
		nchain = Chain()
		nchain.blocks = self.blocks.copy()
		nchain.members = self.members.copy()
		return nchain

	def add_block(self, block: Block):
		ips = list(map(lambda dat: dict(dat)['connection_ip'], self.members))
		if block.sender not in ips:
			mmb = Member(datetime.datetime.now(),
			             block.sender,
			             generate_member_key())
			self.members.append(mmb)
		else:
			member = self.members[ips.index(block.sender)]
			timedelta = block.creation_time - datetime.timedelta(seconds=3.5)
			mmb_time = dict(member)['creation_time']
			if mmb_time > timedelta:
				return None
			else:
				self.members[ips.index(block.sender)].__creation_time = datetime.datetime.now()
		if len(self.blocks) == 0:
			self.blocks.append(block)
			return None
		pos = Proof_of_Slowness(self.blocks[-1],
		                        block)
		validated = pos.validate()
		if validated == True:
			self.blocks.append(block)

	def __chain_hash(self, chain_to_check=None):
		if chain_to_check == None:
			chain_to_check = self.blocks
		hash = ''
		for el in chain_to_check:
			el: Block
			hash += el.hash()
			hash += '|'
		return hash[:-1]

	def __get_version(self):
		versions = []
		for iteration in range(len(self.blocks)):
			forms = {'connected': {},
			         'merged': {},
			         'blocks': {}}  # { location on dict } divider { cluster } divider { filename }
			temp = {}
			for el in self.blocks[:iteration + 1]:
				divided = el.data.split('$!/')
				try:
					temp[divided[2]]
				except:
					temp[divided[2]] = []
				temp[divided[2]].append(divided[1])
			nad = ''
			for el in temp:
				try:
					full = initial_data[el]
					# print(initial_data)
				except Exception as err:
					# print(err,el)
					full = ''
				for ord in temp[el]:
					try:
						if '' in ord or '' in ord:
							full = combine_strings_with_ends(ord, full)
						else:
							full = combine_strings(ord, full)
						nad += ord
					except KeyError as err:
						pass
				forming = []
				for blc in self.blocks[:iteration + 1]:
					if blc.data.split('$!/')[2] == el:
						blc: Block
						copied = Block().import_(blc.export_())
						# if blc.sender != get_local_ip() or \
						# 	copied.sender != get_external_ip():
						# 	copied.sender = hashlib.sha224(str(blc.sender).encode()).hexdigest()
						# 	copied.data = hashlib.sha224(dpen.deep_encoding(str(blc.data)).export()).hexdigest()
						# 	copied.creation_time = hashlib.sha224(str(blc.creation_time).encode()).hexdigest()
						forming.append(copied)
				forms['connected'][el] = nad
				forms['merged'][el] = full
				forms['blocks'][el] = forming
			forms['all'] = forms
			versions.append(forms)
		return versions

	def fetch_current(self):
		version = self.__get_version()[-1]
		return version

	def fetch_version(self, item: int):
		version = self.__get_version()[item]
		return version

	def fetch_period(self, item1: int, item2: int):
		period = self.blocks[item1:item2]
		forms = {'connected': {},
		         'merged': {},
		         'blocks': {}}  # { location on dict } divider { cluster } divider { filename }
		temp = {}
		for el in period:
			divided = el.data.split('$!/')
			try:
				temp[divided[2]]
			except:
				temp[divided[2]] = {}
			temp[divided[2]][divided[0]] = divided[1]
		nad = ''
		for el in temp:
			full = ''
			for ord in range(0, 8):
				try:
					full = combine_strings(temp[el][str(ord)], full)
					nad += temp[el][str(ord)]
				except KeyError as err:
					pass
			forming = []
			for blc in period:
				if blc.data.split('$!/')[2] == el:
					forming.append(blc)
			forms['connected'][el] = nad
			forms['merged'][el] = full
			forms['blocks'][el] = forming
		forms['all'] = forms
		return forms

	def verify(self, other_chain):
		hash1 = self.__chain_hash()
		hash2 = self.__chain_hash(other_chain.blocks)
		list_hash1 = hash1.split('|')
		list_hash2 = hash2.split('|')
		if len(self.blocks) == 0:
			return True
		if len(self.blocks) >= len(other_chain.blocks):
			return False
		accepted = []
		for iteration in range(max(len(list_hash1),
		                           len(list_hash2))):
			snapped = list_hash1.copy()
			try:
				curr_hash1 = list_hash1[iteration]
				snapped = list_hash2.copy()
				curr_hash2 = list_hash2[iteration]
				if curr_hash2 == curr_hash1:
					pass
				else:
					return False
			except Exception as err:
				if snapped == list_hash1:
					if accepted == []:
						pos = Proof_of_Slowness(self.blocks[-1],
						                        other_chain.blocks[iteration])
						approval = pos.validate()
					else:
						pos = Proof_of_Slowness(accepted[-1],
						                        other_chain.blocks[iteration])
						approval = pos.validate()
					if approval == True:
						accepted.append(other_chain.blocks[iteration])
					else:
						return False
				else:
					return False
		return True

	def export_(self):
		converted = pickle.dumps(self)
		return converted

	def import_(self, string: bytes):
		classed = pickle.loads(string)
		return classed
