import difflib
import diff_match_patch as dmp_mod


def prioritize(*items,
				false_included = True,
				reverse = False,
				full = False):

	items = [*items]
	canceling = [None,'',b'',0,False]
	if false_included == False:
		canceling.pop(-1)
	if reverse == True:
		items = items[::-1]
	returnables = []
	prior = len(items)
	for item in items:
		if item not in canceling:
			returnables.append((item,
			                    items.index(item),
			                    True,
			                    prior))
			prior-=1
		else:
			returnables.append((item,
			                    items.index(item),
			                    False,
			                    0))

	if full == False:
		returnables = [*returnables[0]]
		return returnables[0]
	else:
		return returnables


def split_by(string: str, *items):
	rlist = []
	for el in [*items]:
		part = string[:string.find(el)]
		string = string[string.find(el)+len(part):]
		# print('part:',part,' el:',el)
		rlist.append(part)
	rlist.append(string)
	return rlist


def get_changes(s1: str, s2: str) -> str:
	s1 = f"{s1}"
	s2 = f"{s2}"
	seqm = difflib.SequenceMatcher(None, s1, s2)
	changes = []
	for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
		changes.append((opcode, s1[a0:a1], s2[b0:b1]))
	changes = list(map(lambda item: item if [*item][0] != 'None' else False, changes))
	while False in changes:
		changes.remove(False)
	reverted = ''.join(list(s2))
	ldstr = []
	for el in range(len(changes)):
		changes[el] = [*changes[el]]
	for el in changes:
		if el[0] != 'equal':
			ldstr.append(el)
	for el in ldstr:
		changes.remove(el)
	if len(changes) == 0:
		return ''
	for el in [changes[0],changes[-1]]:
		if reverted.find(el[1]) == 0 or reverted.find(el[1])+len(el[1]) == len(reverted):
			reverted = reverted.replace(el[1],'',1)


	unsplit = s2[s2.find(reverted)-4:s2.find(reverted)+len(reverted)+4]
	seqm = difflib.SequenceMatcher(None, s1, s2)
	changes1 = []
	for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
		changes1.append((opcode, s1[a0:a1], s2[b0:b1]))
	changes1 = list(map(lambda item: item if [*item][0] != 'None' else False, changes1))
	while False in changes1:
		changes1.remove(False)
	ldstr = []
	for el in range(len(changes1)):
		changes1[el] = [*changes1[el]]
	fitems = []
	for change in changes1:
		if change[0] == 'delete':
			part = s1.find(change[1])
			part = s2[part-5:part+5]
			fitems.append(part)
	for el in changes1:
		if el[0] != 'equal':
			ldstr.append(el)
	for el in ldstr:
		changes1.remove(el)
	figured = list(map(lambda item: [*item][1], changes1[1:]))
	for item in figured:
		item = ''.join(item[5:-4])
		fitems.append(unsplit[:unsplit.find(item)])
		unsplit = unsplit.replace(item,'',1)
		unsplit = unsplit.replace(fitems[-1],'',1)
	while '' in fitems:
		fitems.remove('')
	return fitems


def simpler_changes(s1: str, s2: str) -> list[str]:
	seqm = difflib.SequenceMatcher(None, s1, s2)
	changes = []
	for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
		changes.append((opcode, s1[a0:a1], s2[b0:b1]))
	changes = list(map(lambda item: item if [*item][0] != 'None' else False, changes))
	while False in changes:
		changes.remove(False)
	for el in range(len(changes)):
		changes[el] = [*changes[el]]

	rlist = []
	dellen = 0
	example = ''.join(s2)
	for el in changes:
		if el[0] == 'equal':
			example = example.replace(el[1],'',1)
			dellen += len(el[1])
		else:
			part = example.find(el[1])+dellen
			part = s2[part-4:part+len(el[2])+5]
			rlist.append(part)

	try:
		if s1.removesuffix(rlist[-1]) == s2.removesuffix(rlist[-1]):
			rlist.remove(rlist[-1])
	except:
		pass

	return rlist


def extract(text, needle, context = 5, point = 0):
	idx = text.find(needle,point)
	if idx == -1:
		return None
	start = max(0, idx-context)
	end = min(len(text)+context, idx+len(needle)+context)
	return text[start:end]


