import os
import json
import argparse
import base64


def encrypt(text, key):
    safe_text = text.replace('#', '%23')
    
    base64_bytes = base64.b64encode(safe_text.encode('utf-8'))
    base64_str = base64_bytes.decode('utf-8')

    encrypted_chars = []
    for i in range(len(base64_str)):
        key_char = key[i % len(key)]
        encrypted_char = chr(ord(base64_str[i]) ^ ord(key_char))
        encrypted_chars.append(encrypted_char)

    encrypted_str = ''.join(encrypted_chars)
    final_encrypted = base64.b64encode(encrypted_str.encode('latin1')).decode('utf-8')
    return final_encrypted


def decrypt(encrypted, key):
    encrypted_bytes = base64.b64decode(encrypted)
    encrypted_str = encrypted_bytes.decode('latin1')

    decrypted_chars = []
    for i in range(len(encrypted_str)):
        key_char = key[i % len(key)]
        decrypted_char = chr(ord(encrypted_str[i]) ^ ord(key_char))
        decrypted_chars.append(decrypted_char)

    base64_str = ''.join(decrypted_chars)
    original_bytes = base64.b64decode(base64_str)
    original_text = original_bytes.decode('utf-8')

    return original_text.replace('%23', '#')


def decrypt_file(filepath, key):
    with open(filepath, 'r', encoding='utf-8') as f:
        encrypted_data = f.read()
    return decrypt(encrypted_data, key)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', required=True)
    args = parser.parse_args()

    folder = args.folder
    key = os.getenv('DECRYPT_KEY')

    if not key:
        raise EnvironmentError("Missing DECRYPT_KEY environment variable")

    # Load rename config
    rename_path = os.path.join(folder, 'rename-config.json')
    with open(rename_path, 'r') as f:
        rename_map = json.load(f)

    for entry in rename_map:
        old = entry['old']
        new = entry['new']
        old_path = os.path.join(folder, old)
        new_path = os.path.join(folder, new)

        decrypted_data = decrypt_file(old_path, key.encode())
        with open(new_path, 'wb') as f:
            f.write(decrypted_data)

if __name__ == '__main__':
    main()
