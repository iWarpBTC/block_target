DIFF_PERIOD = 2016
DIFF_TIMESPAN = 14 * 24 * 60 * 60
POW_LIMIT = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffff

def target_to_bits(target):
    # Determine the exponent (number of bytes needed to represent the target)
    exponent = (target.bit_length() + 7) // 8
    if exponent <= 3:
        coefficient = target << (8 * (3 - exponent))
    else:
        coefficient = target >> (8 * (exponent - 3))
    # Ensure the coefficient fits in 3 bytes
    coefficient &= 0x00ffffff
    # Adjust for overflow in coefficient (if MSB is set)
    if coefficient & 0x00800000:
        coefficient >>= 8
        exponent += 1
    # Combine exponent and coefficient into "bits" format
    bits = (exponent << 24) | coefficient
    return bits

# get block number from the user
print("\nTento kód zkontroluje, jestli bitcoinový kód, který nikdo \nnikdy neviděl, správně spočítal obtížnost těžby.")
block_number = int(input("Který blok tě zajímá: "))

import requests
import json
api_url = "https://blockstream.info/api"
our_block_hash = requests.get(f"{api_url}/block-height/{block_number}").text
our_block_header = json.loads(requests.get(f"{api_url}/block/{our_block_hash}").text)

# determine the first and last block of the previous difficutly adjustment period
if block_number < DIFF_PERIOD:
    print("Zatím nebyl žádný přepočet, obtížnost je genesis.")
    new_target = POW_LIMIT
else:
    period = (block_number // DIFF_PERIOD) - 1
    first_block = period * DIFF_PERIOD
    last_block = first_block + DIFF_PERIOD - 1

    print(f"Prvním a posledním blokem předcházejícího intervalu jsou: {first_block} a {last_block}.")

    # get block header of the first and last block of the previous difficulty adjustment period from blockchain.info API
    first_block_hash = requests.get(f"{api_url}/block-height/{first_block}").text
    last_block_hash = requests.get(f"{api_url}/block-height/{last_block}").text

    first_block_header = json.loads(requests.get(f"{api_url}/block/{first_block_hash}").text)
    last_block_header = json.loads(requests.get(f"{api_url}/block/{last_block_hash}").text)

    time_span = last_block_header['timestamp'] - first_block_header['timestamp']
    print(f"Uplynolo mezi nimi {time_span} vteřin.")
    print(f"Průměrný čas na blok je tedy {time_span / ((DIFF_PERIOD-1) * 60)} minut.")

    if time_span < DIFF_TIMESPAN/4:
        time_span = DIFF_TIMESPAN/4
    if time_span > DIFF_TIMESPAN*4:
        time_span = DIFF_TIMESPAN*4
    print(f"Upravený časový interval je {time_span} sekund.")

    bbits = last_block_header['bits'].to_bytes(4, 'big')
    exp = bbits[0]
    coef = int.from_bytes(bbits[1:], 'big')
    target = coef * 256 ** (exp-3)

    new_target = target
    new_target *= time_span
    new_target //= DIFF_TIMESPAN

    if new_target > POW_LIMIT:
        new_target = POW_LIMIT

    change_percent = 100 - ((new_target / target) * 100)

    print(f"Obtížnost se {'zvýšila' if change_percent > 0 else 'snížila'} o {abs(change_percent):.2f} %.")

new_bits = target_to_bits(new_target)

print(f"Target bits by měly být {new_bits:#x}.")
print(f"A ve skutečnosti jsou   {our_block_header['bits']:#x}.")
print()