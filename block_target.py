import requests
import json

block_height = input('zadej pořadové číslo bloku: ')

response = requests.get('https://api.blockchair.com/bitcoin/dashboards/block/{}'.format(block_height))
parse_json = json.loads(response.text)

hash = int(parse_json['data']['{}'.format(block_height)]['block']['hash'], 16)
bits = parse_json['data']['{}'.format(block_height)]['block']['bits']

bbits = bits.to_bytes(4, 'big')
exp = bbits[0]
coef = int.from_bytes(bbits[1:], 'big')
target = coef * 256 ** (exp-3)
diff = 0xffff * 256 ** (0x1d-3) / target

print('hash zadaného bloku je {} \nhodnota bits je {}; tj. exponent {}, koeficient {}'.format(hex(hash)[2:].zfill(64), hex(bits)[2:], exp, coef))
print('obtížnost sítě byla {}'.format(diff))
print('porovnání hashe bloku a cíle: ')
print(hex(hash)[2:].zfill(64))
print(hex(target)[2:].zfill(64))
print('bylo potřeba {} počátačních nul, hash jich měl {}'.format(64-len(hex(target)[2:]), 64-len(hex(hash)[2:])))
