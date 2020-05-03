# reference https://cryptography.io/en/latest/


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


backend = default_backend()
key = b'\x23\x32' * 16
iv = b'\x46' * 16
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)


def shellcodify(bytestring: bytes) -> str:
    hexstring = bytestring.hex()
    hexes = [hexstring[i:i+2] for i in range(0, len(hexstring), 2)]
    mapped = map(lambda h: '\\x' + h, hexes)
    return ''.join(list(mapped))


def encrypt_sc(sc: bytes) -> bytes:
    encryptor = cipher.encryptor()
    padded_sc = pad_data(sc)
    encrypted = encryptor.update(padded_sc) + encryptor.finalize()
    return encrypted


def decrypt_sc(encrypted_sc: bytes) -> bytes:
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_sc) + decryptor.finalize()
    unpadded_sc = unpad_data(decrypted)
    return unpadded_sc


def _is_equal_to_original(original: bytes, decrypted: bytes) -> bool:
    return original == decrypted


def _print_data(sc: bytes) -> None:
    print('=' * 64)
    print('Original:', shellcodify(sc))
    encrypted_sc = encrypt_sc(sc)
    print('Encrypted:', shellcodify(encrypted_sc))
    decrypted_sc = decrypt_sc(encrypted_sc)
    print('Decrypted:', shellcodify(decrypted_sc))
    print(_is_equal_to_original(sc, decrypted_sc))
    print('=' * 64)
    print()


def pad_data(sc: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(sc) + padder.finalize()
    return padded_data 
    

def unpad_data(sc: bytes) -> bytes:
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(sc) + unpadder.finalize()
    return unpadded_data


# test cases
# sc1 = b'\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\x50\x48\x89\xe2\x57\x48\x89\xe6\x48\x83\xc0\x3b\x0f\x05'
# _print_data(sc1)
# sc2 = b'\x6a\x04\x58\x6a\x01\x5b\x99\xb2\x08\x68\x68\x65\x72\x65\x68\x48\x69\x20\x74\x54\x59\xcd\x80\xb0\x01\x31\xdb\xcd\x80'
# _print_data(sc2)
