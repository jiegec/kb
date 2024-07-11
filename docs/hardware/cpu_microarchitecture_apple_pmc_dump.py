import plistlib
import sys

res = []
with open(sys.argv[1], 'rb') as f:
	data = plistlib.load(f)
	for key in data['system']['cpu']['events']:
		value = data['system']['cpu']['events'][key]
		if 'number' in value:
			res.append((key, value['number'], value['description']))

res = sorted(res, key=lambda x:x[1])
for key, id, desc in res:
	print(f'- {key} ({id}, 0x{id:x}): {desc}')