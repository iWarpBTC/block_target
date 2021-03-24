import requests
import json

print('\nBlock-Target by iWarp ')
block_height = input('zadej pořadové číslo bloku: ')

response = requests.get('https://api.blockchair.com/bitcoin/dashboards/block/{}'.format(block_height))
parse_json = json.loads(response.text)

hash = int(parse_json['data'][0 if block_height == '0' else block_height]['block']['hash'], 16)
bits = parse_json['data'][0 if block_height == '0' else block_height]['block']['bits']

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
print('bylo potřeba {} počátačních nul, hash jich měl {}\n'.format(64-len(hex(target)[2:]), 64-len(hex(hash)[2:])))

response = requests.get('https://api.blockchair.com/bitcoin/stats')
parse_json = json.loads(response.text)

hashrate = int(parse_json['data']['hashrate_24h'], 10)
prob = target / 2**256
probsec = 1 / (prob * hashrate)
print('aktuální (24h průměr) hashrate je {} hash/s ({:.2f} EH/s); vytěžení zadaného bloky by NYNÍ trvalo průměrně {:.0f} sekund ({:.2f} minut)\n'.format(hashrate, hashrate/10**18, probsec, probsec/60))