import base64
import string
import random


def byte_to_bin(b):
    return format(b, "08b")


def bin_to_byte(b):
    return int(b, 2)


def str_to_bin(text):
    return " ".join(format(byte, "08b") for byte in text.encode("utf-8"))


def generate_random_key(length):
    characters = (
        string.ascii_letters
        + "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя "
    )
    return "".join(random.choice(characters) for _ in range(length))


def xor_encrypt(message, key):
    message_bytes = message.encode("utf-8")
    key_bytes = key.encode("utf-8")
    encrypted_bin = []
    for i in range(len(message_bytes)):
        xor_result = format(message_bytes[i] ^ key_bytes[i % len(key_bytes)], "08b")
        encrypted_bin.append(xor_result)
    encrypted_bytes = bytes([bin_to_byte(b) for b in encrypted_bin])
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode("utf-8")
    return encrypted_base64, encrypted_bin


def xor_decrypt(encrypted_message, key):
    encrypted_bytes = base64.b64decode(encrypted_message)
    key_bytes = key.encode("utf-8")
    decrypted_bin = []
    for i in range(len(encrypted_bytes)):
        xor_result = format(encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)], "08b")
        decrypted_bin.append(xor_result)
    decrypted_bytes = bytes([bin_to_byte(b) for b in decrypted_bin])
    decrypted_message = decrypted_bytes.decode("utf-8")
    return decrypted_message