def much_harder_changes(s1: str, s2: str) -> list[str]:
	s1 = f"{s1}"
	s2 = f"{s2}"
	dmp = dmp_mod.diff_match_patch()
	dmp.Diff_Timeout = 0
	diff = dmp.diff_main(s1, s2)
	dmp.diff_cleanupSemantic(diff)
	changes = []
	for el in diff:
		changes.append([*el])
	# print(changes)

	dummy1 = ''.join(list(s1))
	dummy2 = ''.join(list(s2))
	items = set()

	for el in changes:
		if el[0] == -1:
			extraction = s2[s1.find(el[1])-5:s1.find(el[1])+5]
			dummy1 = dummy1.replace(el[1],'',1)
			items.add(extraction)
		elif el[0] == 1:
			extraction = extract(s2,el[1],point=len(s2) - len(dummy2))
			dummy2 = dummy2.replace(el[1],'',1)
			items.add(extraction)
		else:
			dummy2 = dummy2.replace(el[1],'',1)
			dummy1 = dummy1.replace(el[1],'',1)
	return [*items]


def combine_strings(s1: str, s2: str) -> str:
	s1 = f"{s1}"
	crossings = {}
	pi = 0
	for step in range(1,len(s2)):
		for el in range(len(s2)):
			period = s2[el:el + step + 1]
			if s1.find(period, pi) != -1:
				crossings[period] = s1.find(period, pi)
				pi = s1.find(period, pi)
		pi = 0
	max_cross = {}
	ss = []
	sl = []
	for el in crossings:
		ss.append(el)
		sl.append(len(el))
	if len(crossings) == 0:
		return s1 + s2
	maximum = ss[sl.index(max(sl))]
	max_cross[maximum] = crossings[maximum]
	past_max = maximum
	sl.pop(ss.index(maximum))
	ss.remove(maximum)
	for smthn in range(len(crossings)):
		try:
			maximum = ss[sl.index(max(sl))]
			approval = 0
			tapr = 0
			for el in max_cross:
				if maximum in el:
					pass
				else:
					approval += 1
				tapr += 1
			if approval < tapr:
				pass
			else:
				position = 0
				if s2.find(maximum) + len(maximum) > len(s2) / 2:
					position = 1
				elif s2.find(maximum) + len(maximum) < len(s2) / 2:
					position = -1
				if position == 1 and s2.find(maximum) + len(maximum) == len(s2):
					max_cross[maximum] = crossings[maximum]
				elif position == -1 and s2.find(maximum) == 0:
					max_cross[maximum] = crossings[maximum]
			# print(position,maximum,s2.find(maximum),len(s2)/2,s2.find(maximum) + len(maximum))
			sl.pop(ss.index(maximum))
			ss.remove(maximum)
		except Exception as err:
			pass
	anchors = {}
	name = []
	index = []
	for el in max_cross:
		name.append(el)
		index.append(max_cross[el])
	if len(index) == 0:
		return s1 + s2
	anchors[name[index.index(min(index))]] = min(index)
	anchors[name[index.index(max(index))]] = max(index)
	# print(anchors,crossings,max_cross)
	hole = ''
	if len(anchors) == 0:
		while '' in s1:
			s1 = s1.replace("",'')
		while '' in s1:
			s1 = s1.replace("",'')
		return s1 + s2
	if len(anchors) >= 2:
		vals = []
		name = []
		for el in anchors:
			name.append(el)
			vals.append(anchors[el])
		minval = {"min": [name[vals.index(min(vals))], min(vals)]}
		maxval = {"max": [name[vals.index(max(vals))], max(vals)]}
		lfind = 0
		vals_ord = []
		vals1 = []
		order = []
		for el in anchors:
			vals1.append(s2.find(el))
			vals_ord.append(el)
		for el in range(len(vals1)):
			order.append(vals_ord[vals1.index(min(vals1))])
			vals_ord.pop(vals1.index(min(vals1)))
			vals1.pop(vals1.index(min(vals1)))
		# print(order)
		for el in range(1000):
			frst = s1.find(order[0], lfind)
			lfind = frst
			scnd = s1.find(order[1], lfind)
			if scnd != -1:
				intersection = set(order[0]) & set(order[1])
				difference = set((*list(order[0]), *list(order[1]))) - intersection
				# print(difference,'int')
				hole = s1[frst:frst + len(difference) + 1]
				# print(hole, frst, scnd)
				break
		r1 = s1[:frst]
		r1 = r1 + s1[frst:].replace(hole, s2, 1)
		while '' in r1:
			r1 = r1.replace("",'')
		while '' in r1:
			r1 = r1.replace("",'')
		return r1[1:-1]
	else:
		r2 = s1
		r2 = r2.replace(max(anchors), s2, 1)
		while '' in r2:
			r2 = r2.replace("",'')
		while '' in r2:
			r2 = r2.replace("",'')
		return r2[1:-1]