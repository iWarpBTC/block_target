import requests
import json
import time;

lastblock = int(requests.get('https://mempool.space/api/blocks/tip/height').text)
previous_retarget_timestamp = json.loads(requests.get(f'https://mempool.space/api/blocks/{lastblock-lastblock%2016}').text)[0]['timestamp']

ts = time.time()

diff = ts - previous_retarget_timestamp
blocksInEpoch = (lastblock) % 2016
estimatedBlocks = round(diff / 60 / 10)
difficultyChange = (blocksInEpoch - (diff / 60 / 10)) / blocksInEpoch * 100
difficultyChange2 = (600 / (diff / blocksInEpoch ) -1) * 100

print('last block: {}'.format(lastblock))
print(difficultyChange)
print(difficultyChange2)

