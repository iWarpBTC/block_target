import requests
import json
import time;

lastblock = int(requests.get('https://mempool.space/api/blocks/tip/height').text)
previous_retarget_timestamp = json.loads(requests.get(f'https://mempool.space/api/blocks/{lastblock-lastblock%2016}').text)[0]['timestamp']

ts = time.time()

diff = ts - previous_retarget_timestamp
blocksInEpoch = lastblock % 2016
estimatedBlocks = round(diff / 60 / 10)
difficultyChangeOld = (blocksInEpoch - (diff / 60 / 10)) / blocksInEpoch * 100
difficultyChange = (600 / (diff / blocksInEpoch ) -1) * 100

green = 0
red = 0

if (blocksInEpoch >= estimatedBlocks):
    base = estimatedBlocks / 2016 * 100
    green = (blocksInEpoch - estimatedBlocks) / 2016 * 100
else:
    base = blocksInEpoch / 2016 * 100
    red = min((estimatedBlocks - blocksInEpoch) / 2016 * 100, 100 - base)

print('Poslední blok: {}'.format(lastblock))
print()
print('Stará předpověď: {:.2f} %'.format(difficultyChangeOld))
print()
print('Nová předpověď: {:.2f} %'.format(difficultyChange))
print('Základ: {:.2f} %'.format(base))
print('Zelený: {:.2f} %'.format(green))
print('Červený: {:.2f} %'.format(red))

