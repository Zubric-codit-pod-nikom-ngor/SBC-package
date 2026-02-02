from pyaes256 import PyAES256
import random
import sbc_package.encoding_problem.deep_encoding as deep_encoding

def create_password():
	password = ''
	for x in range(16):
		password += chr(random.randint(0, 127))
	return password


def encrypt(data, password):
	aes = PyAES256()
	if type(data) == bytes:
		mle = deep_encoding.MultipleEncodings({'utf-8':data})
		data = deep_encoding.decode_(mle)
	data = list(data)
	for el in range(len(data)):
		if ord(data[el]) <= 127:
			pass
		else:
			data[el] = f'|$#{ord(data[el])}#$|'
	str_data = ''
	for el in data:
		str_data+=el
	crypted = aes.encrypt(str_data, password)
	return crypted


def decrypt(data, password):
	aes = PyAES256()
	decrypted = str(aes.decrypt(url=data['url'],
	                            iv=data['iv'],
	                            salt=data['salt'],
	                            password=password))
	dat = decrypted
	dat: str
	while '|$#' in dat:
		bounds = []
		bounds.append(dat.find('|$#'))
		bounds.append(dat.find('#$|',bounds[0]))
		bounds[1] = bounds[1]+3
		dstr = dat[bounds[0]:bounds[1]]
		letter = chr(int(dstr[3:-3]))
		dat = dat[:bounds[0]]+letter+dat[bounds[1]:]
	return dat


def encrypt_list(list, password):
	encryption_list = []
	for el in list:
		encryption_list.append(encrypt(el,
		                               password))
	return encryption_list